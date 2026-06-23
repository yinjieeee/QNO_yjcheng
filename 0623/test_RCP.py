"""
test_RCP.py
===========
讀取已優化結構（LCP 光源訓練），改用 RCP 光源做單次 forward simulation，
輸出近場相位、winding number、手性密度、遠場分析等圖。

用法：
    python test_RCP.py --struct path/to/structure_iter_020_beta_16.00.npy
                       --l_charge 1 --w0 0.5 --tag rcp_test
"""

import argparse
import os
import numpy as np
import meep as mp
import meep.adjoint as mpa
from scipy.special import genlaguerre

import config as cfg
import models
import utils


# ─────────────────────────────────────────────
# 1. 命令列引數
# ─────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--struct',    type=str,   required=True,
                        help='優化結構 .npy 路徑，例如 beta_data/structure_iter_020_beta_16.00.npy')
    parser.add_argument('--tag',       type=str,   default='rcp_test')
    parser.add_argument('--width',     type=float, default=1.5)
    parser.add_argument('--height',    type=float, default=1.5)
    parser.add_argument('--thick',     type=float, default=0.257)
    parser.add_argument('--res',       type=int,   default=50)
    parser.add_argument('--l_charge',  type=int,   default=1)
    parser.add_argument('--p_radial',  type=int,   default=0)
    parser.add_argument('--w0',        type=float, default=0.5)
    return parser.parse_args()


# ─────────────────────────────────────────────
# 2. 建構 config_dict（避免 vars(cfg) 的雜訊）
# ─────────────────────────────────────────────
def build_config_dict(cfg_module):
    """手動挑選 cfg 模組中的物理參數，回傳乾淨的 dict。"""
    keys = [
        'design_width', 'design_height', 'design_thick',
        'resolution', 'l_charge', 'p_radial', 'w0_target',
        'wavelength', 'frequency', 'fwidth', 'dpml',
        'source_pml', 'monitor_pml', 'material_monitor',
        'tmd_thick', 'base_thick',
        'Sx', 'Sy', 'Sz',
        'monitor_z', 'src_z',
        'zR', 'far_field_distance', 'z_ff_total',
        'w0_radius', 'ff_width', 'ff_res',
        'dir_path',
    ]
    return {k: getattr(cfg_module, k) for k in keys}


# ─────────────────────────────────────────────
# 3. 建立 RCP 光源（覆蓋 LCP 預設值）
# ─────────────────────────────────────────────
def make_rcp_source(config_dict):
    """
    LCP: Ex=1,  Ey=+1j  →  E = (x̂ + iŷ)/√2
    RCP: Ex=1,  Ey=-1j  →  E = (x̂ - iŷ)/√2  ← 此函式回傳
    """
    src_z   = config_dict['src_z']
    src_center = mp.Vector3(0, 0, src_z)          # ← 光源 z 座標，非 design_center
    gs  = mp.GaussianSource(config_dict['frequency'],
                             fwidth=config_dict['fwidth'])
    return [
        mp.Source(gs, component=mp.Ex, center=src_center,
                  size=mp.Vector3(0, 0, 0), amplitude=1.0),
        mp.Source(gs, component=mp.Ey, center=src_center,
                  size=mp.Vector3(0, 0, 0), amplitude=-1j),   # ← RCP 關鍵：負號
    ]


# ─────────────────────────────────────────────
# 4. 設定 MaterialGrid 權重（載入結構）
# ─────────────────────────────────────────────
def load_weights_into_geometry(geometry, weights, Nx, Ny):
    """
    geometry[0] 是 design Block（MaterialGrid）。
    weights 是 flatten 的 1D array，reshape 成 (Nx, Ny, 1)。
    """
    design_var = geometry[0].material          # mp.MaterialGrid
    w = np.clip(weights, 0, 1)
    if w.ndim == 1:
        w = w.reshape(Nx, Ny, 1)
    elif w.ndim == 2:
        w = w[:, :, np.newaxis]
    design_var.weights = w
    return design_var


