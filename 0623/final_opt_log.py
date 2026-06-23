#config.py
import os
import numpy as np
import nlopt
import meep as mp

# --- 續跑相關參數 ---
resume_from = None       # 若非 None，表示從這個 .npy 路徑讀取初始結構
start_beta_val = None

# --- Beta Schedule 控制參數（新增預設值，可被 run_3D.py 覆蓋） ---
start_beta = 4.0
beta_scale = 2**0.5
num_betas = 20
max_beta = 128.0
extra_betas = [256.0, 512.0]

# --- 續跑輔助函式 ---
def load_structure_npy(npy_path):
    npy_path = os.path.expanduser(npy_path)
    if not os.path.isfile(npy_path):
        raise FileNotFoundError(f"[config] 找不到續跑結構檔: {npy_path}")
    data = np.load(npy_path)
    x0 = data.flatten().astype(np.float64)
    print(f"[config] 讀取續跑結構: {npy_path} shape={data.shape} -> flatten={x0.shape}")
    return x0

# ... (其餘主導參數與 update_config 保持不變) ...

# 修改後的 get_beta_schedule
def get_beta_schedule():
    global start_beta, beta_scale, num_betas, max_beta, extra_betas
    schedule = []
    curr = start_beta
    for _ in range(num_betas):
        schedule.append(min(curr, max_beta))
        curr *= beta_scale
    
    if extra_betas:
        schedule.extend(extra_betas)
        
    print(f'beta schedule={sorted(list(set(schedule)))}')
    return sorted(list(set(schedule)))

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# --- 1. 預設主導參數 (會被 run_3D.py 的 argparse 覆蓋) ---
design_width = 1.5
design_height = 1.5
design_thick = 0.257
resolution = 10
l_charge = 0
p_radial = 0
w0_target = 0.5

minimum_length = 0.1
eta_i = 0.5
eta_e = 0.55

test_param = "default"
dir_path = ""

far_times = 10

FF_WIDTH_MAP = {
    0: 3.04,
    1: 3.64,
    2: 4.10,
    3: 4.48,
    4: 4.82,
    5: 5.12,
}

# --- 2. 建立更新函式 ---
def update_config():
    """當主導參數被修改後，重新計算相關物理量與路徑"""
    global dir_path, zR, far_field_distance, z_ff_total, w0_radius, ff_width, ff_res
    global Sx, Sy, Sz, monitor_z, src_z, wavelength, frequency, fwidth, dpml, source_pml, monitor_pml
    global material_monitor, source_material, tmd_thick, base_thick, tmd_width, tmd_height, base_width, base_height
    
    # 更新資料夾路徑
    base_dir = os.path.expanduser("~/LG_WS2")
    dir_path = os.path.join(base_dir, test_param)

    # 重新計算物理參數 (這部分搬運你原本在 config.py 的邏輯)
    wavelength = 0.593
    frequency = 1 / wavelength
    fwidth = frequency * 0.1
    dpml = 0.3
    source_pml = 0.3
    monitor_pml = 0.3
    material_monitor = 0.05

    tmd_width = design_width
    tmd_height = design_height
    base_width = design_width
    base_height = design_height
    
    # 遠場相關計算
    zR = np.pi * w0_target**2 / wavelength
    far_field_distance = far_times * zR  # 假設 far_times = 10
    z_ff_total = far_field_distance + material_monitor
    w0_radius = w0_target * np.sqrt((z_ff_total / zR)**2 + 1)
    ff_width_times = FF_WIDTH_MAP.get(l_charge, 3.0)
    ff_width = ff_width_times * w0_radius
    ff_res = 200 # 你原本 code 寫死 100

    # 模擬範圍計算
    Sx = design_width + 2 * dpml
    Sy = design_width + 2 * dpml
    source_material = 1/resolution
    tmd_thick = 1/resolution
    base_thick = dpml + source_pml + source_material
    Sz = base_thick + tmd_thick + design_thick + material_monitor + monitor_pml + dpml

    monitor_z = Sz/2 - dpml - monitor_pml
    src_z = -Sz/2 + base_thick + tmd_thick/2

# 預設執行一次初始化
update_config()

nlopt_params = {
    'algorithm': nlopt.LD_MMA,
    'update_factor': 12,  # 這裡的預設值會被 args.update_factor 覆蓋
    'ftol': 1e-5
}#models.py

import meep as mp
import config as cfg
import numpy as np


def build_scene_data(config_dict):
    WS2 = mp.Medium(index=2.4)
    gap = mp.Medium(index=3.31)
    diamond = mp.Medium(index=2.4)
    air = mp.air
    
    cell_size = mp.Vector3(config_dict['Sx'], 
                           config_dict['Sy'],
                           config_dict['Sz'])
    
    design_center = mp.Vector3(0, 0, -config_dict['Sz']/2 + config_dict['base_thick'] + config_dict['tmd_thick'] + config_dict['design_thick']/2)

    tmd_center = mp.Vector3(0, 0, -config_dict['Sz']/2 + config_dict['base_thick'] + config_dict['tmd_thick']/2)

    base_center = mp.Vector3(0, 0, -config_dict['Sz']/2 + config_dict['base_thick']/2)
    
    Nx = int(config_dict['resolution'] * config_dict['design_width']) + 1
    Ny = int(config_dict['resolution'] * config_dict['design_height']) + 1
    design_var = mp.MaterialGrid(mp.Vector3(Nx, Ny, 1), mp.air, gap, grid_type="U_MEAN")

    #pml_layer=[mp.PML(config_dict['dpml'], direction=mp.Z)]
    pml_layer=[mp.PML(config_dict['dpml'])]
    geometry = [
        mp.Block(center=design_center,
                 size=mp.Vector3(config_dict['design_width'], config_dict['design_height'], config_dict['design_thick']),
                 material=design_var),
        mp.Block(center=tmd_center,
                 size=mp.Vector3(config_dict['design_width'], config_dict['design_height'], config_dict['tmd_thick']),
                 material=WS2),
        mp.Block(center=base_center,
                 size=mp.Vector3(config_dict['design_width'], config_dict['design_height'], config_dict['base_thick']),
                 material=diamond)
    ]


    src_z = -config_dict['Sz']/2 + config_dict['base_thick'] + config_dict['tmd_thick']/2
    src_center = mp.Vector3(0, 0, src_z)

    w0 = config_dict.get('w0_target', 0.5)

    #def gaussian_amp(pt):
    #    r2 = pt.x**2 + pt.y**2
    #    return np.exp(-r2 / (2 * w0**2))   # 只回傳實數振幅分布

    src = mp.GaussianSource(config_dict['frequency'], fwidth=config_dict['fwidth'])
    src_size = mp.Vector3(0, 0, 0)
    
    source = [
        mp.Source(src, component=mp.Ex, center=src_center, size=src_size, amplitude=1.0),
        mp.Source(src, component=mp.Ey, center=src_center, size=src_size, amplitude=1j)
    ]


    monitor_z = config_dict['Sz']/2 - config_dict['dpml'] - config_dict['monitor_pml']
    
    return {
        "cell_size": cell_size,
        "geometry": geometry,
        "sources": source,
        "pml_layer": pml_layer,
        "design_center": design_center,
        "monitor_z": monitor_z
    }#physics.py

import meep as mp
import meep.adjoint as mpa
import numpy as np
from autograd import numpy as npa
from scipy.special import factorial
from scipy.special import genlaguerre

# === Adjoint (mapping, J_flux) ===

def get_mapping(filter_radius, cfg):
    def mapping(x, eta, beta):
        filtered = mpa.conic_filter(x, filter_radius, cfg.design_width, cfg.design_height, cfg.resolution)
        projected = mpa.tanh_projection(filtered, beta, eta)
        return projected.flatten()
    return mapping


