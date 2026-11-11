# run_forward.py
import argparse
import os
import re
import numpy as np
import meep as mp

import config as cfg
import models
import utils

import meep.adjoint as mpa
import physics


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--struct',   type=str,   required=True, help='結構 .npy 路徑')
    parser.add_argument('--tag',      type=str,   default=None)
    parser.add_argument('--width',    type=float, default=4.5)      # 配合現行預設 4.5
    parser.add_argument('--height',   type=float, default=4.5)
    parser.add_argument('--thick',    type=float, default=0.257)
    parser.add_argument('--res',      type=int,   default=50)
    parser.add_argument('--l_charge', type=int,   default=1)
    parser.add_argument('--p_radial', type=int,   default=0)
    parser.add_argument('--w0',       type=float, default=0.8)      # 配合現行預設 0.8
    parser.add_argument('--beta',     type=float, default=None,
                         help='僅用於出圖檔名/標題標註；預設會嘗試從 --struct 檔名解析 beta_XXX，'
                              '解析不到則標為 512.0')
    parser.add_argument('--pol', type=str, default='lcp', choices=['lcp', 'rcp'], help='偏振設定')
    parser.add_argument('--minimum_length', type=float, default=0.05,
                    help='務必與當初優化這個結構時的 --minimum_length 一致')
    parser.add_argument('--eta_i', type=float, default=0.50,
                    help='務必與當初優化這個結構時的 --eta_i 一致')
    parser.add_argument('--eta_e', type=float, default=0.75,
                    help='務必與當初優化這個結構時的 --eta_e 一致')
    parser.add_argument('--material_monitor', type=float, default=0.05,
                    help='對齊 final_opt_log.py 實際跑 TO 用的值；不是 combined_all 版被改成的 0')
    return parser.parse_args()


def resolve_beta_tag(struct_path, beta_arg):
    """決定要標註在圖檔名稱/標題上的 beta 數值：優先用 --beta，否則從結構檔名解析。"""
    if beta_arg is not None:
        return beta_arg
    m = re.search(r'beta_(\d+(?:\.\d+)?)', os.path.basename(struct_path))
    if m:
        return float(m.group(1))
    return 512.0


def build_config_dict(cfg_module):
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
        'dir_path', 'eta_i', 'eta_e', 'minimum_length'
    ]
    return {k: getattr(cfg_module, k, None) for k in keys}


def make_source(config_dict, pol):
    src_z = config_dict['src_z']
    src_center = mp.Vector3(0, 0, src_z)
    gs = mp.GaussianSource(config_dict['frequency'], fwidth=config_dict['fwidth'])

    ey_amp = 1j if pol.lower() == 'lcp' else -1j

    
    return [
        mp.Source(gs, component=mp.Ex, center=src_center, size=mp.Vector3(0, 0, 0), amplitude=1.0),
        mp.Source(gs, component=mp.Ey, center=src_center, size=mp.Vector3(0, 0, 0), amplitude=ey_amp),
    ]


def load_weights_into_geometry(geometry, weights, Nx, Ny):
    design_var = geometry[0].material
    w = np.clip(weights, 0, 1)
    if w.ndim == 1:
        w = w.reshape(Nx, Ny, 1)
    elif w.ndim == 2:
        w = w[:, :, np.newaxis]
    design_var.weights = w
    return design_var


def fetch_near_fields(sim, nf_dft):
    comps = [mp.Ex, mp.Ey, mp.Ez, mp.Hx, mp.Hy, mp.Hz]
    keys  = ['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz']
    # 加上 .squeeze() 確保去除單維度，符合 utils 畫圖格式 (Nx, Ny)
    return {k: sim.get_dft_array(nf_dft, c, 0).squeeze() for k, c in zip(keys, comps)}


