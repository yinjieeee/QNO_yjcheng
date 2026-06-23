#physics.py

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
    return opt