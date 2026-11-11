## 專案概述

本專案用 Meep 的 adjoint 做 TO 最佳化：在 TMD 單層上方設計一層圖樣化介電結構，讓圓偏振點偶極源的向上輻射，在遠場形成拓撲荷數為 ℓ 的 Laguerre-Gaussian (LG) 渦旋光束。主要評估指標是遠場純度 (purity，即遠場功率落在目標 LG 模態的比例)。

**模擬幾何 (由下而上)：** 鑽石基底(n = 2.4)→ TMD 層 (n = 2.4，厚 1/resolution = 0.02 µm，偶極源放在其中心)→ 設計層 (4.5 × 4.5 µm，厚 0.257 µm，GaP材料在空氣與 n = 3.31 之間連續變化)→ 空氣 → 近場監視面 → PML。

**光源：** 在 TMD 中心同時放 Ex (振幅 1) 與 Ey (振幅 1j) 點源，構成圓偏振偶極 (定義為LCP)，高斯脈衝中心波長 0.593 µm、頻寬為中心頻率的 10%。

**關鍵固定參數(皆在 `config.py` 的 `update_config()`)：**

| 參數                   | 數值                                 | 說明                                             |
| -------------------- | ---------------------------------- | ---------------------------------------------- |
| 波長 / 頻率              | 0.593 µm / 1/0.593                 | Meep 單位 a = 1 µm                               |
| 解析度                  | 50 px/µm                           | 可由 `--res` 改；  <br>TMD 厚度與基底的源層厚度隨之改變(= 1/res) |
| 設計區尺寸 / 厚度           | 4.5 × 4.5 / 0.257 µm               | `--width --height --thick`                     |
| PML 厚度               | 0.3 µm                             | 四周與上下皆有                                        |
| 模擬區大小                | 5.1 × 5.1 × 1.547 µm               | Sx = Sy = 設計寬 + 2·dpml                         |
| 目標光束腰 w0             | 0.8 µm                             | 瑞利長度 zR ≈ 3.39 µm                              |
| 有效遠場距離               | 10 zR ≈ 33.9 µm                    | `--far_times`                                  |
| 遠場視窗                 | 約 24–41 µm 平方(ℓ = 0–5)，200 × 200 點 | 由 `FF_WIDTH_MAP` 查表                            |
| 最小線寬 / eta_i / eta_e | 0.05 µm / 0.50 / 0.75              | 濾波與投影                                          |
| β 排程                 | 4 × √2 遞增，上限 128，再加 256、512        | 共 13 個階段                                       |
| 每階段最大評估次數            | β < 32：12 次；β ≥ 32：30 次            | 整次最佳化約 282 次模擬                                 |

程式相依套件：Python、`meep-mpi`、`meep.adjoint`、`autograd`、`nlopt`、`numpy`、`scipy`、`pandas`、`matplotlib`、`mpirun`。

## 一、完整架構

整個專案是「一條最佳化主線 + 三個獨立的驗證/分析工具」：所有程式共用 `config.py` 的全域參數，並透過 `models.py` 建立同一個模擬場景。

