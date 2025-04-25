### 🔍 Harminv 如何從時域提取 Q 值？

`harminv` 是 Meep 中的諧波分析工具，可從時域場量資料中擷取模態的頻率與 Q 值，適用於共振腔、SPP、光子晶體等結構。

### 📐 數學原理

假設場為下列形式的疊加：

$$
E(t) = \sum_n A_n e^{i\omega_n t} e^{-\gamma_n t}
$$

- $\omega_n$：模態頻率（弧度/秒）
- $\gamma_n$：衰減率
- **Q 值公式**：

$$
Q_n = \frac{\omega_n}{2\gamma_n}
$$

---

### ⚙️ Meep 使用範例

```python
sim.run(mp.after_sources(
            mp.Harminv(mp.Ez, mp.Vector3(x), fcen, df)),
        until_after_sources=mp.stop_when_fields_decayed(50, mp.Ez, mp.Vector3(x), 1e-3))
````

^aedd99

- `mp.Ez`：監測的場分量
- `mp.Vector3(x)`：觀測點位置
- `fcen`：中心頻率（要分析的頻率附近）
- `df`：頻率範圍（例如 0.2）
- [[meep_spp_harminv_notes]]


---

### 📊 輸出範例解析

```
freq: 0.1552  Q: 1200  decay time: 197  |A|: 0.37
freq: 0.1618  Q: 80    decay time: 10   |A|: 0.05
```

| 欄位           | 說明                  |
| ------------ | ------------------- |
| `freq`       | 模態頻率（Hz，或 Meep 單位）  |
| `Q`          | 品質因子（越高越穩定，共振越尖銳）   |
| `decay time` | 場量衰減時間/ 模態的壽命（單位時間） |
| \|`A`\|      | 對應模態的振幅（重要性/強度）     |

---

### 🔎 常見應用與 Q 值意義

| 結構類型       | Q 值代表意義                     |
| ---------- | --------------------------- |
| 微環共振腔      | 評估共振尖銳程度、能量儲存效率             |
| 表面電漿子（SPP） | 分析模態在金屬中的衰減與傳播距離            |
| 光子晶體腔      | 找出局域模態的頻率與壽命（Q）             |
| 發光增強結構     | 用於估算 [[Purcell factor]]增強因子 |

---

### ⚠️ 使用注意

- 模擬時間需足夠長，場需明顯衰減
  >如果時間序列不夠長、或訊號太弱，`harminv` 可能會失敗或輸出不穩定
- 須避免激發太多模態造成干擾
  >Gaussian pulse 太寬頻時，可能會同時激發多個模態，需小心頻譜分析
- `fcen` 和 `df` 的設定要包含目標頻率
  >須讓模擬 **持續足夠長時間**，直到場量衰減，否則無法準確擷取 Q 值

---

### ✅ 建議步驟（以 SPP 為例）

1. 使用 Gaussian source 靠近金屬介面激發寬頻波。
2. 在金屬旁邊設置監測點，記錄 Ez。
3. 使用 `harminv` 分析 Ez 的時間序列，擷取頻率與 Q 值。

---

### 📁 延伸閱讀

- [Meep official doc: harminv](https://meep.readthedocs.io/en/latest/Python_User_Interface/#harminv)
- [Harminv paper by Steven G. Johnson](https://arxiv.org/abs/physics/0211069)