def create_opt_problem(sim, design_region, config_dict, field_cache=None):
    if field_cache is None:
        field_cache = {'near_fields': None, 'ff_fields': None}

    
    # 1. 定義 Near2Far 區域 (Monitor)
    monitor_z = config_dict['monitor_z']
    
    near_monitor = mp.Volume(
        center=mp.Vector3(0, 0, monitor_z),
        size=mp.Vector3(config_dict['design_width'], config_dict['design_height'], 0)
        ) 

    n2f_monitor = mp.Near2FarRegion(
        center=mp.Vector3(0, 0, monitor_z),
        size=mp.Vector3(config_dict['design_width'], config_dict['design_height'], 0),
        direction=mp.Z
    )

    nf_dft = sim.add_dft_fields(
        [mp.Ex, mp.Ey, mp.Ez, mp.Hx, mp.Hy, mp.Hz],
        config_dict['frequency'], config_dict['frequency'], 1,
        center=mp.Vector3(0, 0, monitor_z),
        size=mp.Vector3(config_dict['design_width'], config_dict['design_height'], 0)
    )


    # 2. 建立 N2F 物件
    ff_dist = config_dict['far_field_distance']
    ff_width = config_dict['ff_width']
    ff_res = config_dict['ff_res']
    
    x_ff = np.linspace(-ff_width/2, ff_width/2, ff_res)
    y_ff = np.linspace(-ff_width/2, ff_width/2, ff_res)
    
    # 建立點列表
    ff_points = [mp.Vector3(x, y, monitor_z + ff_dist) for x in x_ff for y in y_ff]
    n2f_obj = mpa.Near2FarFields(sim, [n2f_monitor], ff_points)

    
    # Adjoint 的 N2F 元件
    near_Ex = mpa.FourierFields(sim,near_monitor,mp.Ex)
    near_Ey = mpa.FourierFields(sim,near_monitor,mp.Ey)
    near_Ez = mpa.FourierFields(sim,near_monitor,mp.Ez)
    near_Hx = mpa.FourierFields(sim,near_monitor,mp.Hx)
    near_Hy = mpa.FourierFields(sim,near_monitor,mp.Hy)
    near_Hz = mpa.FourierFields(sim,near_monitor,mp.Hz)
        
    # 3. 計算 Target Field (LG Mode)
    ff_coords = np.array([(p.x, p.y) for p in ff_points])
    X_flat = ff_coords[:, 0]
    Y_flat = ff_coords[:, 1]

    dx = ff_width / (ff_res - 1) if ff_res > 1 else 0
    dy = dx
    area = dx * dy
    
    # --- LG Mode 參數 ---
    zR          = config_dict['zR']    
    z_ff_total  = config_dict['z_ff_total']
    k           = 2 * np.pi / config_dict['wavelength']
    l_charge    = config_dict['l_charge']
    p_radial    = config_dict.get('p_radial', 0)
    w0_radius   = config_dict['w0_radius']  


    # 座標與基本振幅
    rho = np.sqrt(X_flat**2 + Y_flat**2)
    phi = np.arctan2(Y_flat, X_flat)
    
    term1 = (np.sqrt(2) * rho / w0_radius) ** np.abs(l_charge)
    term2 = np.exp(-(rho**2) / (w0_radius**2))

    Lpl = genlaguerre(p_radial, np.abs(l_charge))
    laguerre_term = Lpl(2 * rho**2 / w0_radius**2)

    azimuthal_phase = np.exp(1j * l_charge * phi)

    Rz = z_ff_total * (1 + (zR / z_ff_total)**2)
    curvature_phase = np.exp(1j * k * (rho**2) / (2 * Rz))
    
    gouy_value = (2 * p_radial + np.abs(l_charge) + 1) * np.arctan(z_ff_total / zR)
    gouy_phase = np.exp(-1j *gouy_value)
    
    LG_profile = term1 * term2 * laguerre_term * azimuthal_phase * curvature_phase * gouy_phase
    
    E_target_x_raw = LG_profile / np.sqrt(2)
    E_target_y_raw = 1j *LG_profile / np.sqrt(2)
    power_target_raw = np.sum(np.abs(E_target_x_raw)**2 + np.abs(E_target_y_raw)**2) * area
    
    E_target_x = E_target_x_raw / np.sqrt(power_target_raw)
    E_target_y = E_target_y_raw / np.sqrt(power_target_raw)
    power_target = 1.0
    

    def J(ff_fields, near_Ex, near_Ey, near_Ez, near_Hx, near_Hy, near_Hz):
        power_target = 1.0
        alpha = 0.1
        eps = 1e-30
        # 使用 autograd 的 slicing 提取分量
        ff_Ex = ff_fields[:, 0, 0]
        ff_Ey = ff_fields[:, 0, 1]
        
        # (2500, 1, 6)
        #shape = npa.shape(ff_fields)
        #n_loc_pts = shape[0]      # 當前進程 (Rank) 負責的遠場點數
        #n_freq = shape[1]         # 頻率數量 (通常是 1)
        #n_comp = shape[2]         # 分量數量 (固定為 6: Ex, Ey, Ez, Hx, Hy, Hz)
        if isinstance(ff_Ex, np.ndarray):
            field_cache['ff_fields'] = {
                'Ex': ff_fields[:, 0, 0].copy(),
                'Ey': ff_fields[:, 0, 1].copy(),
                'Ez': ff_fields[:, 0, 2].copy(),
                'Hx': ff_fields[:, 0, 3].copy(),
                'Hy': ff_fields[:, 0, 4].copy(),
                'Hz': ff_fields[:, 0, 5].copy()
            }
        if isinstance(near_Ex, np.ndarray) and isinstance(near_Ey, np.ndarray) and isinstance(near_Ez, np.ndarray) and isinstance(near_Hx, np.ndarray) and isinstance(near_Hy, np.ndarray) and isinstance(near_Hz, np.ndarray):
            field_cache['near_fields'] = {
                'Ex': near_Ex[0, :, :].copy(),
                'Ey': near_Ey[0, :, :].copy(),
                'Ez': near_Ez[0, :, :].copy(),
                'Hx': near_Hx[0, :, :].copy(),
                'Hy': near_Hy[0, :, :].copy(),
                'Hz': near_Hz[0, :, :].copy(),
            }
            
        overlap      = npa.sum(ff_Ex * npa.conj(E_target_x) +
                        ff_Ey * npa.conj(E_target_y)) * area
        overlap_abs2 = npa.abs(overlap)**2
        power_sim    = npa.sum(npa.abs(ff_Ex)**2 + npa.abs(ff_Ey)**2) * area
        purity       = (npa.abs(overlap)**2) / (power_sim * power_target + eps)
        
        fom = npa.log(purity + eps) + alpha * npa.log(overlap_abs2 + eps)
        
        if not hasattr(power_sim, '_value'): 
            field_cache['overlap_abs2'] = float(overlap_abs2)
            field_cache['purity']       = float(purity)
            print(f'--- J diagnostic ---')
            print(f'  [FOM] power_sim                                                   = {float(power_sim):.6e}')
            print(f'  [FOM] overlap_abs2                                                = {float(npa.abs(overlap)**2):.6e}')
            print(f'  [FOM] purity                                                      = {float(purity):.6e}')
            print(f'  [FOM] npa.log(purity + eps) + alpha * npa.log(overlap_abs2 + eps) = {float(purity):.6e}')
            print(f'--------------------')
          
            
        return -fom


    # 5. 建立問題
    opt = mpa.OptimizationProblem(
        simulation=sim,
        objective_functions=[J],
        objective_arguments=[n2f_obj, near_Ex, near_Ey, near_Ez, near_Hx, near_Hy, near_Hz], 
        design_regions=[design_region],
        frequencies=[config_dict['frequency']],
        decay_by=1e-5
    ) #maximum_run_time=400
    opt.field_cache = field_cache
    return opt#run.py
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
    parser.add_argument('--width', type=float, default=1.5)
    parser.add_argument('--height', type=float, default=1.5)
    parser.add_argument('--thick', type=float, default=0.257)
    parser.add_argument('--res', type=int, default=50)
    parser.add_argument('--l_charge', type=int, default=0)
    parser.add_argument('--p_radial', type=int, default=0)
    parser.add_argument('--w0', type=float, default=0.5)
    parser.add_argument('--minimum_length', type=float, default=0.05)
    parser.add_argument('--eta_i', type=float, default=0.50)
    parser.add_argument('--eta_e', type=float, default=0.55)
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
        candidates = sorted([
            f for f in os.listdir(beta_data_dir) if f.startswith('structure_') and f.endswith('.npy')
        ])
        if not candidates:
            raise FileNotFoundError(f"[run] 在 {beta_data_dir} 找不到任何 structure_*.npy")
        latest = os.path.join(beta_data_dir, candidates[-1])
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
    