[![[完整架構流程圖.png]]

實線箭頭代表呼叫或資料流向；`config.py` 被所有模組讀取，圖中只畫出寫入它的 `run.py`。`eval_chirality.py` 既是主線結束時自動呼叫的步驟，也可以獨立執行。

**最佳化主線(一次 `run.py` 執行)：**

1. `torun.sh` 或 `torerun.sh` 用 `mpirun` 啟動 `run.py`。
2. `run.py` 把命令列參數寫進 `config`，呼叫 `update_config()` 重算遠場距離、模擬區大小與輸出路徑，再建立初始結構 x0 與 β 排程。
3. `solver.LGOptimizer` 建立場景(`models`)與伴隨問題(`physics.create_opt_problem`)。
4. 對每個 β 階段，NLopt MMA 反覆呼叫 `objective(x)`：x → 濾波 + tanh 投影得到 mapped_x → Meep 正向模擬(Ex + iEy 偶極)→ 近場 DFT 與 Near2Far 遠場(200 × 200 點)→ FOM = log(purity) + 0.1·log(overlap²) → 伴隨模擬得梯度 → 經 autograd 回到 x。
5. 每個 β 階段結束時只保留該階段 FOM 最高的快照，存下 x、結構圖、近遠場圖，並以它作為下一個 β 的起點。
6. 全部 β 結束後畫歷史曲線，再自動執行 `eval_chirality` 的手性傳播分析。

注意：
- 兩個空間。 x 是最佳化變數(存檔)，mappedx 經濾波與投影、後續接續模擬的材料權重；兩者之間的轉換由 physics.getmapping(濾波半徑, cfg) 負責，參數是最小線寬、etae、etai 與 β。
- MPI。 所有 rank 都一起跑模擬，只有 rank 0(mp.am_master())負責印資訊、畫圖、寫檔。run.py 開頭的 excepthook 讓其他 rank 的錯誤訊息靜默，所以錯誤只會出現在 rank 0。
- 單位與網格。 Meep 單位 a = 1 µm；材料網格點數 Nx = res·width + 1(目前 226 × 226)。
- 檔名前綴。 所有輸出檔名都帶上資料夾名前兩段(如 `017_ell0`)，由 `utils.get_file_prefix` 產生。

## 二、各檔案負責內容

13 個檔案分成三群：被其他程式 import 的核心模組、執行最佳化的入口腳本、最佳化後獨立執行的驗證與分析工具。

### A. 核心模組(被 import，不直接執行)

| 檔案           | 負責什麼     | 主要內容                                                                                                                                                                                                                                                                                                                                                       |
| ------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `config.py`  | 全域參數與衍生量 | 預設參數(設計區、解析度、ℓ、w0、eta)；  <br>`update_config()` 重算 zR、  <br>遠場距離與視窗、  <br>Sx/Sy/Sz、  <br>monitor_z、  <br>src_z、  <br>輸出路徑 `~/LG_WS2/<test_param>`；  <br>`get_beta_schedule()`；  <br>`load_structure_npy()`；  <br>`nlopt_params`；  <br>`FF_WIDTH_MAP`(ℓ → 遠場視窗倍率)                                                                                            |
| `models.py`  | 建立模擬場景   | `build_scene_data(config_dict)` 回傳：  <br>cell_size、  <br>geometry(設計區 MaterialGrid、TMD、基底三個 Block)、  <br>sources(Ex + iEy)、  <br>PML、  <br>design_center、monitor_z。  <br>**三種材料折射率寫死在這支檔案**(鑽石 2.4、WS2 2.4、GaP 3.31)                                                                                                                                       |
| `physics.py` | 映射與目標函數  | `get_mapping`：conic filter + tanh projection；  <br>`create_opt_problem`：建立  <br>近場 DFT、  <br>Near2Far 遠場點陣、  <br>目標 LG 場(含曲率相位與 Gouy 相位)、  <br>FOM 函數 J                                                                                                                                                                                                    |
| `solver.py`  | 最佳化      | `LGOptimizer`：建立  <br>`Simulation` 與伴隨問題、  <br>`objective()`(映射 → 正向 + 伴隨 → 經 autograd 鏈式法則回到設計變數)、  <br>`optimize()`(逐個 β 階段跑 NLopt MMA、對每階段留最佳快照、存檔與繪圖)                                                                                                                                                                                                  |
| `utils.py`   | 存檔與繪圖    | `get_file_prefix`(取資料夾前綴如 `017_ell0`)；  <br>`save_*`、`init_csv/append_csv`；  <br>`plot_design`、  <br>`plot_phase_analysis`、  <br>`plot_farfield_analysis`、  <br>`plot_phase_winding`(計算繞數)、  <br>`plot_near_chirality`、  <br>`plot_ff_chirality`、  <br>`plot_chirality_propagation`、  <br>`plot_purity/overlap/FOM_history`、  <br>`plot_farfield_sim_only` |

### B. 最佳化入口

| 檔案           | 負責什麼         | 主要內容                                                                                                                                                       |
| ------------ | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `run.py`     | 單一最佳化工作的程式入口 | 解析命令列、組出資料夾名稱、覆寫 `config` 變數、建立初始結構(全新：0.5 + 0.01·sin(ℓφ)；續跑：讀 `.npy`)、裁切 β 排程、呼叫 `LGOptimizer.optimize`，結束後自動呼叫 `eval_chirality`。也寫入 `process.pid` 以便中途終止 |
| `torun.sh`   | 「全新一輪」批次啟動   | 預設同時啟動 ℓ = 0–3 四個 job，各用 `mpirun -np 32`(合計 128 個程序)；序號 N-N+3；日期、備註在腳本頂端手改；標準輸出存成 `.out`                                                                   |
| `torerun.sh` | 「續跑」批次啟動     | 每個 job 指定來源資料夾，自動找 `beta_data` 內 iter 最大的結構檔，用 `--resume_npy` + `--start_beta_val auto` 從該 β 階段重新開始；當前設定 3 個 job(ℓ = 2、1、5)，寫入新的資料夾                        |

### C. 驗證與後處理工具(獨立執行)

| 檔案                   | 負責什麼                   | 輸入 → 輸出                                                                                                               |
| -------------------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `eval_chirality.py`  | 手性傳播分析                 | 最佳結構 → 正向模擬 → 在 0–0.9 zR(每 0.1)與 1–10 zR(每 1)的 20 個平面取 6 分量場 → `.npz` 快取 + 光學手性密度傳播圖。`run.py` 結束時自動呼叫；也可 `--dir` 獨立執行 |
| `run_forward.py`     | 純正向驗證某個已存結構            | `.npy`(未映射的設計變數)→ 照檔名的 β 做映射 → 以 LCP 或 RCP 激發跑一次 → 結構圖、遠場相位與強度圖                                                       |
| `run_forward.sh`     | `run_forward.py` 的批次啟動 | 自動找指定資料夾的最新結構、從檔名抽出 β；極化由 `POL_TAG` 設定(目前 lcp)                                                                        |
| `eval_efficiency.py` | 快速效率估算                 | 在 TMD 上下兩個通量監視面算「向上發光占比」，再乘上你輸入的遠場純度(`--purity`)得元件向上轉換效率。不做遠場計算，較快                                                   |
| `test_RCP.py`        | 用 RCP 激發測試結構的手性選擇性     | 載入結構 → 以 Ex + (−1j)Ey 激發 → 近場與遠場分析圖。**目前版本無法執行，見建議章節**                                                                |

**資料夾命名規則(`run.py` 組出)：** `<序號>_ell<ℓ>_<寬><高>_<厚>_w<w0>_ml<最小線寬>_ie<eta_i>0<eta_e>_<備註>`，數字一律去掉小數點與前導 0。例如 `013_ell2_4545_257_w8_ml5_ie5075_job3_0602_log` = 序號 013、ℓ = 2、4.5 × 4.5 µm、厚 0.257、w0 = 0.8、最小線寬 0.05、eta_i = 0.5 / eta_e = 0.75、備註 `job3_0602_log`(為第 3 個 job、6/2 啟動、log 版 FOM，以實際紀錄為準)。

## 操作手冊

程式預期放在 `~/LG_WS2/scripts`(兩支 .sh 的 `SCRIPT_DIR`)，結果寫到 `~/LG_WS2/<資料夾名>/`。

**1. 全新最佳化。** 編輯 `torun.sh` 頂端的 `DATE`、`FOM`、序號起始值(目前是 `N + ELL`)、`COMMON_ARGS`，其中序號不可與既有資料夾重複，再執行 `bash torun.sh`。單一 job 的等價指令：

```bash
mpirun -np 32 python -u run.py --l_charge 1 --serial_number 999 --note test \
  --width 4.5 --height 4.5 --thick 0.257 --w0 0.8 --res 50 \
  --minimum_length 0.05 --eta_i 0.50 --eta_e 0.75
```

**2. 看進度。** `.out` 檔每次評估印 `Iter N | Beta | Purity | Overlap_abs2 | Best FoM`；資料夾內的 `<前綴>_objective_evolution.csv` 逐筆記錄 Iteration、Beta、Raw_Purity、Overlap_Abs2、FOM；`process.pid` 只記 rank 0 的 PID，要中止整個工作請終止對應的 `mpirun`。

**3. 續跑。** 編輯 `torerun.sh` 的 `JOBS`，每行格式為 `ℓ 新序號 備註 來源資料夾 start_beta_val`，`auto` 表示用最新結構檔名上的 β。續跑會從該 β 階段**重新**開始一次(以存下的最佳 x 為起點)，並寫到新的資料夾。β 排程參數必須與當初一致，否則裁切索引會不同。

**4. 驗證已存結構。** 編輯 `run_forward.sh` 的 `JOBS`(ℓ、序號、備註、來源資料夾)與 `POL_TAG`(lcp 或 rcp)後執行。結果在 `~/LG_WS2/<序號>_ell<ℓ>_fwd_<極化>_<日期>_<備註>/`。

**5. 快速算效率。** `python eval_efficiency.py --npy <結構.npy> --dir <輸出資料夾> --purity 85.5`(可用 `mpirun` 加速)。已知問題見「三、建議」的 #3 與 #6。

**6. 手性傳播圖單獨重產。** `mpirun -np 32 python eval_chirality.py --dir ~/LG_WS2/<資料夾> --l_charge <ℓ>`。若資料夾 `chirality_propagation/` 已有同 iter 的 `.npz` 快取，會直接讀快取而不重算。

**輸出資料夾內容(皆帶 `<前綴>_`，例如 `017_ell0_`)：**

```text
~/LG_WS2/<資料夾>/
  process.pid                     rank 0 的 PID
  *_objective_evolution.csv       每次評估的 purity / overlap / FOM
  *_purity_history_staircase.png/.csv，*_Overlap_abs2_history*，*_FOM_history*
  *_final_{purity,overlap_abs2,FoM}_history.npy
  beta_data/                      每個 β 階段最佳結構(.npy = 未映射的設計變數；.png = 映射後結構圖)
  phase_analysis/                 近場相位與強度
  chirality_near_analysis/        近場手性密度
  farfield_analysis/              模擬遠場 vs 目標 LG
  chirality_ff_analysis/          遠場手性密度
  farfield_phase_winding/         遠場相位繞數
  chirality_propagation/          多高度手性傳播圖 + .npz 快取
```

注意：`beta_data/*.npy` 存的是**最佳化變數 x**，不是二值化後的結構。要重建實際結構，必須用同樣的濾波半徑(由 `minimum_length`、`eta_e` 推算)、`eta_i` 與檔名上的 β 再映射一次。