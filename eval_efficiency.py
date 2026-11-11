# eval_efficiency.py
"""
快速效率評估腳本：
僅計算 TMD 上下 Monitor 收集光占比，並搭配已知的遠場純度計算元件向上的物理轉換效率。
"""

import os
import re
import argparse
import numpy as np
import meep as mp
import meep.adjoint as mpa

import config as cfg
import models
import physics
import matplotlib.pyplot as plt

import utils


def load_structure_or_default(dir_path, npy_path=None, beta=512.0):
    """讀取結構 npy 檔案並做 Mapping，若無則回傳預設結構"""
    cfg.update_config()

    if npy_path is None and dir_path:
        raise FileNotFoundError(f"[Fast Evaluator] 在 {dir_path}/beta_data 找不到 structure_iter_*.npy")
    
    if npy_path is None and dir_path:
        beta_data_dir = os.path.join(os.path.expanduser(dir_path), 'beta_data')
        if os.path.exists(beta_data_dir):
            candidates = [f for f in os.listdir(beta_data_dir) if 'structure_iter_' in f and f.endswith('.npy')]
            if candidates:
                def extract_iter(fn):
                    m = re.search(r'iter_(\d+)', fn)
                    return int(m.group(1)) if m else -1
                latest_fn = max(candidates, key=extract_iter)
                npy_path = os.path.join(beta_data_dir, latest_fn)
                
                bm = re.search(r'beta_(\d+(?:\.\d+)?)', latest_fn)
                if bm:
                    beta = float(bm.group(1))

    Nx = int(cfg.resolution * cfg.design_width) + 1
    Ny = int(cfg.resolution * cfg.design_height) + 1

    if npy_path and os.path.isfile(npy_path):
        if mp.am_master():
            print(f"[Fast Evaluator] 載入結構: {npy_path} (Beta={beta})")
        x0 = np.load(npy_path).flatten().astype(np.float64)
    else:
        if mp.am_master():
            print("[Fast Evaluator] 未指定結構檔，使用全 Air 預設結構")
        # 直接建立全 0 的矩陣 (0.0 代表空氣, 1.0 代表介質)
        x0 = np.zeros((Ny, Nx), dtype=np.float64).flatten()

    filter_radius = mpa.get_conic_radius_from_eta_e(cfg.minimum_length, cfg.eta_e)
    mapping_func = physics.get_mapping(filter_radius, cfg)
    mapped_x = mapping_func(x0, cfg.eta_i, beta)
    
    return mapped_x


