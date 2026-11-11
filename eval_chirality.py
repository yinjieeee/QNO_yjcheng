# eval_chirality.py
import os
import re
import numpy as np
import meep as mp
import meep.adjoint as mpa
import utils
import config as cfg
import models
import physics

def find_latest_structure(beta_data_dir):
    """
    掃描 beta_data 資料夾，找出 iter 數字最大的 structure_*.npy 檔案。
    並從檔名中解析出 iter_num 與 beta 值。
    """
    if not os.path.exists(beta_data_dir):
        raise FileNotFoundError(f"[Evaluator] 找不到目錄: {beta_data_dir}")

    candidates = [f for f in os.listdir(beta_data_dir) if 'structure_iter_' in f and f.endswith('.npy')]
    if not candidates:
        raise FileNotFoundError(f"[Evaluator] 在 {beta_data_dir} 找不到任何 structure_*.npy")
        
    # 根據 iter 排序 (假設檔名格式: structure_iter_010_beta_4.00.npy)
    def extract_iter(filename):
        match = re.search(r'iter_(\d+)', filename)
        return int(match.group(1)) if match else -1
        
    latest_file = max(candidates, key=extract_iter)
    full_path = os.path.join(beta_data_dir, latest_file)
    
    iter_num = extract_iter(latest_file)
    
    # 提取 beta 值

    beta_match = re.search(r'beta_([\d.]+)\.npy', latest_file)
    beta = float(beta_match.group(1)) if beta_match else 1.0
    
    return full_path, iter_num, beta