# ─────────────────────────────────────────────
# 5. 提取近場
# ─────────────────────────────────────────────
def extract_near_fields(sim, config_dict):
    """在 sim.run() 後呼叫，提取 monitor 平面的 DFT 場。"""
    monitor_z = config_dict['monitor_z']
    dw        = config_dict['design_width']
    dh        = config_dict['design_height']
    freq      = config_dict['frequency']

    center = mp.Vector3(0, 0, monitor_z)
    size   = mp.Vector3(dw, dh, 0)

    def get(comp):
        return sim.get_dft_array(nf_dft, comp, 0)

    nf_dft = sim.add_dft_fields(
        [mp.Ex, mp.Ey, mp.Ez, mp.Hx, mp.Hy, mp.Hz],
        freq, freq, 1,
        center=center, size=size
    )
    # run 之後才能取值；這裡回傳 dft handle，run 後再呼叫 _fetch
    return nf_dft, center, size


def fetch_near_fields(sim, nf_dft):
    """sim.run() 結束後，從 DFT handle 提取六個分量。"""
    comps = [mp.Ex, mp.Ey, mp.Ez, mp.Hx, mp.Hy, mp.Hz]
    keys  = ['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz']
    return {k: sim.get_dft_array(nf_dft, c, 0) for k, c in zip(keys, comps)}


# ─────────────────────────────────────────────
# 6. 提取遠場（Near2Far）
# ─────────────────────────────────────────────
def compute_far_fields(sim, config_dict, n2f_monitor_region):
    """使用 near2far 計算遠場。"""
    ff_dist  = config_dict['far_field_distance']
    ff_width = config_dict['ff_width']
    ff_res   = config_dict['ff_res']
    monitor_z = config_dict['monitor_z']

    x_ff = np.linspace(-ff_width / 2, ff_width / 2, ff_res)
    y_ff = np.linspace(-ff_width / 2, ff_width / 2, ff_res)
    ff_points = [mp.Vector3(x, y, monitor_z + ff_dist) for x in x_ff for y in y_ff]

    n2f_obj = sim.add_near2far(
        config_dict['frequency'], 0, 1,
        n2f_monitor_region
    )

    # 需在 run 後呼叫
    return n2f_obj, ff_points, ff_res


def fetch_far_fields(sim, n2f_obj, ff_points, ff_res):
    """sim.run() 結束後，提取遠場六分量並 reshape。"""
    ff_data = np.array([sim.get_farfield(n2f_obj, pt) for pt in ff_points])
    # ff_data shape: (N_pts, 6)  → Ex, Ey, Ez, Hx, Hy, Hz
    keys = ['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz']
    return {k: ff_data[:, i].reshape(ff_res, ff_res)
            for i, k in enumerate(keys)}