if __name__ == '__main__':
    mp.verbosity(0)
    main()#solver.py

import numpy as np
import meep as mp
import meep.adjoint as mpa
import nlopt
import csv
import os
from autograd import tensor_jacobian_product
import utils
import models
import physics
import time

class LGOptimizer:
    def __init__(self, cfg, mapping):
        self.cfg = cfg
        self.field_cache = {'near_fields': None, 'ff_fields': None}
        self.beta_checkpoints = []
        self.config_dict = {
            'resolution':         cfg.resolution,
            'design_width':       cfg.design_width,
            'design_height':      cfg.design_height,
            'design_thick':       cfg.design_thick,
            'tmd_width':          cfg.tmd_width,
            'tmd_height':         cfg.tmd_height,
            'tmd_thick':          cfg.tmd_thick,
            'base_width':         cfg.base_width,
            'base_height':        cfg.base_height,
            'base_thick':         cfg.base_thick,
            'source_material':    cfg.source_material,
            'material_monitor':   cfg.material_monitor,
            'monitor_pml':        cfg.monitor_pml,
            'Sx':                 cfg.Sx,
            'Sy':                 cfg.Sy,
            'Sz':                 cfg.Sz,
            'dpml':               cfg.dpml,
            'frequency':          cfg.frequency,
            'fwidth':             cfg.fwidth,
            'eta_i':              cfg.eta_i,
            'eta_e':              cfg.eta_e,
            'wavelength':         cfg.wavelength,
            'monitor_z':          cfg.monitor_z,
            'src_z':              cfg.src_z,
            'far_field_distance': cfg.far_field_distance,
            'ff_width':           cfg.ff_width,
            'ff_res':             cfg.ff_res,
            'l_charge':           cfg.l_charge,
            'p_radial':           cfg.p_radial,
            'w0_target':          cfg.w0_target,
            'w0_radius':          cfg.w0_radius,
            'zR':                 cfg.zR,
            'z_ff_total':         cfg.z_ff_total,
        }
        self.best_snapshot = {
            'x'               : None,
            'mapped_x'        : None,
            'fom'             : -np.inf,
            'iter'            : None,
            'near_fields'     : None,
            'ff_fields'       : None,
            'overlap'         : None,
            'purity'          : None,
        }
        self.mapping = mapping

        self.cur_iter = [0]
        self.current_beta = 1.0
        self.history_FOM = []
        self.history_overlap = []
        self.history_purity = []

        self.obj_csv_path = os.path.join(cfg.dir_path, "objective_evolution.csv")
        if mp.am_master():
            utils.init_csv(self.obj_csv_path, ["Iteration", "Beta", "Raw_Purity", "Overlap_Abs2", "FOM"])

        scene = models.build_scene_data(self.config_dict)

        self.monitor_z  = scene['monitor_z']
        self.design_center = scene['design_center']
        self.design_size = mp.Vector3(
            self.config_dict['design_width'],
            self.config_dict['design_height'],
            self.config_dict['design_thick']
        )

        self.Nx = int(self.config_dict['resolution'] * self.config_dict['design_width']) + 1
        self.Ny = int(self.config_dict['resolution'] * self.config_dict['design_height']) + 1
        self.design_var = scene['geometry'][0].material

        design_region = mpa.DesignRegion(
            self.design_var,
            volume=mp.Volume(
                center=scene['design_center'],
                size=mp.Vector3(
                    self.config_dict['design_width'],
                    self.config_dict['design_height'],
                    self.config_dict['design_thick']
                )
            )
        )
        self.grid_shape = (self.Nx, self.Ny, 1)

        k_point = mp.Vector3(0, 0, 0)
        self.sim = mp.Simulation(
            cell_size=scene['cell_size'],
            geometry=scene['geometry'],
            sources=scene['sources'],
            boundary_layers=scene['pml_layer'],
            resolution=self.config_dict['resolution'],
            default_material=mp.air,
            force_complex_fields=True,
            k_point=k_point
        )

        def custom_update(params):
            shaped_params = params.reshape(self.Nx, self.Ny, 1)
            checked = self.design_var.check_weights(shaped_params)
            self.design_var.weights = checked.astype(np.float64)

        design_region.update_design_parameters = custom_update

        self.plot_sim = mp.Simulation(
            cell_size=scene['cell_size'],
            geometry=scene['geometry'],
            boundary_layers=scene['pml_layer'],
            resolution=self.config_dict['resolution'],
            default_material=mp.air,
            force_complex_fields=True,
            k_point=k_point
        )

        self.opt_problem = physics.create_opt_problem(
            self.sim, design_region, self.config_dict, field_cache=self.field_cache
        )




    def objective(self, x, grad):
        self.cur_iter[0] += 1
        start_time = time.time()

        mapped_x = self.mapping(x, self.config_dict['eta_i'], self.current_beta)
        f0, dJ_du = self.opt_problem([mapped_x])
            
        elapsed = time.time() - start_time

        if grad.size > 0:
            gradient = tensor_jacobian_product(self.mapping, 0)(
                x, self.config_dict['eta_i'], self.current_beta, dJ_du
            )
            grad[:] = gradient
            if mp.am_master():
                print(f"Iter {self.cur_iter[0]} | Beta {self.current_beta:.2f} | "
                      f"FOM: {-f0:.6f} | Grad Norm: {np.linalg.norm(grad):.6e}")

        current_FOM = -float(f0)
        self.history_FOM.append(current_FOM)

        
            
        current_overlap = self.opt_problem.field_cache.get('overlap_abs2', float('nan'))
        self.history_overlap.append(current_overlap)
        current_purity = self.opt_problem.field_cache.get('purity', float('nan'))
        self.history_purity.append(current_purity)
        
        # best iter for each beta
        if current_FOM > self.best_snapshot['fom']:
            self.best_snapshot['x']       = x.copy()
            self.best_snapshot['mapped_x']= mapped_x.copy()
            self.best_snapshot['fom']     = current_FOM
            self.best_snapshot['iter']    = self.cur_iter[0]
            self.best_snapshot['overlap'] = current_overlap
            self.best_snapshot['purity']  = current_purity

            if mp.am_master():
                near_cached = self.opt_problem.field_cache.get('near_fields')
                ff_cached   = self.opt_problem.field_cache.get('ff_fields')
                self.best_snapshot['near_fields'] = (
                    {k: v.copy() for k, v in near_cached.items()} if near_cached else None
                )
                self.best_snapshot['ff_fields'] = (
                    {k: v.copy() for k, v in ff_cached.items()} if ff_cached else None
                )
            
        if mp.am_master():
            utils.append_csv(self.obj_csv_path,
                             [self.cur_iter[0], self.current_beta, current_purity, current_overlap, current_FOM])
            print(f"Iter {self.cur_iter[0]} | Beta {self.current_beta:.2f} | Purity: {current_purity:.6f} "
                  f"Overlap_abs2: {current_overlap} | (Best FoM: {max(self.history_FOM):.6f})")
            print(f'Time: {elapsed:.2f}s')

        return float(f0)

    def optimize(self, x_init, beta_schedule, nlopt_params):
        x = x_init.copy()

        for beta in beta_schedule:
            self.current_beta = beta
            self.best_fom_this_beta = -np.inf
            self.best_x_this_beta = None

            self.best_snapshot = {
                'x'               : None,
                'mapped_x'        : None,
                'fom'             : -np.inf,
                'iter'            : None,
                'near_fields'     : None,
                'ff_fields'       : None,
                'overlap'         : None,
                'purity'          : None,
            }


            
            if mp.am_master():
                print(f"\n--- Starting Beta Stage: {beta} ---")

            solver = nlopt.opt(nlopt_params['algorithm'], len(x))
            solver.set_min_objective(self.objective)
            #solver.set_ftol_rel(nlopt_params['ftol'])

            if beta < 32.0:
                current_maxeval = 12
            elif 32.0 <= beta <= 1024.0:
                current_maxeval = 1
            else:
                current_maxeval = nlopt_params['update_factor']
            solver.set_maxeval(current_maxeval)
            
            solver.set_lower_bounds(nlopt_params['lb'])
            solver.set_upper_bounds(nlopt_params['ub'])

            try:
                x = solver.optimize(x)
            except nlopt.RoundoffLimited:
                if mp.am_master():
                    print("NLopt: Roundoff limited, moving to next stage.")
            except nlopt.ForcedStop:
                if mp.am_master():
                    print("NLopt: Forced stop.")

            self.beta_checkpoints.append(self.cur_iter[0])

            # 直接從最佳快照提取數據，完全不需重跑模擬
            snap        = self.best_snapshot
            best_x      = snap['x'] if snap['x'] is not None else x
            mapped_x    = snap['mapped_x']
            near_fields = snap['near_fields']
            ff_fields   = snap['ff_fields']
            best_iter   = snap['iter']
            
            # use best iter for plotting
            #best_x = self.best_x_this_beta if self.best_x_this_beta is not None else x
            #mapped_x = self.mapping(best_x, self.config_dict['eta_i'], beta)

            # 下個 beta 階段從本次最理想的解出發
            x = best_x.copy()
            
            #mapped_x = self.mapping(x, self.config_dict['eta_i'], beta)
            #ff_fields, near_fields = self._get_near_fields_and_farfields(mapped_x)

            
            if mp.am_master() and (mapped_x is not None):

                # 只有 Master 核心繪圖前才進行 2D 變形，防止手性圖因為 1D 陣列而噴錯
                if ff_fields is not None:
                    ff_res = self.config_dict['ff_res']
                    ff_fields = {k: v.reshape(ff_res, ff_res) for k, v in ff_fields.items()}
                    
                # 1. 存結構數據
                utils.save_structure_data(self.cfg.dir_path, best_iter, beta, best_x)

                # 2. 結構圖
                utils.plot_design(
                    plot_sim=self.plot_sim,
                    design_variables=self.design_var,
                    mapped_x=mapped_x,
                    Nx=self.Nx,
                    Ny=self.Ny,
                    iters=best_iter,
                    beta=beta,
                    dir_path=self.cfg.dir_path,
                    design_center=self.design_center,
                    design_size=self.design_size,
                    opt_problem=self.opt_problem
                )
                print(f'plot_design done. iters={best_iter}')
                
                # 3. 近場相位圖（數據已由所有 rank 取出，這裡只畫圖）
                utils.plot_phase_analysis(
                    near_fields=near_fields,
                    iter_num=best_iter,
                    beta=beta,
                    dir_path=self.cfg.dir_path,
                    design_size=self.design_size,
                )
                print(f'plot_phase_analysis done. iters={best_iter}')
                

                utils.plot_near_chirality(
                        near_fields=near_fields,
                        iter_num=best_iter,
                        beta=beta,
                        dir_path=self.cfg.dir_path,
                        cfg=self.config_dict
                    )
                print(f'plot_near_chirality done. iters={best_iter}')
                
                    # 4. 遠場圖
                utils.plot_farfield_analysis(
                    ff_fields=ff_fields,
                    iter_num=best_iter,
                    beta=beta,
                    dir_path=self.cfg.dir_path,
                    cfg=self.config_dict
                )
                print(f'plot_farfield_analysis done. iters={best_iter}')
                
                # 遠場手性密度圖
                utils.plot_ff_chirality(
                    ff_fields=ff_fields,
                    iter_num=best_iter,
                    beta=beta,
                    dir_path=self.cfg.dir_path,
                    cfg=self.config_dict
                )
                print(f'plot_ff_chirality done. iters={best_iter}')
                # 空間手性傳播圖（ASM 角譜法）
                if near_fields is not None:
                    utils.plot_chirality_propagation(
                        near_fields=near_fields,
                        iter_num=best_iter,
                        beta=beta,
                        dir_path=self.cfg.dir_path,
                        cfg=self.config_dict,
                        n_slices=2
                    )
                    
                winding = utils.plot_phase_winding(
                    ff_fields=ff_fields,
                    iter_num=best_iter,
                    beta=beta,
                    dir_path=self.cfg.dir_path,
                    cfg=self.config_dict,                  # 移除 design_size=self.design_size
                    l_charge=self.config_dict['l_charge'],
                    r_fraction=None                        # 建議改為 None，讓程式自動精準追蹤遠場強度峰值 (50.61%)
                )
                print(f'Far-Field Phase winding(LCP) = {winding:.3f} × 2π (expected = {self.config_dict["l_charge"]})')
                
                print(f"Beta {beta} finished. Best FoM: {snap['fom']:.6f} when iter = {best_iter}")

        if mp.am_master():
            print("\nOptimization Finished.")
            utils.save_npy(self.cfg.dir_path, "final_purity_history.npy",
                           np.array(self.history_purity))
            utils.plot_purity_history(self.history_purity, self.beta_checkpoints,
                                      self.cfg.dir_path)
            
            utils.save_npy(self.cfg.dir_path, "final_overlap_abs2_history.npy",
                           np.array(self.history_overlap))
            utils.plot_overlap_history(self.history_overlap, self.beta_checkpoints,
                                      self.cfg.dir_path)
            
            utils.save_npy(self.cfg.dir_path, "final_FoM_history.npy",
                           np.array(self.history_FOM))
            utils.plot_FOM_history(self.history_FOM, self.beta_checkpoints,
                                      self.cfg.dir_path)#utils.py

