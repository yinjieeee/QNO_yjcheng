---
Paper:
  - Plasmonic Purcell factor and coupling efficiency to surface plasmons. Implications for addressing and controlling optical nanosources
Paragraph:
  - "2.1"
tags:
  - Purcell_factor
---
Meaning：腔體內與真空中的自發性輻射衰減率的比值$F_P=\dfrac{3}{4\pi^2}(\dfrac{\lambda_{em}}{n_1})^3\dfrac{Q}{V}$

|                |                                    |
| -------------- | ---------------------------------- |
| 角頻率            | $\omega_{em}=2{\pi}c/\lambda_{em}$ |
| excited state  | $\|b>$                             |
|  ground state  | $\|a>$                             |
|                |                                    |
激發原子在ground state，其衰減率：
$$\Gamma(\mathbf{r})={\dfrac{2\pi}{\hbar^2}}\sum\limits_{\mathbf{k}_n}|\left\langle{a, \mathbf{k}_n|H_I|b,0}\right\rangle|^2\delta(\omega_{em}-\omega_{\mathbf{kn}})$$
- $H_I=-\hat{\textbf{p}}\cdot{\hat{\textbf{E}}}(\textbf{r})$ 交互作用的Hamitonian，描述電偶極近似後的原子與電磁場的耦合

主要探討腔體內的自發性輻射率，所以分成兩種組成：
- 真空貢獻：$n_1\Gamma_0={\dfrac{2\pi}{\hbar^2}}\sum\limits_{\textbf{k}_n}|\left\langle{a, \textbf{k}_n|H_0|b,0}\right\rangle|^2\delta(\omega_{em}-\omega_{\textbf{kn}})=n_1\dfrac{p^2{\omega_{em}^3}}{3\pi\epsilon_0\hbar{c}^3}$
- 腔體貢獻：$\Gamma_{cav}={\dfrac{2\pi}{\hbar^2}}\sum\limits_{\textbf{k}_n}|\left\langle{g, \textbf{k}_n|H_{cav}|e,0}\right\rangle|^2\delta(\omega_{em}-\omega_{\textbf{kn}})$

腔體貢獻限制**單模腔體**，共振在$\omega_c$，$$\Gamma_{cav}={\dfrac{2\pi}{\hbar^2}}\sum\limits_{\textbf{k}_n}|\left\langle{a, \textbf{1}|H_{cav}|b,0}\right\rangle|^2\delta(\omega_{em}-\omega_{\textbf{c}})\tag{8}$$





|                        |                                                                         |
| ---------------------- | ----------------------------------------------------------------------- |
| 表示光子存在的模態              | $\langle{a},\textbf{1}\|$的1                                             |
| 原子與腔體模態的耦合率(視cQED的g定義) | $\hbar{g}=\|\left\langle{a, \textbf{1}\|H_{cav}\|b,0}\right\rangle\|$的g |
| 量化體積                   | V                                                                       |
| boson operator         | $\hat{a}$                                                               |
| 腔體模態間的空間變化             | $\textbf{f}(\textbf{r})$                                                |

單模腔體的電場向量
$$\hat{E}_{cav}(\textbf{r})=i\sqrt{\dfrac{\hbar{\omega_c}}{2\varepsilon_0\varepsilon_1V}}\textbf{f}(\textbf{r})\hat{a}+h.c.\tag{9}$$
- $|\textbf{f}(\textbf{r})|=0$為節點，$|\textbf{f}(\textbf{r})|=1$則為波腹(離節點最遠)
為了實現這個表示法，典型的電場向量可表示
$$\hat{E}_{cav}(\textbf{r},t)=i\sqrt{\dfrac{\hbar{\omega_c}}{2\varepsilon_0\varepsilon_1V}}\textbf{f}(\textbf{r})e^{-i\omega_ct}+c.c.\tag{10}$$ 
normalized with respect to the energy 
**(11)**  $\hbar\omega_c=\frac{1}{2}\int[\varepsilon_0\varepsilon_1(\textbf{r})E^2(\textbf{r},t)+\mu_0{\textbf{H}}^2(\textbf{r},t)]d\textbf{r}$ 
**(12)**  $=\dfrac{\hbar\omega_c}{\epsilon_1V}\int\varepsilon(\textbf{r})|\textbf{f}(\textbf{r})|^2d\textbf{r}$ 
假設為**非色散介質**，可得其模態體積遵循**共振光譜形狀**
**(13)**  $V=\dfrac{1}{\varepsilon_1}\int\varepsilon(\textbf{r})|\textbf{f}(\textbf{r})|^2d\textbf{r}$
假設為**損耗腔體**，公式(8)的dirac分布會改成每角頻率的模態密度$N(\omega)$ (unit: $s\cdot{rad^{-1}}$)
進一步的變化，模態共振可以被假設成Lorentzian
**(14)**  $\delta(\omega-\omega_c){\to}N(\omega)=\dfrac{1}{\pi}\dfrac{\dfrac{\kappa_{cav}}{2}}{(\omega-\omega_c)^2+\dfrac{\kappa_{cav}^2}{4}}$ 
where $Q=\omega_c/\kappa_{cav}$，可以簡化成
**(15)**  $N(\omega)=\dfrac{2Q}{\pi\omega_c}\dfrac{1}{1+4Q^2(\dfrac{\omega-\omega_c}{\omega_c})^2}$


