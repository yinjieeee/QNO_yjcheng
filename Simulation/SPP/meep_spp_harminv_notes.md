![[harminv#^aedd99]]

### 解釋

**`sim.run(...)`**
- 功能：執行模擬（run simulation）
- **`sim`** 前面建立的 **`mp.Simulation()`** 實體
- 內部兩個主要參數：
    - **`mp.after_sources(...)`** → 在 source 關閉後才開始執行的分析
    - **`until_after_sources=...`** → 設定什麼時候終止模擬

**`mp.after_sources(...)`**
- - 功能：**等 source 發完（場不再被注入）之後**，才開始執行這段分析指令
- 這能避免 `harminv` 讀到 source 本身的頻率，干擾模態分析

 **`mp.Harminv(...)`**
- 功能：分析某個場量在某位置的頻率組成，輸出每個頻率對應的 Q 值、衰減時間、振幅
- 常用來分析共振腔、波導模態、SPP 等模態參數

```python
mp.Harminv(field, where, fcen, df)
```

| 參數      | 意義                          |
| ------- | --------------------------- |
| `field` | 要觀察的場分量（例：`mp.Ez`, `mp.Ex`） |
| `where` | 觀察位置（例：`mp.Vector3(x)`）     |
| `fcen`  | 預估的模態中心頻率（Hz 或 Meep 單位）     |
| `df`    | 頻率搜尋範圍寬度（例：`0.2` 代表 ±0.1）   |

>`fcen` 和 `df` 的設定會影響結果：太窄可能錯過模態，太寬可能雜訊干擾

**`until_after_sources = mp.stop_when_fields_decayed(...)`**
- 這是模擬的 **停止條件**，意思是「等場在某點衰減到足夠小再停」

```python
mp.stop_when_fields_decayed(time, field, where, threshold)
```

| 參數          | 意義                           |
| ----------- | ---------------------------- |
| `time`      | 最長觀察時間（單位為 Meep 單位時間，ex: 50） |
| `field`     | 要監看的場分量（如 `mp.Ez`）           |
| `where`     | 觀察場變化的位置（例：`mp.Vector3(x)`）  |
| `threshold` | 衰減門檻，場量小於這個值就停（如 `1e-3`）     |
>這樣設置可以保證你在模擬中有足夠的時間觀察場的衰減過程，不會過早終止

### 範例值解釋

```python
mp.Harminv(mp.Ez, mp.Vector3(5), fcen=1.5, df=0.3)
```

- 在位置 `x=5` 的點，觀察 `Ez` 分量
- 預期模態頻率在 1.5 左右，搜尋範圍為 1.35 ~ 1.65 ($fecn\pm\frac{df}{2}$)
- 會輸出：模態頻率、Q 值、衰減時間等

### 完整流程概念

1. **激發**：先用 Gaussian pulse 激發寬頻場
2. **觀測**：用 Harminv 分析某點的場變化
3. **分析**：萃取其中的共振模態頻率與 Q 值
4. **終止**：當場量足夠衰減（表示模態已釋放能量）就自動結束模擬