import matplotlib
matplotlib.use('Agg') # 確保在無介面環境下不報錯
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import csv
import meep as mp
from scipy.special import genlaguerre


plt.rcParams.update({
    'font.size': 16,           # 標準字體
    'axes.titlesize': 18,      # 子圖標題 (Axes title)
    'axes.labelsize': 16,      # 座標軸標籤
    'xtick.labelsize': 14,     # 座標刻度
    'ytick.labelsize': 14,
    'legend.fontsize': 14,
    'figure.titlesize': 18,    # 總標題 (Figure suptitle)
    'figure.figsize': (10, 10), # 統一畫布比例
    'figure.dpi': 150,          # 統一解析度
    'lines.marker': 'o',
    'lines.linestyle': '--'
})
# === 基礎存檔功能 ===
def save_npy(dir_path, filename, data):
    """通用的 .npy 存檔函式"""
    os.makedirs(dir_path, exist_ok=True)
    full_path = os.path.join(dir_path, filename)
    np.save(full_path, data)

def init_csv(filepath, header):
    """初始化 CSV 檔案 (寫入標頭)"""
    # 確保目錄存在
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

def append_csv(filepath, row_data):
    """附加一筆資料到 CSV"""
    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row_data)

def save_gradient_data(dir_path, iter_num, beta, component_name, data):
    """儲存梯度資料"""
    grad_path = os.path.join(dir_path, 'gradient_data')
    filename = f"gradient_{component_name}_iter_{iter_num:03d}_beta_{beta:.2f}.npy"
    save_npy(grad_path, filename, data)