def main():
    args = parse_args()

    # 1. 更新 cfg 全域參數
    cfg.test_param    = args.tag
    cfg.design_width  = args.width
    cfg.design_height = args.height
    cfg.design_thick  = args.thick
    cfg.resolution    = args.res
    cfg.l_charge      = args.l_charge
    cfg.p_radial      = args.p_radial
    cfg.w0_target     = args.w0
    cfg.material_monitor = args.material_monitor
    cfg.update_config()

    config_dict = build_config_dict(cfg)

    out_dir = cfg.dir_path
    os.makedirs(out_dir, exist_ok=True)
    if mp.am_master():
        print(f"[INFO] Output dir: {out_dir}")

    # 2. 載入結構
    struct_path = os.path.expanduser(args.struct)

    weights = np.load(struct_path).flatten().astype(np.float64)
    BETA = resolve_beta_tag(args.struct, args.beta)

    filter_radius = mpa.get_conic_radius_from_eta_e(config_dict['minimum_length'], config_dict['eta_e'])
    mapping_func = physics.get_mapping(filter_radius, cfg)
    mapped_weights = mapping_func(weights, config_dict['eta_i'], BETA)
    
    # 3. 建立場景與 RCP 光源
    scene = models.build_scene_data(config_dict)
    Nx = int(cfg.resolution * cfg.design_width)  + 1
    Ny = int(cfg.resolution * cfg.design_height) + 1
    load_weights_into_geometry(scene['geometry'], mapped_weights, Nx, Ny)

    sources = make_source(config_dict, args.pol)

    # 4. 建立 Simulation 實例
    sim = mp.Simulation(
        cell_size        = scene['cell_size'],
        geometry         = scene['geometry'],
        sources          = sources,
        boundary_layers  = scene['pml_layer'],
        resolution       = config_dict['resolution'],
        default_material = mp.air,
        force_complex_fields = True,
    )

    # 5. 設定 Monitors
    monitor_z = config_dict['monitor_z']
    dw, dh    = config_dict['design_width'], config_dict['design_height']
    freq      = config_dict['frequency']

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


    # 6. 執行模擬
    if mp.am_master():
        print("[INFO] Running simulation ...")
    sim.run(until_after_sources=mp.stop_when_fields_decayed(
        dt=50, c=mp.Ez,
        pt=mp.Vector3(0, 0, monitor_z),
        decay_by=1e-5
    ))

    # 7. 擷取近場與遠場數據
    near_fields = fetch_near_fields(sim, nf_dft)

    ff_width = config_dict['ff_width']
    ff_res   = config_dict['ff_res']
    ff_dist  = config_dict['far_field_distance']
    x_ff = np.linspace(-ff_width / 2, ff_width / 2, ff_res)
    y_ff = np.linspace(-ff_width / 2, ff_width / 2, ff_res)
    ff_points = [mp.Vector3(x, y, monitor_z + ff_dist) for x in x_ff for y in y_ff]

    ff_raw = np.array([sim.get_farfield(n2f_obj, pt) for pt in ff_points])
    ff_fields = {k: ff_raw[:, i].reshape(ff_res, ff_res)
                 for i, k in enumerate(['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz'])}

    # 8. 繪圖 (僅 Master 執行)
    if mp.am_master():
        ITER = 0
        design_size = mp.Vector3(dw, dh, config_dict['design_thick'])
        utils.plot_design(
            plot_sim=sim,
            design_variables=scene['geometry'][0].material,
            mapped_x=mapped_weights,
            Nx=Nx,
            Ny=Ny,
            iters=ITER,
            beta=BETA,
            dir_path=out_dir,
            design_center=scene['design_center'],
            design_size=design_size,
            opt_problem=None
        )
        # 模擬遠場相位 / 強度 —— 各自單獨輸出成一張圖（+ 原始數據 .npy）
        phase_path, intensity_path = utils.plot_farfield_sim_only(
            ff_fields=ff_fields, iter_num=ITER, beta=BETA, dir_path=out_dir, cfg=config_dict
        )
        print(f" Sim Far-Field Phase     -> {phase_path}")
        print(f" Sim Far-Field Intensity -> {intensity_path}")

        print(f"\n[DONE] Standard figures saved to: {out_dir}")

if __name__ == '__main__':
    mp.verbosity(0)
    main()