def run_fast_evaluation(dir_path=None, npy_path=None, known_purity=100.0):
    """
    僅執行 TMD 上下 Monitor 通量計算，帶入已知純度計算效率
    """
    cfg.update_config()
    mapped_x = load_structure_or_default(dir_path, npy_path)

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
    }

    scene = models.build_scene_data(cfg_dict)
    Nx = int(cfg.resolution * cfg.design_width) + 1
    Ny = int(cfg.resolution * cfg.design_height) + 1
    design_var = scene['geometry'][0].material
    design_var.weights = mapped_x.reshape(Nx, Ny, 1).astype(np.float64)

    sim = mp.Simulation(
        cell_size=scene['cell_size'],
        geometry=scene['geometry'],
        sources=scene['sources'],
        boundary_layers=scene['pml_layer'],
        resolution=cfg.resolution,
        default_material=mp.air,
        force_complex_fields=True,
        k_point=mp.Vector3(0, 0, 0)
    )

    # 架設 TMD 上下 Flux Monitor
    z_tmd_center = cfg.src_z
    
    # 1. 計算 TMD 中心至 Gap 頂面的總距離
    dist_from_center = cfg.design_thick
    
    # 2. 上下 Monitor 設定於距 TMD 中心相同的距離
    z_top_mon = z_tmd_center + dist_from_center
    z_bot_mon = z_tmd_center - dist_from_center

    mon_size = mp.Vector3(cfg.design_width, cfg.design_height, 0)

    top_flux_region = mp.FluxRegion(center=mp.Vector3(0, 0, z_top_mon), size=mon_size, direction=mp.Z)
    bot_flux_region = mp.FluxRegion(center=mp.Vector3(0, 0, z_bot_mon), size=mon_size, direction=mp.Z)

    top_flux_mon = sim.add_flux(cfg.frequency, 0, 1, top_flux_region)
    bot_flux_mon = sim.add_flux(cfg.frequency, 0, 1, bot_flux_region)

    if mp.am_master():
        print("[Fast Evaluator] 開始執行近場通量模擬 (無需遠場計算)...")

    sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ex, mp.Vector3(0, 0, cfg.monitor_z), 1e-5))
    
    if mp.am_master():
        fig, ax = plt.subplots(figsize=(8, 6))
    
        # 1. 繪製 Meep 2D X-Z 剖面結構
        sim.plot2D(output_plane=mp.Volume(center=mp.Vector3(0, 0, 0), size=mp.Vector3(cfg.Sx, 0, cfg.Sz)), ax=ax)
    
        # 2. 畫出關鍵 z 軸位置虛線
        ax.axhline(y=z_top_mon, color='red', linestyle='--', linewidth=2, label=f'Top Monitor (z={z_top_mon:.3f})')
        ax.axhline(y=z_bot_mon, color='blue', linestyle='--', linewidth=2, label=f'Bottom Monitor (z={z_bot_mon:.3f})')
        ax.axhline(y=z_tmd_center, color='green', linestyle=':', label='TMD Center')
    
        # 3. 加上圖例與座標軸標籤
        ax.set_xlabel("X (μm)", fontsize=12)
        ax.set_ylabel("Z (μm)", fontsize=12)
        ax.set_title("Monitor Positions and Device Geometry", fontsize=14)
        ax.legend(loc='upper right')
        plt.tight_layout()
        
        # 4. 儲存圖檔
        out_dir = os.path.expanduser(dir_path) if dir_path else "."
        prefix = utils.get_file_prefix(out_dir)
        png_path = os.path.join(out_dir, f"{prefix}_monitor_positions.png")
        plt.savefig(png_path, dpi=300)
        print(f"[Fast Evaluator] 結構與 Monitor 標示圖已儲存為 {png_path}")

    # 計算發光占比
    P_up_raw = mp.get_fluxes(top_flux_mon)[0]
    P_down_raw = mp.get_fluxes(bot_flux_mon)[0]

    P_up = max(0.0, P_up_raw)
    P_down = abs(P_down_raw)
    P_total_emitted = P_up + P_down + 1e-30

    ratio_up_pct = (P_up / P_total_emitted) * 100.0
    ratio_down_pct = (P_down / P_total_emitted) * 100.0

    # 處理輸入純度格式 (若是 decimal <= 1.0 則自動乘以 100)
    purity_pct = known_purity if known_purity > 1.0 else known_purity * 100.0
    device_efficiency_pct = (ratio_up_pct * purity_pct) / 100.0

    if mp.am_master():
        print("\n" + "=" * 65)
        print("         【快速物理轉換效率評估報告 (Fast Evaluator)】")
        print("=" * 65)
        print(f"1. TMD 上下 Monitor 收集光占比：")
        print(f"   - 向上發光功率 (P_up)           : {P_up:.6e} W")
        print(f"   - 向下發光功率 (P_down)         : {P_down:.6e} W")
        print(f"   - TMD 總發射功率 (P_total)       : {P_total_emitted:.6e} W")
        print(f"   - 向上發光占比 (X%)             : {ratio_up_pct:.2f}%")
        print(f"   - 向下發光占比                 : {ratio_down_pct:.2f}%")
        print("-" * 65)
        print(f"2. 帶入之已知遠場純度 (Purity, Y%)：")
        print(f"   - 遠場純度 (Y%)                : {purity_pct:.2f}%")
        print("-" * 65)
        print(f"3. 元件向上的物理轉換效率 (Device Efficiency, Z%)：")
        print(f"   - 計算公式：向上發光占比 (X%) × 純度 (Y%) = 效率 (Z%)")
        print(f"   - 向上物理轉換效率 (Z%)        : {ratio_up_pct:.2f}% × {purity_pct:.2f}% = {device_efficiency_pct:.2f}%")
        print("=" * 65 + "\n")

    return {
        "ratio_up_pct": ratio_up_pct,
        "ratio_down_pct": ratio_down_pct,
        "purity_pct": purity_pct,
        "device_efficiency_pct": device_efficiency_pct
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="快速效率評估 (已知遠場純度)")
    parser.add_argument('--dir', type=str, default=None, help='專案資料夾路徑')
    parser.add_argument('--npy', type=str, default=None, help='指定 .npy 結構檔案路徑')
    parser.add_argument('--purity', type=float, required=True, help='已知的遠場純度 (可填 85.5 或 0.855)')
    args = parser.parse_args()

    mp.verbosity(0)
    run_fast_evaluation(dir_path=args.dir, npy_path=args.npy, known_purity=args.purity)


