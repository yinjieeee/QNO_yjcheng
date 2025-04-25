這份說明針對如何將 Conda 環境匯出為 `.yaml` 檔，方便備份、重建、或部署到其他機器。

---

## 1. 基本指令：匯出 Conda 環境

```bash
conda env export > environment.yaml
```

- 匯出目前啟用的 Conda 環境及其所有套件（包含 Python 版本與通道 channel）
- 預設輸出檔案：當前資料夾下的 `environment.yaml`

---

## 2. 匯出指定環境（非目前啟用者）

```bash
conda env export -n myenv > myenv.yaml
```

- `-n myenv`：指定環境名稱
- 適合有多個 Conda 環境時手動匯出

---

## 3. 僅匯出安裝歷史（推薦，較乾淨）

```bash
conda env export --from-history > environment.yaml
```

- 只包含手動安裝過的套件
- 不會輸出過多依賴（如 `libgcc`, `openssl` 等）
- 適合用於專案部署或分享給他人

---

## 4. YAML 檔案保存位置建議

| 位置                | 用途說明                             |
|---------------------|--------------------------------------|
| `/專案根目錄/environment.yaml` | 與程式碼一起版本控制（建議）          |
| `~/conda_envs_backups/`       | 個人環境備份區                        |
| `~/Dropbox/conda_envs/`       | 雲端備份環境                          |

> 小提示：可以建立 `.gitignore` 忽略不想同步的環境 YAML（例如含敏感路徑者）

---

## 5. 用 YAML 檔重建 Conda 環境

```bash
conda env create -f environment.yaml
```

- 預設會建立 `.yaml` 檔中指定的環境名稱
- 若想改名：

```bash
conda env create -f environment.yaml -n new_env_name
```

---

## 6. 檢查目前有哪些環境

```bash
conda env list
```

---

## 7. 刪除環境

```bash
conda env remove -n env_name
```

---

## 8. YAML 範例（典型輸出）

```yaml
name: myenv
channels:
  - defaults
dependencies:
  - python=3.9.12
  - numpy=1.23.0
  - pandas=1.4.2
  - pip:
      - matplotlib==3.5.2
```

---

## 9. 常見錯誤與排查

| 錯誤訊息                          | 原因與解法                                             |
|-----------------------------------|--------------------------------------------------------|
| `ResolvePackageNotFound`          | 該版本不再可用，考慮升級、改用其他 channel             |
| `YAML parsing error`              | `.yaml` 檔縮排有誤，請檢查空格或冒號                   |
| 環境建立後套件不全                | 建議使用 `--from-history` 匯出者重建時避免依賴缺漏     |

---

## 10. 建議加入 Git 專案的範本結構

```bash
my_project/
├── environment.yaml  # Conda 環境設定
├── requirements.txt  # pip 套件（若用 pip）
├── src/              # 程式碼資料夾
├── data/             # 資料集
└── README.md         # 專案說明
```

---

## 小結

- 使用 `conda env export > environment.yaml` 匯出完整環境
- 使用 `--from-history` 匯出更乾淨、適合分享
- 保存於專案內或雲端資料夾，方便跨機器重建環境