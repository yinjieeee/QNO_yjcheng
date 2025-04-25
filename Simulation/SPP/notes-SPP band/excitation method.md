在 Meep（MIT Electromagnetic Equation Propagation）中，`excitation method` 指的是用來激發場（電磁波）的方式，也就是在模擬中如何「注入」能量或訊號到模擬區域。這是模擬電磁現象（如波導、共振腔、光子晶體等）時非常核心的一環。

---
### 如何選擇 Excitation Method？

|目標|推薦 Excitation 方法|
|---|---|
|想要寬頻分析（如傳輸光譜）|Gaussian Pulse|
|想要分析單頻穩態行為（如共振）|Continuous Wave|
|想注入導波模態（如波導模擬）|EigenMode Source|
|特殊需求（如時域編碼、非線性激發）|Custom Source|


---

### Meep 中常見的 Excitation 方法有：

#### 1. **Continuous Wave (CW) Source**

- **說明**：連續波源，發出單一頻率的正弦波。
    
- **適用情境**：模擬穩態頻率響應，如共振模態、傳輸頻譜等。
    
- **Meep 實作**：
    
    ```python
    source = mp.Source(mp.ContinuousSource(frequency=1.0),
                       component=mp.Ez,
                       center=mp.Vector3(0,0))
    ```
    

#### 2. **Gaussian Pulse Source**

- **說明**：有限時間內發出一個高斯包絡的脈衝，頻譜寬（可涵蓋多個頻率）。
    
- **適用情境**：模擬寬頻響應，如傳輸譜、模態分析（FDTD 頻譜分析）。
    
- **Meep 實作**：
    
    ```python
    source = mp.Source(mp.GaussianSource(frequency=1.0, fwidth=0.2),
                       component=mp.Ez,
                       center=mp.Vector3(0,0))
    ```
    

#### 3. **Custom Sources**

- **說明**：使用使用者自定義的 time-domain 函數。
    
- **適用情境**：需要模擬具特定時域特性的場源（如任意調變、方波等）。
    
- **Meep 實作**：
    
    ```python
    def my_func(t):
        return np.sin(2*np.pi*1.0*t) * np.exp(-((t-20)/10)**2)
    
    source = mp.Source(mp.CustomSource(my_func),
                       component=mp.Ez,
                       center=mp.Vector3(0,0))
    ```
    

#### 4. **Mode Source**

- **說明**：注入已知導波模態（如波導中的 TE 或 TM 模態），使用 eigenmode solver 來找出模態並注入。
    
- **適用情境**：研究導波結構（如光子晶體波導、矽波導）中的模態耦合與傳輸。
    
- **Meep 實作**（需搭配 mode solver）：
    
    ```python
    mode_src = mp.EigenModeSource(src=mp.GaussianSource(frequency=1.0, fwidth=0.2),
                                  center=mp.Vector3(-5, 0),
                                  size=mp.Vector3(0, 3),
                                  eig_band=1,
                                  eig_parity=mp.ODD_Z)
    ```

---

### 小結

在 Meep 中，excitation method 指的是「如何激發場源」，常見方法有 Gaussian、CW、Custom 與 Mode source，各自適用於不同模擬目的。若你能說明你正在模擬哪種類型的結構（例如：共振腔、波導、光柵等），我可以幫你推薦最合適的 excitation 設定。

你目前是要模擬哪一種結構或現象？我可以幫你寫出完整的 source 設定範例。