以下是 使用 Python + MEEP 模擬旋光效應（Optical Activity / Optical Rotation） 的完整總整理。

一、旋光原理簡介

旋光（Optical Rotation）：光通過手性介質時，線偏振方向產生旋轉。

常見於：

手性分子材料

手性結構（如螺旋狀光子晶體）

人工手性結構（metamaterial）


旋光角 $\theta$ 通常與波長 $\lambda$、材料厚度 $d$ 成正比： $$ \theta = \alpha d \quad \text{（其中 } \alpha \text{ 為旋光率）} $$



---

二、模擬流程概覽

graph TD
A[設計手性結構或材料] --> B[設定材料參數]
B --> C[定義光源偏振狀態]
C --> D[設置 MEEP 模擬]
D --> E[輸出場資訊]
E --> F[分析旋光角與偏振變化]


---

三、重點注意事項

1. 結構設計（Chiral Structure Design）

方式一：結構手性（推薦）

螺旋通道、旋轉排列、旋轉鏡像不對稱結構

使用 rotate()、geometry_lattice 做出對稱打破


方式二：等效材料張量（進階）

使用 epsilon_tensor 模擬人工旋光材料（非對稱張量）



2. 材料參數

使用 
```python
mp.Medium(epsilon=..., D_conductivity=..., ...)
```
設定材料

若可得，使用實際的折射率色散資料 ε(λ) 模擬更準確

注意：MEEP 不原生支援 chirality（如 $\mathbf{D} = \varepsilon \mathbf{E} + i\kappa \mathbf{B}$），需以結構或自定張量模擬實現


3. 光源設定

建議使用圓偏振源：
```python
def circular_source(freq, center, size, direction='RCP'):
    phase = 1j if direction == 'RCP' else -1j
    return [
        mp.Source(mp.ContinuousSource(frequency=freq), component=mp.Ex, center=center, size=size, amplitude=1),
        mp.Source(mp.ContinuousSource(frequency=freq), component=mp.Ey, center=center, size=size, amplitude=phase)
    ]
```



若研究線偏振旋轉，用單一方向偏振輸入即可


4. 模擬區域與參數

增加解析度 resolution=30~60 提高精度

使用 PML 邊界吸收反射波

選擇適當時間長度 
```python
until_after_sources=mp.stop_when_fields_decayed(...) 
```
捕捉穩定波形



---

四、旋光角與偏振分析

1. 擷取場值
```python
Ex_data = sim.get_array(center=output_point, component=mp.Ex)
Ey_data = sim.get_array(center=output_point, component=mp.Ey)
```

2. 旋光角計算（假設輸出為線偏振）
```python
import numpy as np
theta = 0.5 * np.angle(Ex_data + 1j * Ey_data)
```


3. 若使用 LCP / RCP 輸入

比較兩者透過率差異：circular dichroism

或比較相位差：circular birefringence



---

五、結果驗證建議

計算旋光角與厚度、波長關係曲線

嘗試模擬不同結構參數對旋光角的影響

與文獻或理論旋光率作對比



---

六、延伸應用

設計旋光濾波器、手性分子感測器、偏振控制元件

可延伸至非線性旋光模擬（如倍頻後旋光）



---

七、推薦工具搭配

- MEEP 官方文件
- 使用 matplotlib + numpy.fft 做傅立葉分析與偏振態可視化
- 搭配 MPB（光子帶隙模擬）分析手性結構的頻散關係
