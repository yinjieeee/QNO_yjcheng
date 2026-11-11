# run.py

import sys
import meep as mp
import re
def mpi_excepthook(exc_type, exc_value, exc_traceback):
    """
    自訂的例外處理掛鉤：
    只有主核心會印出完整的錯誤追溯 (Traceback)，其他核心則靜默退出。
    """
    if mp.am_master():
        # 主核心正常印出錯誤
        import traceback
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)
    
    sys.stderr.flush()
    sys.exit(1)

sys.excepthook = mpi_excepthook

import warnings

def mpi_warning_showwarning(message, category, filename, lineno, file=None, line=None):
    if mp.am_master():
        # 只允許主核心印出警告
        msg = warnings.formatwarning(message, category, filename, lineno, line)
        sys.stderr.write(msg)

warnings.showwarning = mpi_warning_showwarning


##########################################################################################

import argparse
import config as cfg
import physics
import utils
import solver
import numpy as np
import meep as mp
import meep.adjoint as mpa
import os


def main():
    parser = argparse.ArgumentParser()
    # 資料夾與標記

    parser.add_argument('--serial_number', type=str, default='000')
    parser.add_argument('--tag', type=str, default='test')
    
    # 你列出的主導參數
    parser.add_argument('--width', type=float, default=4.5)
    parser.add_argument('--height', type=float, default=4.5)
    parser.add_argument('--thick', type=float, default=0.257)
    parser.add_argument('--res', type=int, default=50)
    parser.add_argument('--l_charge', type=int, default=0)
    parser.add_argument('--p_radial', type=int, default=0)
    parser.add_argument('--w0', type=float, default=0.8)
    parser.add_argument('--minimum_length', type=float, default=0.05)
    parser.add_argument('--eta_i', type=float, default=0.50)
    parser.add_argument('--eta_e', type=float, default=0.75)
    parser.add_argument('--far_times', type=float, default=10)
    parser.add_argument('--note', type=str, default='run1', help='備註訊息') # 增加備註

    # ── 續跑新增參數 ──────────────────────────────────────────
    parser.add_argument('--resume_dir',     type=str,   default=None, help='前次結果資料夾，例如 ~/LG_WS2/job1_0518_purity')
    parser.add_argument('--resume_npy',     type=str,   default=None, help='直接指定 .npy 完整路徑（優先於 resume_dir 自動搜尋）')
    parser.add_argument('--update_factor',  type=int,   default=None, help='覆蓋 config 的 nlopt update_factor')
    parser.add_argument('--start_beta_val', type=float,   default=None, help='直接指定要從哪一個具體的 beta 值開始續跑（例如 64.0 或 90.51）')

    # ── 新增：Beta Schedule 參數 ───────────────────────────────
    parser.add_argument('--start_beta',     type=float, default=4.0,       help='起始的 beta 數值')
    parser.add_argument('--beta_scale',     type=float, default=2**0.5,    help='每階 beta 的乘算放大倍率')
    parser.add_argument('--num_betas',      type=int,   default=20,        help='主循環內部生成 beta 的總點數')
    parser.add_argument('--max_beta',       type=float, default=128.0,     help='主循環生成的最高 beta 上限')
    parser.add_argument('--extra_betas',    type=float, nargs='*', default=[256.0, 512.0], 
                        help='手動追加的後期高二值化 beta 列表，用空白分隔')
    
    args = parser.parse_args()


    def fmt(val):
        """將數字轉為字串並移除小數點，例如 1.5 -> '15', 0.257 -> '257'"""
        s = str(val).replace('.', '')
        return s.lstrip('0') if s.startswith('0') else s

    # 範例結果：ell3_1515_257_w05_run1
    folder_tag = (
        f"{args.serial_number}_"
        f"ell{args.l_charge}_"
        f"{fmt(args.width)}{fmt(args.height)}_{fmt(args.thick)}_"
        f"w{fmt(args.w0)}_"
        f"ml{fmt(args.minimum_length)}_"
        f"ie{fmt(args.eta_i)}0{fmt(args.eta_e)}_"
        f"{args.note}"
    )
    # 將外部參數寫入 config 模組
    cfg.test_param = folder_tag
    cfg.design_width = args.width
    cfg.design_height = args.height
    cfg.design_thick = args.thick
    cfg.resolution = args.res
    cfg.l_charge = args.l_charge
    cfg.p_radial = args.p_radial
    cfg.w0_target = args.w0
    cfg.minimum_length = args.minimum_length
    cfg.eta_i = args.eta_i
    cfg.eta_e = args.eta_e
    cfg.far_times = args.far_times

    
    cfg.start_beta_val  = args.start_beta_val
    # 重要：呼叫更新函式，讓 config 重新計算 zR, w0_radius 等
    # ── 寫入 config (新增 Beta 參數覆蓋) ──────────────────────
    cfg.start_beta      = args.start_beta
    cfg.beta_scale      = args.beta_scale
    cfg.num_betas       = args.num_betas
    cfg.max_beta        = args.max_beta
    cfg.extra_betas     = args.extra_betas
    
    if args.update_factor is not None:
        cfg.nlopt_params['update_factor'] = args.update_factor  # 新增覆蓋
    cfg.update_config()

    if mp.am_master():
        os.makedirs(cfg.dir_path, exist_ok=True)
        with open(os.path.join(cfg.dir_path, "process.pid"), "w") as f:
            f.write(str(os.getpid()))
        print(f"Process PID: {os.getpid()} recorded in {cfg.dir_path}")
    

    # 2. 執行優化迴圈   
    Nx = int(cfg.resolution * cfg.design_width) + 1
    Ny = int(cfg.resolution * cfg.design_height) + 1

    if args.resume_npy:
        # 直接指定 npy 路徑
        x0 = cfg.load_structure_npy(args.resume_npy)
    elif args.resume_dir:
        # 自動在 resume_dir/beta_data/ 找最新的 structure_*.npy
        beta_data_dir = os.path.join(os.path.expanduser(args.resume_dir), 'beta_data')

        candidates = [f for f in os.listdir(beta_data_dir) if 'structure_iter_' in f and f.endswith('.npy')]
        if not candidates:
            raise FileNotFoundError(f"[run] 在 {beta_data_dir} 找不到任何 structure_iter_*.npy")
        latest_fn = max(candidates, key=lambda fn: int(re.search(r'iter_(\d+)', fn).group(1)))
        latest = os.path.join(beta_data_dir, latest_fn)
        if mp.am_master():
            print(f"[run] 自動選取最新結構: {latest}")
        x0 = cfg.load_structure_npy(latest)

    else:
        
        xx, yy = np.meshgrid(
            np.linspace(-cfg.design_width/2, cfg.design_width/2, Nx),
            np.linspace(-cfg.design_height/2, cfg.design_height/2, Ny))
    
        phi = np.arctan2(yy, xx)
        x0 = 0.5 + 0.01 * np.sin(cfg.l_charge * phi)
        x0 = np.clip(x0.flatten(), 0, 1)

    # ── beta schedule 裁切（續跑跳過已完成的 stage）────────────
    beta_schedule_full = cfg.get_beta_schedule()
    if cfg.start_beta_val is not None:
        # 尋找與輸入的 start_beta_val 最接近的 beta 索引
        # 使用 np.isclose 容忍浮點數運算產生的些微誤差
        closest_idx = None
        for idx, b in enumerate(beta_schedule_full):
            if np.isclose(b, cfg.start_beta_val, rtol=1e-2): # 允許 1% 以內的誤差
                closest_idx = idx
                break
        
        if closest_idx is not None:
            beta_schedule = beta_schedule_full[closest_idx:]
            if mp.am_master():
                print(f"[run] 成功匹配到 Beta={cfg.start_beta_val}，將從索引 [{closest_idx}] 開始續跑。")
        else:
            # 找不到精確匹配時的防呆機制：自動抓第一個大於等於該值的階段
            beta_schedule = [b for b in beta_schedule_full if b >= cfg.start_beta_val]
            if mp.am_master():
                print(f"[run] 警告：無法精確匹配 Beta={cfg.start_beta_val}，自動裁切後的 schedule 剩餘：{beta_schedule}")
    else:
        # 全新跑，不裁切
        beta_schedule = beta_schedule_full
        
    if mp.am_master():
        print(f"[run] beta schedule: {beta_schedule}")

        
    nlopt_params = cfg.nlopt_params
    nlopt_params['lb'] = np.zeros_like(x0)
    nlopt_params['ub'] = np.ones_like(x0)
    
    if mp.am_master():
        print("Starting Optimization...")

    filter_radius = mpa.get_conic_radius_from_eta_e(cfg.minimum_length, cfg.eta_e)
    mapping_func = physics.get_mapping(filter_radius, cfg)
    # 初始化優化引擎
    opt_engine = solver.LGOptimizer(cfg, mapping_func)
    opt_engine.optimize(x0, beta_schedule, nlopt_params)

    # --- 新增：優化結束後執行獨立後處理 ---
    best_snap = opt_engine.best_snapshot
    if best_snap['mapped_x'] is not None:
        import eval_chirality
        # 將目前的設定寫入 evaluator 需要的 cfg_dict
        opt_engine.config_dict['minimum_length'] = cfg.minimum_length
        eval_chirality.run_chirality_analysis(
            dir_path=cfg.dir_path,
            iter_num=best_snap['iter'],
            beta=opt_engine.current_beta,
            mapped_x=best_snap['mapped_x'],
            cfg_dict=opt_engine.config_dict
        )
    else:
        if mp.am_master():
            print("[run] 警告：無法取得最佳結構，略過手性傳播分析。")

if __name__ == '__main__':
    mp.verbosity(0)
    main()


