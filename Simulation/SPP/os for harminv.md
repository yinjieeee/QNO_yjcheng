**呼叫外部程式 `harminv` 來做頻譜分析**，從用 Meep 收集的電場時間序列中，找出其**頻率組成與 Q-factor**。

---

### 🔧 程式碼逐行說明

```python
import os
```

引入 Python 的 `os` 模組，用來執行 shell 指令。

---

```python
cmd_str1 = f"OMP_NUM_THREADS=1 harminv -t {1/resolution} -Q 1 0-3 < ey_time_data.txt"
```

這行是關鍵，生成的 shell 指令如下：

### 🧨 實際執行的命令行：

```bash
OMP_NUM_THREADS=1 harminv -t Δt -Q 1 0-3 < ey_time_data.txt
```

逐項拆解：

| 部分                   | 說明                                                                       |
| -------------------- | ------------------------------------------------------------------------ |
| `OMP_NUM_THREADS=1`  | 限制 harminv 使用 1 條執行緒（避免吃滿所有 CPU 核心）                                      |
| `harminv`            | 執行 `harminv` 程式，它是用來分析頻譜與 Q 值的工具                                         |
| `-t 1/resolution`    | 每個時間點之間的間距 $\Delta t$，要與你在 Meep 用 `at_every(1/resolution)` 的 sampling 一致 |
| `-Q 1 0-3`           | 將結果濾波，僅輸出 Q-factor 大於 1、頻率範圍在 0 到 3 的模態                                  |
| `< ey_time_data.txt` | 將時間序列資料從此檔案輸入給 harminv（格式：`Ey_real Ey_imag` 每行一筆）                        |

^a5c14f

---

```python
os.system(cmd_str1)
```

這行會直接執行上述指令，相當於在終端機裡輸入一樣的東西。Harminv 分析結果會直接印出到 terminal（或 Jupyter output）。

---

### ✅ 這段的前提條件

1. 你已經把 `ey_data` 與 `time_data` 輸出到 `ey_time_data.txt`，格式如下：
    
    ```text
    0.1234   0.0000
    0.1298   0.0000
    ...
    ```
    
2. 你執行的是時間序列分析，希望從某點的 Ey(t)E_y(t) 得到：
    - 含有的頻率成分（mode frequency）
    - 每個頻率的 Q-factor
    - 每個 mode 的 amplitude、decay rate

---

### ✅ 輸出長什麼樣？

Harminv 會印出像這樣的東西：

```text
frequency    decay rate     Q       amplitude       error
1.2345       0.00123        501     0.045 + 0.003i   1e-6
```

- `frequency`：模態頻率（單位：normalized frequency）
- `Q`：品質因子（越高代表越穩定、越少耗散）
- `amplitude`：模態的振幅（複數）
- `error`：Harminv 自己估計的數值擬合誤差
    

---

### 🧠 為何這樣設參數？

|設定|原因|
|---|---|
|`OMP_NUM_THREADS=1`|Harminv 有 OpenMP 支援，預設吃滿所有核心，會干擾系統運作|
|`-t 1/resolution`|必須對應你時間序列的取樣頻率，否則頻譜會錯|
|`-Q 1 0-3`|避免雜訊模態、只看 0 到 3 的物理模態（Meep freq 預設單位）|

^869bc5

---

### 🧪 延伸建議（進階自動化）

如果你想把結果直接存下來（而不是只在 terminal 顯示），可以改成：

```python
cmd_str1 = f"OMP_NUM_THREADS=1 harminv -t {1/resolution} -Q 1 0-3 < ey_time_data.txt > harminv_output.txt"
```

然後你就可以用 Python 讀取並分析結果：

```python
with open("harminv_output.txt", "r") as f:
    lines = f.readlines()
    # 進一步處理文字結果
```

---

### ✅ 小結

這段就是**用 Python 自動呼叫 harminv** 來從 `Ey(t)` 時間序列提取模態頻率與 Q 值。關鍵是：

- 要正確對應 `resolution`、時間間距 `-t`
- 資料格式要正確（複數形式）
- 加 `OMP_NUM_THREADS=1` 是為了控制資源用量
