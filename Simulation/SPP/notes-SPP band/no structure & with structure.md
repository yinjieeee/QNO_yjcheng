### 🔚 小結
研究 SPP 模態是否成功激發的關鍵分析步驟之一 ^b500ef
- 分析是否產生 SPP ^e72fde
- 移除非模態的場干擾 ^5f20fa
- 排除背景成分 ^67e424

```python
ey0_data = []  # no structure
time0_data = []  # no structure
ey_data = []
time_data = []
````

### ❓ 為什麼要區分「no structure」？

在模擬 Surface Plasmon Polaritons (SPPs) 時，我們會執行兩次模擬：

| 模擬情境                     | 是否加入金屬結構 (Ag) | 用途                            |
| ------------------------ | ------------- | ----------------------------- |
| **無結構 (no structure)**   | ❌ 沒有 Ag block | 作為背景參考，記錄 source 傳播時的純電場反應    |
| **有結構 (with structure)** | ✅ 加入金屬 Ag 結構  | 用來觀察是否激發出 SPP 模態，以及其時間演化與頻率特性 |

---

### 🧪 對應變數用途

|變數名稱|來源情境|資料內容|
|---|---|---|
|`ey0_data`|無結構|每個時間點的 Ey 值（背景場）|
|`time0_data`|無結構|時間軸（對應 Ey）|
|`ey_data`|有結構|每個時間點的 Ey 值（含結構場）|
|`time_data`|有結構|時間軸（對應 Ey）|

---

### 🧠 分析用途

這樣的資料區分允許我們進行以下分析：

1. **比較有結構與無結構下的 Ey 場量差異** → 分析是否產生 SPP。
2. **計算模態擷取的基準（Baseline Subtraction）** → 移除非模態的場干擾。
3. **繪圖與頻譜轉換（如 FFT、harminv）** 時可排除背景成分。

---

### ✅ 推薦後續應用範例

```python
# 對兩組資料做比較或差分分析
ey0_data = np.array(ey0_data)
ey_data = np.array(ey_data)
diff = ey_data - ey0_data  # 移除背景場
```

或：

```python
# 視覺化比較 Ey 時域曲線
plt.plot(time0_data, ey0_data, label="No Structure")
plt.plot(time_data, ey_data, label="With Structure")
```

---

### 🔚 小結

註解 `# no structure` 代表的是「**這是一組在沒有金屬結構（如 Ag block）時所收集的場資料**」，通常做為對照組（control）或背景消除（baseline removal）之用，是研究 SPP 模態是否成功激發的關鍵分析步驟之一。