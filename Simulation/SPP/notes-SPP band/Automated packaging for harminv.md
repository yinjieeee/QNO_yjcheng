### 🎯 總體目標（Overall Purpose）

>在特定 Bloch 波向量 $k_x$ 下，模擬某一點的電場響應，並用 Harminv 提取該位置的模態頻率

應用範圍包含：
- 光子晶體 band structure 掃描
- 共振腔模態分析
- 導模頻率萃取
- Q-factor 頻譜分析

---

### 🧭 整體流程總覽（High-Level Workflow）

| 步驟 | 動作 | 說明 |
|------|------|------|
| ① | 定義收資料方式 | 定義 `collect_ey_tmp()`：從模擬中擷取 \( E_y(t) \) |
| ② | 建立模擬 | 依據輸入的 `kx` 設定 `mp.Simulation` |
| ③ | 收集時間序列資料 | 使用 `mp.at_every()` 收資料 |
| ④ | 儲存成檔案 | 寫入 `ey_time_tmp.txt`，供 Harminv 使用 |
| ⑤ | 呼叫 Harminv 分析 | 利用 `subprocess` 執行並抓取輸出 |
| ⑥ | 解析輸出 | 提取正頻率模態，回傳作為結果 |

---

### 🧩 功能區塊分項說明（Functional Blocks）

#### 1. 函式定義與暫存區初始化（Function Definition & Temp Storage）

```python
def sim_k_point_harminv(sim, kx):
    ey_tmp = []
    time_tmp = []
````

| 功能                   | 說明                                      |
| -------------------- | --------------------------------------- |
| 定義函式                 | 分析給定 $k_x$​ 下的模態頻率<br>定義模擬與分析流程         |
| `ey_tmp`, `time_tmp` | 儲存模擬期間的 $E_y$ 資料與時間戳記<br>初始化儲存時間序列資料的陣列 |

---

#### 2. 資料收集函式定義（Field Sampling Function）

```python
def collect_ey_tmp(sim):
    ey = sim.get_field_point(mp.Ey, mp.Vector3(0, sr_y))
    ey_tmp.append(ey)
    time_tmp.append(sim.meep_time())
```

| 功能   | 說明                         |
| ---- | -------------------------- |
| 收集場值 | 每次呼叫時擷取模擬中指定點的 $E_y$​ 值與時間 |
| 用途   | 提供時間序列給 Harminv 頻譜分析       |

---

#### 3. 建立與執行模擬（Simulation Setup & Run）

```python
sim.reset_meep()
sim = mp.Simulation(..., k_point=mp.Vector3(kx))
sim.run(mp.after_time(10, mp.at_every(1/resolution, collect_ey_tmp)), until=30)
```

| 功能                         | 說明                              |
| -------------------------- | ------------------------------- |
| `reset_meep()`             | 重設模擬狀態，避免前一次干擾                  |
| `k_point = mp.Vector3(kx)` | 設定 Bloch 波向量（$k_x$）             |
| `run()`                    | 模擬從 0 跑到 30，10 (穩態)之後開始以固定間距收資料 |

---

#### 4. 資料轉換與儲存（Data Conversion & File Output）

```python
with open(filename, "w") as f:
    for t, ey in zip(time_tmp, ey_tmp):
        f.write(f"{ey.real}+{ey.imag}i\n")
```

|功能|說明|
|---|---|
|資料轉換|將 list 轉為 NumPy array，利於運算與儲存|
|檔案輸出|將複數場值寫入檔案供 Harminv 使用（格式為 real+imagi）

---

#### 5. 執行 Harminv（Run Harminv via Subprocess）

```python
cmd = f"OMP_NUM_THREADS=1 harminv -t {1/resolution} -Q 1 0-3 < {filename}"
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
```

|功能|說明|
|---|---|
|呼叫外部工具|使用 Harminv 對時間序列資料做模態頻譜分析|
|控制資源|限制為單執行緒運作以防 CPU 滿載|
|擷取結果|把輸出結果擷取為文字供 Python 處理|

---

#### 6. 解析輸出結果（Parse Harminv Output）

```python
for line in result.stdout.splitlines():
    if line.startswith("frequency") or not line.strip():
		continue  # Skip header or empty lines
    try:
        freq = np.float64(line.split(",")[0].strip())
        if freq > 0:
            frequencies.append(freq)
    except (ValueError, IndexError):
        continue  # Skip invalid lines
return frequencies
```

| 功能     | 說明                |
| ------ | ----------------- |
| 處理文字輸出 | 將每行輸出逐行讀取與篩選      |
| 萃取正頻率  | 過濾掉錯誤行、負頻率與非數據列   |
| 回傳值    | 回傳此 $k_x$下的所有模態頻率 |

---

### 📈 常見用法（Typical Usage）

```python
kx_list = np.linspace(0, 0.5, 20)
all_modes = []
for kx in kx_list:
    modes = sim_k_point_harminv(sim, kx)
    all_modes.append((kx, modes))
```

之後可視覺化：

```python
for kx, freqs in all_modes:
    for f in freqs:
        plt.scatter(kx, f)
```

---

### ✅ 小結（Summary）

這個函式實現了一個完整的頻譜分析流程：

> 「模擬 → 時域收場 → 儲存 → Harminv 頻譜分析 → 擷取模態頻率」

非常適合用於自動化掃描不同波向量、分析模態譜與建立 band structure。
