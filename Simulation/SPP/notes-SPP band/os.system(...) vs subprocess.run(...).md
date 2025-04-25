### ✅ 功能對比

| 比較項目                         | `os.system()`           | `subprocess.run()`                      |
| ---------------------------- | ----------------------- | --------------------------------------- |
| 語法簡單                     | ✅ 很簡單                   | 稍複雜（但可封裝）                               |
| 取得輸出結果                   | ❌ 無法直接取得 stdout/stderr  | ✅ 可用 `capture_output=True` 抓出來          |
| 檢查執行是否成功                 | ❌ 要自己額外處理               | ✅ 有 `returncode` 可用                     |
| 執行更安全、穩定                 | ❌ 易受 shell injection 影響 | ✅ 可用 `args` 傳遞，較安全                      |
| 跨平台兼容性                   | 中等                      | ✅ 更好，尤其在 Windows 系統                     |
| 進階控制（如 timeout、stdin 輸入） | ❌ 幾乎無法做                 | ✅ 支援 `stdin`、`timeout`、`text`、`env` 等參數 |

---

### ✅ 建議原則

|情境|建議使用|
|---|---|
|只是執行一個指令、無需抓輸出|`os.system()` 勉強可以|
|想要：取得執行結果、處理錯誤、判斷狀態|✅ 一律建議用 `subprocess.run()`|
|要傳遞 stdin（像你 `< input.txt`）|✅ `subprocess` 可以處理更彈性|
|有安全性或大型自動化需求|✅ `subprocess`|

---

### ✅ 總結建議

> **日常開發中，除非真的非常簡單，否則建議都使用 `subprocess.run()`。**

`os.system()` 已經是比較舊的方法，缺乏彈性與安全性。

---

#### 🎯 範例轉換

from os: 
```python
os.system("harminv -t 0.01 -Q 1 0-3 < data.txt")

```

to subprocess:
```python
import subprocess
cmd = "harminv -t 0.01 -Q 1 0-3 < data.txt"
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print(result.stdout)
```

>如果有很多模擬要跑、很多結果要抓，建議直接用 `subprocess` 搭配函式封裝