def save_structure_data(dir_path, iter_num, beta, data):
    """儲存結構設計參數"""
    beta_path = os.path.join(dir_path, 'beta_data')
    filename = f"structure_iter_{iter_num:03d}_beta_{beta:.2f}.npy"
    save_npy(beta_path, filename, data)

def save_history_arrays(dir_path, history):
    """儲存優化歷史陣列"""
    save_npy(dir_path, "evaluation_history.npy", np.array(history, dtype=object))

# === 繪圖功能 ===

def plot_design(plot_sim, design_variables, mapped_x, Nx, Ny, iters, beta, dir_path, design_center, design_size, opt_problem):
    """
    繪製當前設計結構圖。
    注意：這裡會暫時覆蓋 design_variables 的權重以進行繪圖。
    """
    
    # 1. 計算並顯示二值化比例 (Run1 風格)
    binary_ratio = np.sum((mapped_x < 0.1) | (mapped_x > 0.9)) / len(mapped_x) * 100
    if mp.am_master():
        print(f" Binary ratio: {binary_ratio:.1f}% (< 0.1 or > 0.9)")

    # 2. 重塑形狀並更新 MaterialGrid 權重
    # solver.py 中 MaterialGrid 是 (Nx, Ny, 1)，需對應 reshape
    try:
        mapped_x_reshaped = mapped_x.reshape(Nx, Ny, 1)
    except ValueError:
        # 容錯處理，若原本非 3D Grid
        mapped_x_reshaped = mapped_x.reshape(Nx, Ny)
        print(f"Warning: Reshaped mapped_x to ({Nx}, {Ny}) instead of ({Nx}, {Ny}, 1)")

    # 直接設定 weights，這是最準確反映 mapped_x 的方式
    design_variables.weights = mapped_x_reshaped


    # 3. 設定繪圖參數 (Run1 風格)
    fig = plt.figure()
    ax = plt.gca()
    
    # 提取寬高 (design_size 是 mp.Vector3)
    d_width = design_size.x
    d_height = design_size.y

    # 4. 執行 Plot2D
    # 關鍵：關閉 sources, monitors, boundaries 以獲得乾淨的結構圖
    if mp.am_master():
        plot_sim.plot2D(
            ax=ax,
            plot_sources_flag=False,
            plot_monitors_flag=False,
            plot_boundaries_flag=False,
            output_plane=mp.Volume(center=design_center, size=mp.Vector3(d_width, d_height, 0))
        )
        
        # 5. 標題與存檔 (Run1 風格)
        plt.title(f"Iteration={iters:03d}, Beta={beta:.2f}") # 移除小數點格式，除非 beta 是 float
        plt.axis('off')
        plt.tight_layout()
        
        beta_path = os.path.join(dir_path, 'beta_data')
        os.makedirs(beta_path, exist_ok=True)
        
        # 檔名格式對齊 run1.py: structure_iter_{:03d}_beta_{:.2f}.png
        save_filename = f"structure_iter_{iters:03d}_beta_{beta:.2f}.png"
        plt.savefig(os.path.join(beta_path, save_filename), dpi=200, bbox_inches='tight')
        plt.close(fig)

def plot_phase_winding(ff_fields, iter_num, beta, dir_path, cfg, l_charge, n_points=360, r_fraction=None):
    """沿圓環提取遠場 LCP 相位，並計算拓撲繞數 (Winding Number)"""
    from scipy.ndimage import map_coordinates

    # 1. 讀取遠場定義參數
    w0_radius = cfg['w0_radius']   # 遠場傳播後的束腰半徑
    ff_width  = cfg['ff_width']    # 遠場監視器的實體總寬度
    ff_res    = cfg['ff_res']      # 遠場解析度像素數
    
    r_max = ff_width / 2.0
    
    # 2. 計算遠場 LG 模態之理論強度最大值半徑 (r_peak)
    if r_fraction is None:
        if l_charge == 0:
            r_fraction = 0.2  # l=0 中心點，取小半徑環
        else:
            r_peak = w0_radius * np.sqrt(abs(l_charge) / 2)
            r_fraction = min(r_peak / r_max, 0.85)
    
    r_phys = r_fraction * r_max
    
    # 3. 提取並重塑遠場 2D 數據
    ff_Ex = np.asarray(ff_fields['Ex'], dtype=complex).reshape(ff_res, ff_res)
    ff_Ey = np.asarray(ff_fields['Ey'], dtype=complex).reshape(ff_res, ff_res)
    
    # 計算遠場像素間距與中心點
    dx = ff_width / ff_res
    dy = ff_width / ff_res
    cx, cy = ff_res / 2.0, ff_res / 2.0
    
    r_px_x = r_phys / dx
    r_px_y = r_phys / dy
    
    # 4. 圓環路徑抽樣點 (x 軸對應第 0 軸，y 軸對應第 1 軸)
    phi_arr = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    sample_x = cx + r_px_x * np.cos(phi_arr)
    sample_y = cy + r_px_y * np.sin(phi_arr)
    
    # 雙線性內插遠場分量
    ex = map_coordinates(ff_Ex.real, [sample_x, sample_y], order=1) + 1j * map_coordinates(ff_Ex.imag, [sample_x, sample_y], order=1)
    ey = map_coordinates(ff_Ey.real, [sample_x, sample_y], order=1) + 1j * map_coordinates(ff_Ey.imag, [sample_x, sample_y], order=1)
    
    # 5. 投影至目標 LCP 基底
    e_lcp = ((ex + ey) / np.sqrt(2)).T
    phase_raw = np.angle(e_lcp)
    phase_unwrapped = np.unwrap(phase_raw)
    
    total_winding = (phase_unwrapped[-1] - phase_unwrapped[0]) / (2 * np.pi)
    
    # 6. 繪圖與儲存
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    fig.suptitle(f"Far-Field Phase Winding | Iter={iter_num}, Beta={beta:.2f} |\n"
                 f"r={r_phys:.2f}μm | Expected ell={l_charge}")

    phi_deg = np.degrees(phi_arr)

    # 左圖：Wrapped Phase
    axes[0].plot(phi_deg, phase_raw, color='steelblue', linewidth=1.5)
    axes[0].set_xlabel("φ (deg)")
    axes[0].set_ylabel("Phase (rad)")
    axes[0].set_title("Wrapped phase")
    axes[0].set_xlim(0, 360)
    axes[0].set_xticks([0, 90, 180, 270, 360])
    axes[0].axhline(np.pi, color='gray', linestyle='--', linewidth=0.8)
    axes[0].axhline(-np.pi, color='gray', linestyle='--', linewidth=0.8)

    # 右圖：Unwrapped Phase 疊加理想直線
    axes[1].plot(phi_deg, phase_unwrapped, color='coral', linewidth=1.0, label='Simulated')
    ideal = l_charge * np.radians(phi_deg) + phase_unwrapped[0]
    axes[1].plot(phi_deg, ideal, color='black', linestyle='--', linewidth=1.0,
                 label=f'Ideal ell={l_charge}')
    axes[1].set_xlabel("φ (deg)")
    axes[1].set_ylabel("Phase (rad)")
    axes[1].set_title(f"Unwrapped | Total winding = {total_winding:.2f} × 2π")
    axes[1].set_xlim(0, 360)
    axes[1].set_xticks([0, 90, 180, 270, 360])
    axes[1].legend()

    plt.tight_layout()

    winding_path = os.path.join(dir_path, 'farfield_phase_winding')
    os.makedirs(winding_path, exist_ok=True)
    save_path = os.path.join(winding_path,
                             f"ff_winding_iter_{iter_num:03d}_beta_{beta:.2f}_rfraction_{r_fraction:.4f}.png")
    plt.savefig(save_path, bbox_inches='tight', dpi=200)
    plt.close(fig)

    return total_winding