*Spatial Profile*
公式(9) 表示的interaction Hamiltonnian電場向量，也可以寫成
**(16)**  $|{\langle}g,\textbf{1}|H_{cav}|e,0\rangle|^2=\dfrac{p^2\hbar\omega_c}{2\varepsilon_0\varepsilon_1V}|\textbf{u}\cdot\textbf{f}(\textbf{r})|^2$      
- $\textbf{p}=p\textbf{u}$，$\textbf{u}$電偶極向量(orientation)
*Purcell factor*  利用公式(15)公式(16)，腔體貢獻對於衰減率的表示可以簡化成
**(17)**  $\Gamma_{cav}=\dfrac{2P^2}{\hbar\varepsilon_0\varepsilon_1}|\textbf{u}\cdot\textbf{f}(\textbf{r})|^2\dfrac{Q}{V}\dfrac{1}{1+4Q^2(\dfrac{\omega_{em}-\omega_c}{\omega_c})^2}$                                                                       
因此，normalized衰減率可以被寫成(同時利用公式(6) $\lambda_{em}=\dfrac{2\pi{c}}{\omega_{em}}$ )
**(18)**  $\dfrac{\Gamma_{cav}}{n_1\Gamma_0}=\dfrac{3}{4\pi^2}(\dfrac{\lambda_{em}}{n_1})^3\dfrac{Q}{V}\dfrac{|\textbf{u}\cdot\textbf{f}(\textbf{r})|^2}{1+4Q^2(\dfrac{\omega_{em}-\omega_c}{\omega_c})^2}$                                                                          