# ─────────────────────────────────────────────
# 7. 主程式
# ─────────────────────────────────────────────
def main():
    args = parse_args()

    # 7-1. 更新 config
    cfg.design_width  = args.width
    cfg.design_height = args.height
    cfg.design_thick  = args.thick
    cfg.resolution    = args.res
    cfg.l_charge      = args.l_charge
    cfg.p_radial      = args.p_radial
    cfg.w0_target     = args.w0
    cfg.test_param    = args.tag
    cfg.update_config()

    config_dict = build_config_dict(cfg)

    # 7-2. 建立輸出資料夾
    out_dir = cfg.dir_path
    os.makedirs(out_dir, exist_ok=True)
    if mp.am_master():
        print(f"[INFO] Output dir: {out_dir}")

    # 7-3. 讀取結構權重
    struct_path = os.path.expanduser(args.struct)
    weights = np.load(struct_path)
    if mp.am_master():
        print(f"[INFO] Loaded weights from: {struct_path}  shape={weights.shape}")

    # 7-4. 建立場景（LCP 預設，後面會覆蓋光源）
    scene = models.build_scene_data(config_dict)

    # 7-5. 載入結構到 MaterialGrid
    Nx = int(cfg.resolution * cfg.design_width)  + 1
    Ny = int(cfg.resolution * cfg.design_height) + 1
    design_var = load_weights_into_geometry(scene['geometry'], weights, Nx, Ny)

    # 7-6. 覆蓋為 RCP 光源
    rcp_sources = make_rcp_source(config_dict)
    if mp.am_master():
        print("[INFO] Source polarisation: RCP  (Ex=1, Ey=-1j)")

    # 7-7. 建立 Simulation
    sim = mp.Simulation(
        cell_size        = scene['cell_size'],
        geometry         = scene['geometry'],
        sources          = rcp_sources,         # ← RCP
        boundary_layers  = scene['pml_layer'],
        resolution       = config_dict['resolution'],
        default_material = mp.air,
        force_complex_fields = True,
        # k_point 不需要設定（點光源無 Bloch 邊界）
    )

    # 7-8. 設定 monitors（先登記，run 後取值）
    monitor_z  = config_dict['monitor_z']
    dw, dh     = config_dict['design_width'], config_dict['design_height']
    freq       = config_dict['frequency']

    nf_dft = sim.add_dft_fields(
        [mp.Ex, mp.Ey, mp.Ez, mp.Hx, mp.Hy, mp.Hz],
        freq, freq, 1,
        center=mp.Vector3(0, 0, monitor_z),
        size  =mp.Vector3(dw, dh, 0)
    )

    n2f_region = mp.Near2FarRegion(
        center   =mp.Vector3(0, 0, monitor_z),
        size     =mp.Vector3(dw, dh, 0),
        direction=mp.Z
    )
    n2f_obj = sim.add_near2far(freq, 0, 1, n2f_region)

    # 7-9. 執行模擬（等收斂）
    if mp.am_master():
        print("[INFO] Running simulation ...")
    sim.run(until_after_sources=mp.stop_when_fields_decayed(
        dt=50, c=mp.Ez,
        pt=mp.Vector3(0, 0, monitor_z),
        decay_by=1e-5
    ))
    if mp.am_master():
        print("[INFO] Simulation done.")

    # 7-10. 提取近場 & 遠場（只在 master rank 畫圖）
    near_fields = fetch_near_fields(sim, nf_dft)

    ff_width = config_dict['ff_width']
    ff_res   = config_dict['ff_res']
    ff_dist  = config_dict['far_field_distance']
    x_ff = np.linspace(-ff_width / 2, ff_width / 2, ff_res)
    y_ff = np.linspace(-ff_width / 2, ff_width / 2, ff_res)
    ff_points = [mp.Vector3(x, y, monitor_z + ff_dist) for x in x_ff for y in y_ff]

    # get_farfield 回傳 [Ex, Ey, Ez, Hx, Hy, Hz] 複數 array
    ff_raw = np.array([sim.get_farfield(n2f_obj, pt) for pt in ff_points])  # (N, 6)
    ff_fields = {k: ff_raw[:, i].reshape(ff_res, ff_res)
                 for i, k in enumerate(['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz'])}

    # 7-11. 繪圖（全部集中在 master）
    if mp.am_master():
        ITER  = 0        # 非優化，用 iter=0 表示
        BETA  = 0.0
        design_size = mp.Vector3(dw, dh, config_dict['design_thick'])

        # --- 近場相位圖 ---
        utils.plot_phase_analysis(
            near_fields=near_fields,
            iter_num   =ITER,
            beta       =BETA,
            dir_path   =out_dir,
            design_size=design_size,
        )
        print("plot_phase_analysis done.")

        # --- Winding number（三個採樣半徑交叉驗證）---
        print("\n--- Phase Winding (RCP input) ---")
        for rf in [0.3, 0.45, 0.65]:
            winding = utils.plot_phase_winding(
                near_fields=near_fields,
                iter_num   =ITER,
                beta       =rf,          # 用 rf 當 beta 以區分檔名
                cfg        =config_dict,
                dir_path   =out_dir,
                design_size=design_size,
                l_charge   =config_dict['l_charge'],
                r_fraction =rf,
            )
            print(f"  r_fraction={rf:.2f}  →  winding = {winding:+.3f} × 2π"
                  f"  (LCP-optimised expected = +{config_dict['l_charge']}, "
                  f"RCP expected = -{config_dict['l_charge']})")

        # --- 近場手性密度 ---
        utils.plot_near_chirality(
            near_fields=near_fields,
            iter_num   =ITER,
            beta       =BETA,
            dir_path   =out_dir,
            cfg        =config_dict,
        )
        print("plot_near_chirality done.")

        # --- 遠場強度 / 相位圖 ---
        utils.plot_farfield_analysis(
            ff_fields=ff_fields,
            iter_num =ITER,
            beta     =BETA,
            dir_path =out_dir,
            cfg      =config_dict,
        )
        print("plot_farfield_analysis done.")

        # --- 遠場手性密度圖 ---
        utils.plot_ff_chirality(
            ff_fields=ff_fields,
            iter_num =ITER,
            beta     =BETA,
            dir_path =out_dir,
            cfg      =config_dict,
        )
        print("plot_ff_chirality done.")

        print(f"\n[DONE] All figures saved to: {out_dir}")


# ─────────────────────────────────────────────
if __name__ == '__main__':
    mp.verbosity(0)
    main()