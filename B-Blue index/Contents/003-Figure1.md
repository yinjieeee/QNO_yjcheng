---
Paper:
  - "[[003-Controlled-Phase Gate Using Dynamically Coupled Cavities and Optical Nonlinearities]]"
Page: 2/6
Paragraph:
---
![[Pasted image 20250212131629.png]]
>FIG. 1. Absorption, storage, and emission process with sche-matic illustrations of cavity implementations in $\chi^{(2)}$ (left) and $\chi^{(3)}$ (right) materials. Two sets of photonic crystal mirrors oriented perpendicularly ($\chi^{(2)}$) or inline ($\chi^{(3)}$) have band gaps in different frequency ranges as illustrated by the black lines in the bottom panel. One-sided cavities required for complete absorption are achieved by a slight frequency offset between the band gaps of the right (solid black) and left (dashed black) mirror. The decoupled mode (blue) is within the band gap of both mirrors while the coupled mode (purple) lies at the band edge of the left mirror. Only the decoupled cavity modes must have small volumes for efficient photon-photon interaction. The control modes are confined by weak mirrors ($\omega_1$ and $\omega_2$) located at the exterior of the small cavity modes.

| murmur            |                                                                                                                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| $\chi^{(2)}$ <br> | 兩個垂直波導，綠色場跟紫色光子垂直進入波導，然後在中央位置產生綠色場跟紅色場(綠色變紅色，且變寬許多；紫色變藍色)，發射時變成綠色場進紫色光子出<br>@紅色場和藍色場都細細的，為啥？圖片不是顯示他比較寬嗎<br>@紅色窄對綠色寬，why？<br>@藍色窄還有兩倍表示，紫色寬，why？                                  |
|                   | Absorption：$\omega_p$ and $\omega_a$ in<br>Storage：$\omega_b$ and $2\omega_b$<br>Emission：$\omega_p$ in, and $\omega_a$ out                                                      |
| $\chi^{(3)}$      | 我比較想說成一個波導，然後有兩個區塊(中央區塊跟邊緣區塊)<br>綠色場和紅色場右邊進，紫色光子左邊進，在中間會合後變成了藍色場(注意藍色小小的)，發射時綠色場和紅色場還是右邊進，紫色光子左邊出去<br>@只有藍色細細的，why？<br>@紅色和綠色一樣寬，紫色比藍色寬，why？<br>@left mirror和right mirror的差異是甚麼？ |
|                   | Absorption：$\omega_a$, $\omega_1$ and $\omega_2$ in<br>Storage：$\omega_b$<br>Emission：$\omega_1$ and $\omega_2$ in, and $\omega_a$ out                                           |

| **$χ^{(2)}$ ** | 三波混合                                                                                                   |
| -------------- | ------------------------------------------------------------------------------------------------------ |
| 吸收             | 頻率為 $\omega_a$ 的入射光子（紫色）通過波導傳播，以靜態速率 $\gamma$ 與腔模態 $a$ 耦合                                              |
| 儲存             | 模式 $b$（紅色）與波導解耦，通過強經典場（頻率 $\omega_p$，綠色）控制的三波混合過程與模式 $a$ 耦合，滿足 $\omega_p + \omega_b = \omega_a$        |
| 拉比振盪           | 兩個光子被吸收到模式 $b$ 後，在模式 $b$ 的雙光子態與模式 $c$ 的單光子態（頻率 $2\omega_b$，藍色）之間進行拉比振盪                                 |
| 相位控制           | 將存儲時間調整為一個完整拉比振盪週期，引入 $\pi$ 相位變化                                                                       |
| 頻譜特性           | 腔模 $b$ 的頻率：$\omega_b$（紅色）<br>控制場頻率：$\omega_p$（綠色）<br>雙頻率模式：$2\omega_b$（藍色）<br>入射光頻率：$\omega_a$（紫色波導光子） |
| 能帶結構           | 垂直排列的光子晶體鏡面形成特定頻率範圍的能帶間隙                                                                               |

| $χ^{(3)}$ | 四波混合                                                                                         |
| --------- | -------------------------------------------------------------------------------------------- |
| 耦合過程      | 使用兩個經典控制場（頻率 $\omega_1$ 和 $\omega_2$），通過四波混合過程使模式 $a$ 和 $b$ 耦合                               |
| 頻率關係      | 滿足 $\omega_2 - \omega_1 = \omega_a - \omega_b$ 的頻率匹配條件                                       |
| 相位調製      | 模式 $b$ 中的雙光子自相位調製產生條件相位移動                                                                    |
| 特殊性質      | 這種自相位調製效應在單光子輸入時不存在                                                                          |
| 頻譜特性      | 控制場頻率：$\omega_1$（紅色）和 $\omega_2$（綠色）<br>腔模 $b$ 頻率：$\omega_b$（藍色）<br>腔模 $a$ 頻率：$\omega_a$（紫色） |
| 能帶結構      | 內聯排列的光子晶體鏡面產生不同的能帶結構                                                                         |

| 關鍵比較參數 | $χ^{(2)}$                        | $χ^{(3)}$                                   |
| ------ | -------------------------------- | ------------------------------------------- |
| 能量守恆   | $\omega_p + \omega_b = \omega_a$ | $\omega_2 - \omega_1 = \omega_a - \omega_b$ |
| 相位操作   | 拉比振盪產生 $\pi$ 相位                  | 自相位調製產生條件相位移動                               |
| 腔模耦合   | 單一經典場   $\omega_p$ 控制            | 雙經典場   $\omega_1$ 和 $\omega_2$ 控制           |
