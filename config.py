#config.py
import os
import numpy as np
import nlopt
import meep as mp

# --- 續跑相關參數 ---
resume_from = None       # 若非 None，表示從這個 .npy 路徑讀取初始結構
start_beta_val = None

# --- Beta Schedule 控制參數（新增預設值，可被 run.py 覆蓋） ---
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
design_width = 4.5
design_height = 4.5
design_thick = 0.257
resolution = 50
l_charge = 0
p_radial = 0
w0_target = 0.8

minimum_length = 0.05
eta_i = 0.5
eta_e = 0.75

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
    'update_factor': None,  # 這裡的預設值會被 args.update_factor 覆蓋
    'ftol': 1e-5
}