def run_chirality_analysis(dir_path, iter_num=None, beta=None, mapped_x=None, cfg_dict=None):
    """
    獨立的物理分析模組：執行正向模擬並繪製多高度手性傳播圖。
    - 若由 run.py 呼叫：直接使用傳入的 mapped_x, iter_num, beta。
    - 若獨立執行：自動從 beta_data 資料夾尋找最新結構並重新 Mapping。
    """
    if cfg_dict is None:
        cfg.update_config() # 確保路徑與參數已更新
        cfg_dict = {
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
            'minimum_length':     cfg.minimum_length # 加入 mapping 所需參數
        }

    freq      = cfg_dict['frequency']
    ff_width  = cfg_dict['ff_width']
    ff_res    = cfg_dict['ff_res']
    zR        = cfg_dict['zR']
    dw        = cfg_dict['design_width']
    dh        = cfg_dict['design_height']
    res       = cfg_dict['resolution']

    # 1. 處理輸入資料 (若獨立執行，需自行尋找與 Mapping)
    if mapped_x is None or iter_num is None or beta is None:
        beta_data_dir = os.path.join(dir_path, 'beta_data')
        if mp.am_master():
            print(f"[Evaluator] 獨立運行模式，開始掃描 {beta_data_dir} ...")
        
        try:
            npy_path, iter_num, beta = find_latest_structure(beta_data_dir)
        except FileNotFoundError as e:
            if mp.am_master():
                print(e)
            return

        if mp.am_master():
            print(f"[Evaluator] 找到最新結構: {os.path.basename(npy_path)} (Iter={iter_num}, Beta={beta})")
            
        x0 = cfg.load_structure_npy(npy_path)
        
        # 進行物理變換 (Mapping)
        filter_radius = mpa.get_conic_radius_from_eta_e(cfg_dict['minimum_length'], cfg_dict['eta_e'])
        mapping_func = physics.get_mapping(filter_radius, cfg)
        mapped_x = mapping_func(x0, cfg_dict['eta_i'], beta)

    save_dir = os.path.join(dir_path, 'chirality_propagation')
    if mp.am_master():
        os.makedirs(save_dir, exist_ok=True)
        print(f"\n[Evaluator] 開始執行手性傳播分析 (Iter={iter_num}, Beta={beta})...")
        

    prefix = utils.get_file_prefix(dir_path)
    cache_file = os.path.join(save_dir, f"{prefix}_n2f_fields_iter_{iter_num:03d}.npz")

    z_trans = np.arange(0, 0.95, 0.1)
    z_far   = np.arange(1, 11, 1)
    z_ratios = np.concatenate([z_trans, z_far])

    multi_z_fields = {}

    # ── 2. 檢查快取或執行模擬 ──
    if os.path.exists(cache_file):
        if mp.am_master():
            print(f"  [Evaluator] 讀取快取資料: {cache_file}")
            with np.load(cache_file) as data:
                for z_ratio in z_ratios:
                    z_key = f"{z_ratio:.1f}"
                    multi_z_fields[z_ratio] = {
                        'Ex': data[f"z{z_key}_Ex"], 'Ey': data[f"z{z_key}_Ey"], 'Ez': data[f"z{z_key}_Ez"],
                        'Hx': data[f"z{z_key}_Hx"], 'Hy': data[f"z{z_key}_Hy"], 'Hz': data[f"z{z_key}_Hz"]
                    }
    else:
        if mp.am_master():
            print(f"  [Evaluator] 無快取，開始建立 MEEP 實例並進行正向模擬 (zR={zR:.4f})...")
            
        # 重建場景
        scene = models.build_scene_data(cfg_dict)
        Nx = int(res * dw) + 1
        Ny = int(res * dh) + 1
        design_var = scene['geometry'][0].material
        
        # 確保 mapping 結果正確賦值
        shaped = mapped_x.reshape(Nx, Ny, 1)
        design_var.weights = shaped.astype(np.float64)

        sim = mp.Simulation(
            cell_size=scene['cell_size'],
            geometry=scene['geometry'],
            sources=scene['sources'],
            boundary_layers=scene['pml_layer'],
            resolution=res,
            default_material=mp.air,
            force_complex_fields=True,
            k_point=mp.Vector3(0, 0, 0)
        )

        monitor_z = scene['monitor_z']
        
        nf_dft = sim.add_dft_fields(
            [mp.Ex, mp.Ey, mp.Ez, mp.Hx, mp.Hy, mp.Hz],
            freq, freq, 1, center=mp.Vector3(0, 0, monitor_z), size=mp.Vector3(dw, dh, 0)
        )

        n2f_monitor = mp.Near2FarRegion(
            center=mp.Vector3(0, 0, monitor_z), size=mp.Vector3(dw, dh, 0), direction=mp.Z
        )
        n2f_obj = sim.add_near2far(freq, 0, 1, n2f_monitor)

        # 執行模擬 (MPI 集體操作)
        sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ex, mp.Vector3(), 1e-5))

        save_data = {}
        n2f_res = ff_res / ff_width

        for z_ratio in z_ratios:
            z_key = f"{z_ratio:.1f}"
            z_dist = z_ratio * zR
            
            if z_ratio == 0:
                # 讀取近場 (寫成單行避免括號遺漏)
                fields = {comp: sim.get_dft_array(nf_dft, getattr(mp, comp), 0).squeeze() for comp in ['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz']}
            else:
                # 讀取遠場
                ff_vol = mp.Volume(center=mp.Vector3(0, 0, monitor_z + z_dist), size=mp.Vector3(ff_width, ff_width, 0))
                raw_fields = sim.get_farfields(n2f_obj, n2f_res, where=ff_vol)
                
                # 防彈級擷取邏輯
                fields = {}
                comps = ['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz']
                for i, comp in enumerate(comps):
                    if isinstance(raw_fields, dict):
                        if comp in raw_fields:
                            arr = raw_fields[comp]
                        else:
                            arr = raw_fields[getattr(mp, comp)]
                    else:
                        arr = raw_fields[i]
                    fields[comp] = np.asarray(arr).squeeze()

            multi_z_fields[z_ratio] = fields
            
            if mp.am_master():
                for comp, arr in fields.items():
                    save_data[f"z{z_key}_{comp}"] = arr

        if mp.am_master():
            np.savez_compressed(cache_file, **save_data)
            print(f"  [Evaluator] 場數據 (完整 6 分量) 已快取至: {cache_file}")

    # ── 3. 呼叫 Utils 繪圖 ──
    if mp.am_master() and multi_z_fields:
        print("  [Evaluator] 開始繪製多高度手性傳播圖...")
        utils.plot_chirality_propagation(
            multi_z_fields,
            iter_num=iter_num,
            beta=beta,
            dir_path=dir_path,
            cfg=cfg_dict
        )
        print("  [Evaluator] 手性傳播分析完成！")

# 供命令列獨立執行的進入點
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="獨立執行手性傳播分析")
    parser.add_argument('--dir', type=str, required=True, help='專案資料夾路徑 (例如: ~/LG_WS2/test_0709)')
    parser.add_argument('--l_charge', type=int, default=None, help='手性拓撲荷數')
    args = parser.parse_args()
    
    # 初始化 MPI
    mp.verbosity(0)
    
    target_dir = os.path.expanduser(args.dir)
    cfg.dir_path = target_dir

    if args.l_charge is not None:
        cfg.l_charge = args.l_charge
        cfg.update_config()
        
    # 執行分析 (不傳入 mapped_x 等，讓函式自己去抓最新結構)
    run_chirality_analysis(dir_path=target_dir)