def plot_phase_analysis(near_fields, iter_num, beta, dir_path, design_size):
    """接收數據並使用 show 函數進行繪圖"""

    ex_data = near_fields['Ex']
    ey_data = near_fields['Ey']
    
    # 1. 數據計算
    e_lcp = ((ex_data + ey_data) / np.sqrt(2)).T
    e_rcp = ((ex_data - ey_data) / np.sqrt(2)).T
    fields = {
        'LCP': e_lcp,
        'RCP': e_rcp,
    }

    # 2. 畫布與範圍設定
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle(f"Near-Field | Iter={iter_num}, Beta={beta:.2f}")
    extent = [-design_size.x/2, design_size.x/2, -design_size.y/2, design_size.y/2]

    phase_kw = dict(cmap='twilight_shifted', vmin=-np.pi, vmax=np.pi)
    # 3. 定義內部輔助函數（確保能存取 fig 和 extent）
    def show(ax, data, title, cmap='inferno', **kw):
        im = ax.imshow(data, cmap=cmap, extent=extent,
                       origin='lower', aspect='equal', **kw)
        ax.set_title(title)
        ax.set_xlabel("x (μm)")
        ax.set_ylabel("y (μm)")
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        # 若偵測到相位範圍，則設定特殊刻度
        if 'vmin' in kw and np.isclose(kw['vmin'], -np.pi):
            cbar.set_ticks([-np.pi, 0, np.pi])
            cbar.set_ticklabels([r'$-\pi$', '0', r'$\pi$'])

    # 4. 迴圈呼叫 show 繪製強度與相位
    for i, (name, field) in enumerate(fields.items()):
        show(axes[i, 0], np.angle(field), f"(Phase){name}", **phase_kw)
        intensity = np.abs(field)**2
        max_val = intensity.max()
        intensity_norm = intensity / (max_val + 1e-30)
        show(axes[i, 1], intensity_norm, f"|{name}|² (Norm. Intensity)", vmin=0, vmax=1)
        
    # 5. 排版與存檔
    plt.tight_layout()
    phase_path = os.path.join(dir_path, 'phase_analysis')
    os.makedirs(phase_path, exist_ok=True)
    
    save_filename = f"phase_iter_{iter_num:03d}_beta_{beta:.2f}.png"
    plt.savefig(os.path.join(phase_path, save_filename), dpi=200, bbox_inches='tight')
    plt.close(fig)

def plot_farfield_analysis(ff_fields, iter_num, beta, dir_path, cfg):
    """
    ex_ff, ey_ff: shape (ff_res, ff_res)，x 為第 0 軸
    需轉置後給 imshow（imshow 慣例是 [row=y, col=x]）
    """
    #print(f'  [FF debug] ff_Ex type={type(ff_Ex)}, ff_Ey type={type(ff_Ey)}')
    #if ff_Ex is not None:
    #    print(f'  [FF debug] ff_Ex dtype={getattr(ff_Ex, "dtype", "N/A")}, shape={getattr(ff_Ex, "shape", "N/A")}')

    #if ff_Ex is None or ff_Ey is None:
    #    print('  [FF debug] ff_Ex or ff_Ey is None, skipping plot')
    #    return
    ff_Ex = ff_fields['Ex']
    ff_Ey = ff_fields['Ey']

    ff_Ex = np.asarray(ff_Ex, dtype=complex)
    ff_Ey = np.asarray(ff_Ey, dtype=complex)
    
    ff_width = cfg['ff_width']
    ff_res = cfg['ff_res']
    extent   = [-ff_width/2, ff_width/2, -ff_width/2, ff_width/2]

    ff_Ex = ff_Ex.reshape(ff_res, ff_res)
    ff_Ey = ff_Ey.reshape(ff_res, ff_res)
    
    x_ff = np.linspace(-ff_width/2, ff_width/2, ff_res)
    y_ff = np.linspace(-ff_width/2, ff_width/2, ff_res)
    
    X_flat = np.array([x for x in x_ff for y in y_ff])
    Y_flat = np.array([y for x in x_ff for y in y_ff])

    dx = ff_width / (ff_res - 1) if ff_res > 1 else 0
    dy = dx
    area = dx * dy

    zR          = cfg['zR']    
    z_ff_total  = cfg['z_ff_total']
    k           = 2 * np.pi / cfg['wavelength']
    l_charge    = cfg['l_charge']
    p_radial    = cfg['p_radial']
    w0_radius   = cfg['w0_radius']
    

    rho = np.sqrt(X_flat**2 + Y_flat**2)
    phi = np.arctan2(Y_flat, X_flat)

    term1 = (np.sqrt(2) * rho / w0_radius) ** np.abs(l_charge)
    term2 = np.exp(-(rho**2) / (w0_radius**2))

    Lpl = genlaguerre(p_radial, np.abs(l_charge))
    laguerre_term = Lpl(2 * rho**2 / w0_radius**2)

    azimuthal_phase = np.exp(1j * l_charge * phi)

    Rz = z_ff_total * (1 + (zR / z_ff_total)**2)
    curvature_phase = np.exp(1j * k * (rho**2) / (2 * Rz))
    
    gouy_value = (2 * p_radial + np.abs(l_charge) + 1) * np.arctan(z_ff_total / zR)
    gouy_phase = np.exp(-1j *gouy_value)
    
    LG_profile = term1 * term2 * laguerre_term * azimuthal_phase * curvature_phase * gouy_phase


    E_target_x_raw = LG_profile / np.sqrt(2)
    E_target_y_raw = 1j * LG_profile / np.sqrt(2)
    
    power_target_raw = np.sum(np.abs(E_target_x_raw)**2 + np.abs(E_target_y_raw)**2) * area
    
    E_target_x = E_target_x_raw / np.sqrt(power_target_raw)
    E_target_y = E_target_y_raw / np.sqrt(power_target_raw)
    power_target = 1.0


    # Purity
    overlap = np.sum(ff_Ex.flatten() * np.conj(E_target_x) + ff_Ey.flatten() * np.conj(E_target_y)) * area
    power_sim = np.sum(np.abs(ff_Ex)**2 + np.abs(ff_Ey)**2) * area

    purity = (np.abs(overlap)**2) / (power_sim * power_target + 1e-30)
    overlap_abs2 = np.abs(overlap)**2

    E_target_x_2d = E_target_x.reshape(ff_res, ff_res)
    E_target_y_2d = E_target_y.reshape(ff_res, ff_res)

    # Phase
    sim_phase = (ff_Ex + ff_Ey).T
    target_phase = (E_target_x_2d + E_target_y_2d).T

    #Intensity
    sim_intensity = (np.abs(ff_Ex)**2 + np.abs(ff_Ey)**2).T
    target_intensity = (np.abs(E_target_x_2d)**2 + np.abs(E_target_y_2d)**2).T
    
    # 繪圖
    fig, axes = plt.subplots(2, 2, figsize=(9, 9))
    fig.suptitle(f"Far-Field  |  Iter={iter_num}, Beta={beta:.2f}, Purity={purity*100:.2f}%, Overlap_abs2={overlap_abs2:.2f}")
    phase_kw = dict(cmap='twilight_shifted', vmin=-np.pi, vmax=np.pi)

    def show(ax, data, title, cmap='inferno', **kw):
        """
        預設繪製強度圖（inferno），若傳入 vmin/vmax（如 phase_kw）則處理為相位圖刻度。
        """
        im = ax.imshow(data, cmap=cmap, extent=extent,
                       origin='lower', aspect='equal', **kw)
        ax.set_title(title)
        ax.set_xlabel("x (μm)")
        ax.set_ylabel("y (μm)")
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        if 'vmin' in kw and np.isclose(kw['vmin'], -np.pi):
            cbar.set_ticks([-np.pi, 0, np.pi])
            cbar.set_ticklabels([r'$-\pi$', '0', r'$\pi$'])

    show(axes[0,0], np.angle(sim_phase), "Sim Phase", **phase_kw)
    show(axes[0,1], sim_intensity, "Sim Intensity")

    show(axes[1,0], np.angle(target_phase),  f"Target LG(l={l_charge}) Phase", **phase_kw)
    show(axes[1,1], target_intensity, f"Target LG(l={l_charge}) Intensity")

    plt.tight_layout()
    ff_path = os.path.join(dir_path, 'farfield_analysis')
    os.makedirs(ff_path, exist_ok=True)
    save_path = os.path.join(ff_path, f"ff_iter_{iter_num:03d}_beta_{beta:.2f}.png")
    plt.savefig(save_path, bbox_inches='tight', dpi=200)
    plt.close(fig)
    