###### 2.1.1 Summarize
腔體貢獻的衰減率遵循公式(18)並改寫成$\dfrac{\Gamma_{cav}}{n_1\Gamma_0}=F_P\dfrac{|\textbf{u}\cdot\textbf{f}(\textbf{r})|^2}{1+4Q^2(\dfrac{\omega_{em}-\omega_c}{\omega_c})^2}$ 
- $\textbf{f}(\textbf{r})$表示位置依賴性（從節點處的抵消到波腹處的最大效應）
- 分母 $[{1+4Q^2(\dfrac{\omega_{em}-\omega_c}{\omega_c})^2}]$顯示了發射頻率和腔體共振之間的失諧(detuning)效應
最終，發射耦合對模態
發射器耦合對模態沿著電偶極呈現極化（$|\textbf{u}\cdot\textbf{f}(\textbf{r})|$)
接著再研究'電偶極發射器對奈米級電漿的耦合'的Purcell Factor. recall 公式(3)有助於研究:
- Purcell Factor與給予模態之間有關聯
- 腔體共振遵循Lorentzian形狀(shape)
- 模態體積可從公視(3)被推算，假設一非色散介質，其可表示$V=\dfrac{\int\varepsilon(\textbf{r})|\textbf{E}(\textbf{r})|^2d\textbf{r}}{Max[\varepsilon_1]|\textbf{E}(\textbf{r})|^2}$
$|\textbf{E}(\textbf{r})|$腔體模態相關的電場向量
$\textbf{f}(\textbf{r})=\dfrac{\textbf{E}(\textbf{r})}{Max[|\textbf{E}(\textbf{r})|]}$表示模態分布
###### 2.1.2 Purcell factor near a nanofiber
在3D光學腔體中自發性輻射的全控制是技術上的困難與帶寬限制，故提出了較簡易的配置
尤其是光子奈米環中的光致光輻射可以提升其光譜範圍，這是過去十年廣泛研究的主題
為了推導近光波導的Purcell Factor，定義了任意量化長度(L)
電場向量和模態密度可以以下公式表示
**(21)**  $\hat{\textbf{E}}(\textbf{r})=i\sqrt{\dfrac{\hbar\omega_c}{2\varepsilon_0\varepsilon_1A_{eff}L}}\textbf{f}(\textbf{r})\hat{a}+h.c.$ 
**(22)**  $A_{eff}=\dfrac{\int\varepsilon(x,z)|\textbf{E}(\textbf{r}_xz)|^2dxdz}{Max[\varepsilon_1|\textbf{E}(\textbf{r}_xz)|^2]}$ 
**(23)**  $N(\omega)=\dfrac{L}{\pi}\dfrac{1}{v_g}$, with $v_g=\dfrac{d\omega}{dk_g}$ 
$A_{eff}$ 代表模態有效面積，$v_g$ 被引導的模態的群速度，
$N^{2D}=\dfrac{1}{\pi{v_g}}$被引導的模態的密度
延續前面的計算，可以將Purcell Factor簡化成
**(24)**  $F_P=\dfrac{\Gamma_{guided}}{n_1\Gamma_0}=\dfrac{3}{4\pi}\dfrac{(\frac{\lambda_{em}}{n_1})^2}{A_{eff}}\dfrac{n_g}{n_1}$     
光子奈米光纖附近的 Purcell 因子由群指數控制$n_g=c/v_g$和橫向限制決定$A_{eff}$
高Purcell Factor需要低群速度和(或者)高限制模態
###### 2.1.3 Purcell factor in Fabry-Perot cavity
最終考慮1D面波導，被引導的模態的密度遵循$N^{1D}=\omega/2\pi{n_{eff}}n_g$
$n_{eff}$表示模態有效index，Purcell factor可以改寫成
**(25)**  $F_P=\dfrac{\Gamma_{guided}}{n_1\Gamma_0}=\dfrac{3}{4}\dfrac{(\frac{\lambda_{em}}{n_1})}{L_{eff}}\dfrac{n_{eff}n_g}{{n_1}^2}$
**(26)**  $L_{eff}=\dfrac{\int\varepsilon(z)|\textbf{E}(\textbf{z})|^2dz}{Max[\varepsilon_1|\textbf{E}(\textbf{z})|^2]}$ ，模態有效長度
###### 2.1.4 Coupling effciency(β-factor)
已介紹Purcell factor，量化電偶極與光子晶體之間的耦合強度
由於發射器可以透過各種通道（腔模式、洩漏、非輻射能量傳輸）鬆弛到其基態，因此定義腔體模態的耦合效率也很有用。這就是所謂的 β 因子
**(27)**  $\beta=\dfrac{\Gamma_{cav}}{\Gamma_{tot}}=\dfrac{\Gamma_{cav}}{\Gamma_{cav}+\Gamma_{other}}$
$\Gamma_{tot}$是總衰減率(包含relaxation channels)
在單模腔體中，relaxation channels通常式腔體模態的衰減率$\Gamma_{cav}$和洩漏(leak)模態的耦合
通常洩漏與初始輻射率$(\Gamma_{other}\simeq{n_1}\Gamma_0)$屬於同一數量級，因此$\beta\simeq\Gamma_{cav}/(\Gamma_{cav}+n_1\Gamma_0)\simeq{F_P}/(1+F_P)$。例如，約 Fp ~ 10 的 Purcell 因子對應於耦合效率 b ~ 90%。低閾值雷射需要高 β 因子
##### 2.2 Decay rate near lossy and dispersive materials
在有損色散介質存在的情況下，衰減速率的改變可以用典型的Lorentz振盪電偶極模型來描述，也可以用完整的量子來描述來描述。在這兩種情況下，這都會導致速率修改的以下表達式
**(28)**  $\dfrac{\Gamma_u(\textbf{r})}{n_1\Gamma_0}=\dfrac{6\pi}{n_1k_0}Im[g_{uu}(\textbf{r,r},\omega_{em})]$       
G為發射器環境相關的Green's tensor，$G_{uu}$代表沿電偶極對角線分量$\textbf{u}$
此表達式量化了複雜環境中衰減率的變化，並確定電漿奈米結構對螢光衰減率影響。公式(28)是Fermi's golden rule則對色散和有損耗環境的推廣。事實上，Fermi's golden rule(4)可以改寫為
**(29)**  $\Gamma(\textbf{r})=2\pi{g^2}(\textbf{r},\omega_{em})N(\omega_{em})$    
**(30)**  $\hbar{g}(\textbf{r},\omega_{em})=|\langle{a,\textbf{1}}|H_{cav}|b,0\rangle|$ 
**(31)**  $=\sqrt{\dfrac{\hbar{\omega_c}}{2\varepsilon_0\varepsilon_1V}}|\textbf{p}\cdot\textbf{f}(\textbf{r})|$
g耦合強度，$N(\omega)$模態密度，
從散射形式可以知道，部分局部態密度 (partial local density of states, P-LDOS) 與格林二元組(Green's dyad)有關（單位：$s\cdot{m^3}$）
**(32)**  $\rho_u(\textbf{r},\omega_{em})=\dfrac{k_0^2}{\pi\omega}Im[G_{uu}(\textbf{r},\textbf{r},\omega_{em})]$                               
因此在非吸收介質中，公式(4)和公式(28)完全相等；自cQED角度，P-LDOS也可以改寫成
**(33)**  $\rho_u(\textbf{r},\omega)=\dfrac{f_u(\textbf{r})}{2\epsilon_1V}N(\omega)$      
P-LDOS掌握了腔體模態$f_u(\textbf{r})$和可用光發模態$\rho(\omega)=N(\omega)/V$間的耦合之空間獨立，每單位角頻率和單位體積