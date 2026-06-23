#utils.py

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