def plot_purity_history(history, beta_checkpoints, dir_path):
    """
    繪製 Purity 優化曲線：包含原始震盪數據與階梯狀的最佳值曲線
    """
    if not history:
        print("No history to plot.")
        return

    # 轉為 numpy array 方便計算
    history_arr = np.array(history)
    iterations = np.arange(1, len(history_arr) + 1)
    
    # 計算階梯狀的最佳值 (Best-so-far)
    # np.maximum.accumulate 會回傳一個陣列，第 i 個元素是前 i 個元素中的最大值
    best_so_far = np.maximum.accumulate(history_arr)

    # 準備繪圖
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 1. 畫原始數據 (Raw Detail) 
    ax.plot(iterations, history_arr, color='tab:blue', linewidth=1.5, alpha=0.7, label='Raw Iterations')
    
    # 2. 畫階梯狀最佳值 (Staircase) - 使用深色，顯示實際進步
    ax.plot(iterations, best_so_far, color='tab:red', linewidth=1.0, label='Best Purity (So far)')
    
    # 標註最終數值
    final_best = best_so_far[-1]
    ax.text(iterations[-1], final_best, f"{final_best*100:.2f}%",  verticalalignment='bottom', horizontalalignment='right', 
            color='tab:blue', fontweight='bold')

    ax.set_xlabel('Iteration')
    ax.set_ylabel(r'$\text{Purity}$')
    ax.set_title('Optimization History: Target LG Mode Purity')
    
    if beta_checkpoints:
        for cp in beta_checkpoints[:-1]: # 最後一個點是結尾，通常不需劃線
            # marker=None: 代表「不指定」
            # marker='None' or '': 代表「明確指定為無 marker」
            
            ax.axvline(x=cp, color='purple', linestyle='-', linewidth=2.0, alpha=0.7, marker='None', label='Beta Switch' if cp == beta_checkpoints[0] else "")
            
    ax.margins(x=0)
    ax.grid(True, alpha=0.5, linestyle='--')
    ax.legend(loc='lower right')
    
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # 存檔
    output_path = os.path.join(dir_path, "purity_history_staircase.png")
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close(fig)


    # 額外存一份 CSV 包含這兩組數據，方便你後續用 Origin 或 Matlab 畫圖
    df = pd.DataFrame({
        "Iteration": iterations,
        "Raw_Purity": history_arr,
        "Best_So_Far": best_so_far
    })
    csv_path = os.path.join(dir_path, "purity_history_full.csv")
    df.to_csv(csv_path, index=False)

def plot_overlap_history(history, beta_checkpoints, dir_path):
    """
    繪製 overlap 優化曲線：包含原始震盪數據與階梯狀的最佳值曲線
    """
    if not history:
        print("No history to plot.")
        return

    # 轉為 numpy array 方便計算
    history_arr = np.array(history)
    iterations = np.arange(1, len(history_arr) + 1)
    
    # 計算階梯狀的最佳值 (Best-so-far)
    # np.maximum.accumulate 會回傳一個陣列，第 i 個元素是前 i 個元素中的最大值
    best_so_far = np.maximum.accumulate(history_arr)

    # 準備繪圖
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 1. 畫原始數據 (Raw Detail) 
    ax.plot(iterations, history_arr, color='tab:blue', linewidth=1.5, alpha=0.7, label='Raw Iterations')
    
    # 2. 畫階梯狀最佳值 (Staircase) - 使用深色，顯示實際進步
    ax.plot(iterations, best_so_far, color='tab:red', linewidth=1.0, label='Best Overlap_abs2 (So far)')
    
    # 標註最終數值
    final_best = best_so_far[-1]
    ax.text(iterations[-1], final_best, f"{final_best:.2f}",  verticalalignment='bottom', horizontalalignment='right', 
            color='tab:blue', fontweight='bold')

    ax.set_xlabel('Iteration')
    ax.set_ylabel(r'$\text{Overlap}^2$')
    ax.set_title('Optimization History: Target LG Mode Overlap_abs2')
    
    if beta_checkpoints:
        for cp in beta_checkpoints[:-1]: # 最後一個點是結尾，通常不需劃線
            # marker=None: 代表「不指定」
            # marker='None' or '': 代表「明確指定為無 marker」
            
            ax.axvline(x=cp, color='purple', linestyle='-', linewidth=2.0, alpha=0.7, marker='None', label='Beta Switch' if cp == beta_checkpoints[0] else "")
            
    ax.margins(x=0)
    ax.grid(True, alpha=0.5, linestyle='--')
    ax.legend(loc='lower right')
    
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # 存檔
    output_path = os.path.join(dir_path, "Overlap_abs2_history_staircase.png")
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close(fig)


    # 額外存一份 CSV 包含這兩組數據，方便你後續用 Origin 或 Matlab 畫圖
    df = pd.DataFrame({
        "Iteration": iterations,
        "Overlap_Abs2": history_arr,
        "Best_So_Far": best_so_far
    })
    csv_path = os.path.join(dir_path, "Overlap_abs2_history_full.csv")
    df.to_csv(csv_path, index=False)


def plot_FOM_history(history, beta_checkpoints, dir_path):
    """
    繪製 overlap 優化曲線：包含原始震盪數據與階梯狀的最佳值曲線
    """
    if not history:
        print("No history to plot.")
        return

    # 轉為 numpy array 方便計算
    history_arr = np.array(history)
    iterations = np.arange(1, len(history_arr) + 1)
    
    # 計算階梯狀的最佳值 (Best-so-far)
    # np.maximum.accumulate 會回傳一個陣列，第 i 個元素是前 i 個元素中的最大值
    best_so_far = np.maximum.accumulate(history_arr)

    # 準備繪圖
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 1. 畫原始數據 (Raw Detail) 
    ax.plot(iterations, history_arr, color='tab:blue', linewidth=1.5, alpha=0.7, label='Raw Iterations')
    
    # 2. 畫階梯狀最佳值 (Staircase) - 使用深色，顯示實際進步
    ax.plot(iterations, best_so_far, color='tab:red', linewidth=1.0, label='Best FOM (So far)')
    
    # 標註最終數值
    final_best = best_so_far[-1]
    ax.text(iterations[-1], final_best, f"{final_best:.2f}",  verticalalignment='bottom', horizontalalignment='right', 
            color='tab:blue', fontweight='bold')

    ax.set_xlabel('Iteration')
    ax.set_ylabel(r'FOM')
    ax.set_title('Optimization History: Target LG Mode FOM')
    
    if beta_checkpoints:
        for cp in beta_checkpoints[:-1]: # 最後一個點是結尾，通常不需劃線
            # marker=None: 代表「不指定」
            # marker='None' or '': 代表「明確指定為無 marker」
            
            ax.axvline(x=cp, color='purple', linestyle='-', linewidth=2.0, alpha=0.7, marker='None', label='Beta Switch' if cp == beta_checkpoints[0] else "")
            
    ax.margins(x=0)
    ax.grid(True, alpha=0.5, linestyle='--')
    ax.legend(loc='lower right')
    
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # 存檔
    output_path = os.path.join(dir_path, "FOM_history_staircase.png")
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close(fig)


    # 額外存一份 CSV 包含這兩組數據，方便你後續用 Origin 或 Matlab 畫圖
    df = pd.DataFrame({
        "Iteration": iterations,
        "FOM": history_arr,
        "Best_So_Far": best_so_far
    })
    csv_path = os.path.join(dir_path, "FOM_history_full.csv")
    df.to_csv(csv_path, index=False)


def plot_near_chirality(near_fields, iter_num, beta, dir_path, cfg):
    """
    繪製遠場手性密度圖，風格與 plot_farfield_analysis 一致
    """
    c = 1.0 
    f = cfg['frequency']
    coeff = (np.pi * f) / (c**2)
    c_vac = coeff * 1.0

    
    design_width = cfg['design_width']
    extent   = [-design_width/2, design_width/2, -design_width/2, design_width/2]

    # 轉置：(x, y) → (y, x) 配合 imshow（與 plot_farfield_test 一致）

    dot = (np.conj(near_fields['Ex']) * near_fields['Hx'] + 
           np.conj(near_fields['Ey']) * near_fields['Hy'] + 
           np.conj(near_fields['Ez']) * near_fields['Hz'])

    # 3. 應用於 Zilch 計算
    # C = chirality_coeff * Im(E* · H)

    c_data = coeff * (np.imag(dot)).T
    c_total = np.abs(c_data)
    g_factor = c_total / c_vac

    avg_g = np.mean(g_factor)
    if mp.am_master():
        print(f"  [Chirality] Avg Enhancement g: {avg_g:.2f}")
        
    # 正規化（方便比較不同 iter 之間的相對分佈）
    max_abs = np.max(np.abs(c_data)) + 1e-30
    c_norm = c_data / max_abs

    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    fig.suptitle(f"Near-Field Chirality | Iter={iter_num}, Beta={beta:.2f}")

    def show(ax, data, title, cmap='RdBu', **kw):
        im = ax.imshow(data, cmap=cmap, extent=extent,
                       origin='lower', aspect='equal', **kw)
        ax.set_title(title)
        ax.set_xlabel("x (μm)")
        ax.set_ylabel("y (μm)")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    show(axes[0], c_data,  "C (raw)",        vmin=-max_abs, vmax=max_abs)
    show(axes[1], c_norm,  "C (normalized)", vmin=-1, vmax=1)

    plt.tight_layout()
    save_dir = os.path.join(dir_path, 'chirality_near_analysis')
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, f"near_chirality_{iter_num:03d}_beta_{beta:.2f}.png"),
                dpi=200, bbox_inches='tight')
    plt.close(fig)

    
def plot_ff_chirality(ff_fields, iter_num, beta, dir_path, cfg):
    """
    繪製遠場手性密度圖，風格與 plot_farfield_analysis 一致
    """
    c = 1.0 
    f = cfg['frequency']
    coeff = (np.pi * f) / (c**2)
    
    ff_width = cfg['ff_width']
    extent   = [-ff_width/2, ff_width/2, -ff_width/2, ff_width/2]

    # 轉置：(x, y) → (y, x) 配合 imshow（與 plot_farfield_test 一致）

    dot = (np.conj(ff_fields['Ex']) * ff_fields['Hx'] + np.conj(ff_fields['Ey']) * ff_fields['Hy'] + np.conj(ff_fields['Ez']) * ff_fields['Hz'])

    # 3. 應用於 Zilch 計算
    # C = chirality_coeff * Im(E* · H)

    c_data = coeff * (np.imag(dot)).T

    # 正規化（方便比較不同 iter 之間的相對分佈）
    max_abs = np.max(np.abs(c_data)) + 1e-30
    c_norm = c_data / max_abs

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(f"Far-Field Chirality | Iter={iter_num}, Beta={beta:.2f}")

    def show(ax, data, title, cmap='RdBu', **kw):
        im = ax.imshow(data, cmap=cmap, extent=extent,
                       origin='lower', aspect='equal', **kw)
        ax.set_title(title)
        ax.set_xlabel("x (μm)")
        ax.set_ylabel("y (μm)")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    show(axes[0], c_data,  "C (raw)",        vmin=-max_abs, vmax=max_abs)
    show(axes[1], c_norm,  "C (normalized)", vmin=-1, vmax=1)

    plt.tight_layout()
    save_dir = os.path.join(dir_path, 'chirality_ff_analysis')
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, f"ff_chirality_{iter_num:03d}_beta_{beta:.2f}.png"),
                dpi=200, bbox_inches='tight')
    plt.close(fig)


def plot_chirality_propagation(near_fields, iter_num, beta, dir_path, cfg, n_slices=5):
    """
    用角譜法（ASM）從近場傳播到遠場，計算中間各 z 平面的手性密度分佈。
    完全基於已快取的 near_fields，不需重跑模擬。
    """
    if not mp.am_master():
        return

    import os
    import matplotlib.pyplot as plt

    f       = cfg['frequency']
    wl      = cfg['wavelength']
    k0      = 2 * np.pi / wl
    coeff   = (np.pi * f) / (1.0**2)

    dw      = cfg['design_width']
    ff_dist = cfg['far_field_distance']
    Nx_nf   = near_fields['Ex'].shape[0]
    Ny_nf   = near_fields['Ex'].shape[1]

    dx = dw / Nx_nf
    dy = dw / Ny_nf

    # 空間頻率網格
    kx = np.fft.fftfreq(Nx_nf, d=dx) * 2 * np.pi
    ky = np.fft.fftfreq(Ny_nf, d=dy) * 2 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    KZ2 = k0**2 - KX**2 - KY**2
    KZ  = np.where(KZ2 >= 0, np.sqrt(KZ2), 1j * np.sqrt(-KZ2))

    components = ['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz']

    # 對每個分量做 FFT
    spectra = {}
    for comp in components:
        spectra[comp] = np.fft.fft2(near_fields[comp])

    z_slices = np.linspace(0, ff_dist, n_slices)

    fig, axes = plt.subplots(1, n_slices, figsize=(3 * n_slices, 3.5), sharey=True)
    fig.suptitle(f"Chirality Propagation (ASM) | Iter={iter_num}, Beta={beta:.2f}", y=1.05)

    extent = [-dw/2, dw/2, -dw/2, dw/2]

    for idx, dz in enumerate(z_slices):
        prop = np.exp(1j * KZ * dz)

        fields_z = {}
        for comp in components:
            fields_z[comp] = np.fft.ifft2(spectra[comp] * prop)  # 只做一次 ifft2

        dot = (np.conj(fields_z['Ex']) * fields_z['Hx'] +
               np.conj(fields_z['Ey']) * fields_z['Hy'] +
               np.conj(fields_z['Ez']) * fields_z['Hz'])
        c_data = coeff * np.imag(dot).T

        ax = axes[idx]
        max_abs = np.max(np.abs(c_data)) + 1e-30
        im = ax.imshow(c_data, cmap='RdBu', extent=extent,
                       origin='lower', vmin=-max_abs, vmax=max_abs)
        ax.set_title(f"Δz={dz:.2f}μm", fontsize=11)
        ax.set_xlabel("x (μm)", fontsize=10)
        if idx == 0:
            ax.set_ylabel("y (μm)", fontsize=10)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    plt.tight_layout()
    save_dir = os.path.join(dir_path, 'chirality_propagation')
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir,
                f"prop_chirality_{iter_num:03d}_beta_{beta:.2f}.png"),
                dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f'plot_chirality_propagation done. iters={iter_num}')