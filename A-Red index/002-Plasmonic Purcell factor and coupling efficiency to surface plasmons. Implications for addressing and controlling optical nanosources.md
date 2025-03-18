---
Cite as: IOP Publushing, J. Opt. 18 (2016) 094005 (23pp)
DOI: 10.1088/2040-8978/18/9/094005
Submitted: " 4 October 2015"
Accepted: 22 December 2015
Author:
  - G Colas des Francs
  - J Barthes
  - A Bouhelier
  - J C Weeber
  - A Dereux
  - A Cuche
  - C Girard
tags:
  - Purcell_factor
  - surface_plasmon
  - localized_plasmon
  - cQED
  - red_index
Source from: LINE-QNO Group
---
|      |                                                                                 |
| ---- | ------------------------------------------------------------------------------- |
| 自己問題 | 除了Purell Factor的小段有比較理解怎麼計算，其餘的(尤其是本篇主要內容)感覺一直讀不太懂，也讀得很慢<br>@先換其他篇讀，等讀比較多時再回來看看 |


#### Related links
- [[Purcell factor]]

---
#### Researchers
01. G Colas des Francs
2. J Barthes
3. A Bouhelier
4. J C Weeber
5. A Dereux
6. A Cuche
7. C Girard
---
#### Abstract
>The Purcell factor $F_p$ is a key quantity in cavity quantum electrodynamics (cQED) that quantifies the coupling rate between a dipolar emitter and a cavity mode. 
>Its simple form $F_{p}\propto{Q/V}$ unravels the possible strategies to enhance and control light–matter interaction. 
>Practically, efficient light–matter interaction is achieved thanks to either (i) high quality factor Q at the basis of cQED or (ii) low modal volume V at the basis of nanophotonics and plasmonics. 
>In the last decade, strong efforts have been done to derive a plasmonic Purcell factor in order to transpose cQED concepts to the nanocale, in a scale-law approach. 
>In this work, we discuss the plasmonic Purcell factor for both delocalized (SPP) and localized (LSP) surface-plasmon-polaritons and briefly summarize the expected applications for nanophotonics. 
>On the basis of the SPP resonance shape (Lorentzian or Fano profile), we derive closed form expression for the coupling rate to delocalized plasmons. 
>The Q factor and modal confinement of both SPP and LSP are quantified, demonstrating their strongly subwavelength behavior.

|     |                                                                                                       |
| --- | ----------------------------------------------------------------------------------------------------- |
| 核心  | Purcell factor                                                                                        |
| 延伸  | 從Purcell factor找出可以對應實際材料的參數(高Q低V)，拓展在應用上<br>(i)  cQED的Q<br>(ii) nano光子學和電漿的低模態體積V                    |
| 討論  | (i)  討論SPP/ LSP兩種電漿的Purcell factor<br>(ii) 討論SPP共振形狀((Lorentzian or Fano profile)，推導出SPP電漿耦合率的封閉形式表達式 |
| 證實  | SPP/ LSP的Q參數及模態被量化，證實其亞波長的效應                                                                          |




---
#### Introduction
nanophotonics實現奈米尺度下光與物質之間的作用，直至單光子/原子尺度
動機主要為顯著高敏度檢測的應用，如奈米光學影像(表面分析)、環安(空污/ 傳染病性病原體檢測)或者健康照護(癌前診斷/ 治療診斷)與晶片上整合超快光子元件的小型化
光學截面是表徵光物質作用效率的簡易方法
於分子而言，通常為$\sigma\sim10^{-20}m^2$，與繞射極限光束的聚焦區域於可見範圍${(\frac{\lambda}{2})}^2\sim10^{-13}m^2$相比
數量級差距呈現兩者的不匹配性，造成實驗的困難度
過往的政策指出增加光物質作用效率by
(i)使用低工作溫度以增加吸收截面(T<10K)""分子吸收截面增加至繞射級線$\sigma_0=\frac{3\lambda^2}{2\pi}$，顯示出分子吸收了聚焦光束的入射光
(ii)透過將分子置於具有高Q的光學微腔內來增加相互作用的持續時間
(iii)利用近場光學或電漿將激發光束限制在繞射極限以下
定量描述，光物質作用效率可依協同參數C計算出。
在自由空間中，協同性可表示為共振原子截面與高斯光束的光腰的有效面積$A_{eff}=\pi{w_0^2}$，$C_0\sim\sigma_0/A_{eff}$
因此，協同性量化聚焦點和分活性區域之間的適應性，在fabry perot中，$C=4C_0F/\pi$，F是精細度，腔體通過波的往返次數$F/\pi$增強了自由空間的協同性，腔體內有一係數(4)表示模態波腹處的強度增強
在cQED中，協同性可被表示$C=\frac{g^2}{2\kappa_{cav}n_1\Gamma_0}$
g 原子與腔體模態的耦合率，$\kappa_{cav}$腔體損耗率，$\Gamma_0$真空中的原子衰減率，$n_1\Gamma_0$材料中的原子衰減率
強耦合strong coupling regime($g\gg\kappa_{cav}$),  $\Gamma_0$($C\gg1$) leaads to a reversible energy exchange between cavity and the atom.
in weak coupling regime, the cavity open a new channel for the for the atom(irreversible) relaxtion with a decay rate $\Gamma=(1+2C)\Gamma_0$
$\Gamma_{0}->n_1\Gamma_0$
$\Gamma-n_1\Gamma_0=2Cn_1\Gamma_0$
$\Gamma-n_1\Gamma_0=\Gamma_{cav}=2Cn_1\Gamma_0$
Purcell factor quantifies the effect of the cavity on the atom decay rate and writes   $F_P=\dfrac{\Gamma_{cav}}{n_1\Gamma_0}=2C$
where also can be expressed $F_P=\dfrac{\Gamma_{cav}}{n_1\Gamma_0}=\dfrac{3}{4\pi^2}(\dfrac{\lambda_{em}}{n_1})^3\dfrac{Q}{V_{eff}}$
Q quality factor腔體的品質因子
Veff 腔體模態在耦合時的有效體積
$\lambda_{em}$ 原子的發射波長
這種表示法與典型Fabry perot腔體以精細度表示法相同

值得注意的是，Purcell factor可見透過控制Q與V以達到高效自發性輻射效率
但高Q意味著模態數少(因為繞射極限)，為此分子電漿對於光物質作用有了新的應對
強限制的表面電漿極化確保了深亞波長的有效耦合，cQED增加作用的持續時間
由於這個原因，需細講Q factor在Purcell Factor的意義，進入珀塞爾因子的品質因子（Q factor）是腔體因子和原子共振中較小的那個。

> [!NOTE]
>品質因子（Q factor）是一個描述共振系統能量儲存能力的物理量。
>在這個系統中，存在兩個品質因子：
>腔體的品質因子（cavity factor）
>原子共振的品質因子（atomic resonance）
>當我們計算珀塞爾因子時，我們需要使用這兩個品質因子中較小的那個。這是因為：
>系統的整體性能受限於其最弱的環節
>較低的品質因子會成為限制系統表現的瓶頸
>舉個例子：
>如果腔體的品質因子是1000，而原子共振的品質因子是500，那麼在計算珀塞爾因子時，我們應該使用500這個值，因為它是較小的那個，也是實際限制系統性能的因素。
>這個概念很重要，因為它告訴我們系統的實際性能總是受到最弱部分的限制，而不是由最強的部分決定的。

實際上，$1/Q=1/Q_{atom}+1/Q_{cav}$
Qatom 原子輻射光譜的品質因子
Qcav 腔體的品質因子
這也是cQED通常操作在低溫的原因：原子共振夠窄，使腔體能夠控制自發性輻射($Q_{atom}{\gg}Q_{cav},and{ Q}\sim{Q_{cav}}$)
相對的，表面電漿共振的Q小可以操作在室溫並實現高速光學元件
小Q為奈米級的超快控制鋪路

Purcell Factor用方程式解釋了腔體發射耦合的光學腔體性質，其發射器性質無關
論是否為窄共振或者深度限制的模態，高Q/V比值實現最高效的耦合效率
Purcell Factor是將cQED轉置成量子電漿的關鍵參數
於此篇文章，首先將總結光學微腔內的Purcell Fator推導並著重描述其基本假設(sec2)
詳細討論部分關於已存在的有效SPP發射器的耦合器(sec3)
接著研究電漿的Purcell Factor之觀念，由於模態限制是電漿奈米結構附近實現高Purcell Factor的重要參數，我們遵循擴展金屬膜(sec4)、電漿波導(sec5)，支持非局部表面電漿極化(surface plasmon polaritons，SPP)，延伸至奈米物體維持局部表面(localized surface plasmons，LSP)(sec6)



#### SEC2 Purcell Fator
##### 2.1 Purcell Fator in an optical microcavity; generalities
自發性輻射
角頻率$\omega_{em}=2{\pi}c/\lambda_{em}$
excited state $|b>$     ground state $|a>$
激發原子在ground state，其衰減率可以表示為：
$\Gamma(\mathbf{r})={\dfrac{2\pi}{\hbar^2}}\sum\limits_{\mathbf{k}_n}|\left\langle{a, \mathbf{k}_n|H_I|b,0}\right\rangle|^2\delta(\omega_{em}-\omega_{\mathbf{kn}})$
$H_I=-\hat{\textbf{p}}\cdot{\hat{\textbf{E}}}(\textbf{r})$ 交互作用的Hamitonian，描述電偶極近似後的原子與電磁場的耦合
對腔體內的自發性雷射率有興趣，為此，分成兩種組成：真空貢獻(均勻介質n1)與腔體貢獻
$n_1\Gamma_0={\dfrac{2\pi}{\hbar^2}}\sum\limits_{\textbf{k}_n}|\left\langle{a, \textbf{k}_n|H_0|b,0}\right\rangle|^2\delta(\omega_{em}-\omega_{\textbf{kn}})=n_1\dfrac{p^2{\omega_{em}^3}}{3\pi\epsilon_0\hbar{c}^3}$
$\Gamma_{cav}={\dfrac{2\pi}{\hbar^2}}\sum\limits_{\textbf{k}_n}|\left\langle{g, \textbf{k}_n|H_{cav}|e,0}\right\rangle|^2\delta(\omega_{em}-\omega_{\textbf{kn}})$
腔體貢獻限制'單模腔體'，共振在$\omega_c$，
$\Gamma_{cav}={\dfrac{2\pi}{\hbar^2}}\sum\limits_{\textbf{k}_n}|\left\langle{a, \textbf{1}|H_{cav}|b,0}\right\rangle|^2\delta(\omega_{em}-\omega_{\textbf{c}})$                                                                                 (8)
$\langle{a},\textbf{1}|$的1表示光子存在的模態
$\hbar{g}=|\left\langle{a, \textbf{1}|H_{cav}|b,0}\right\rangle|$，g代表原子與腔體模態的耦合率(視cQED的g定義)
有關於單模腔體的電場向量描述
$\hat{E}_{cav}(\textbf{r})=i\sqrt{\dfrac{\hbar{\omega_c}}{2\varepsilon_0\varepsilon_1V}}\textbf{f}(\textbf{r})\hat{a}+h.c.$                                                                                                 (9)
V為量化體積，$\hat{a}$為boson operator，$\textbf{f}(\textbf{r})$表示腔體模態間的空間變化
$|\textbf{f}(\textbf{r})|=0$為節點，$|\textbf{f}(\textbf{r})|=1$則為波腹(離節點最遠)
為了實現這個表示法，典型的電場向量可表示$\hat{E}_{cav}(\textbf{r},t)=i\sqrt{\dfrac{\hbar{\omega_c}}{2\varepsilon_0\varepsilon_1V}}\textbf{f}(\textbf{r})e^{-i\omega_ct}+c.c.$     (10)
normalized with respect to the energy   $\hbar\omega_c=\frac{1}{2}\int[\varepsilon_0\varepsilon_1(\textbf{r})E^2(\textbf{r},t)+\mu_0{\textbf{H}}^2(\textbf{r},t)]d\textbf{r}$                  (11)
$=\dfrac{\hbar\omega_c}{\epsilon_1V}\int\varepsilon(\textbf{r})|\textbf{f}(\textbf{r})|^2d\textbf{r}$                                                                                                                   (12)
假設為非色散介質，可得其模態體積遵循"共振光譜形狀"  $V=\dfrac{1}{\varepsilon_1}\int\varepsilon(\textbf{r})|\textbf{f}(\textbf{r})|^2d\textbf{r}$            (13)
假設為損耗腔體，公式(8)的dirac分布會改成每角頻率的模態密度$N(\omega)$ (unit: $s\cdot{rad^{-1}}$)
進一步的變化，模態共振可以被假設成Lorentzian
$\delta(\omega-\omega_c){\to}N(\omega)=\dfrac{1}{\pi}\dfrac{\dfrac{\kappa_{cav}}{2}}{(\omega-\omega_c)^2+\dfrac{\kappa_{cav}^2}{4}}$                                                                                   (14)
where $Q=\omega_c/\kappa_{cav}$，可以簡化成$N(\omega)=\dfrac{2Q}{\pi\omega_c}\dfrac{1}{1+4Q^2(\dfrac{\omega-\omega_c}{\omega_c})^2}$                                         (15)


*Spatial Profile*
公式(9) 表示的interaction Hamiltonnian電場向量，也可以寫成$|{\langle}g,\textbf{1}|H_{cav}|e,0\rangle|^2=\dfrac{p^2\hbar\omega_c}{2\varepsilon_0\varepsilon_1V}|\textbf{u}\cdot\textbf{f}(\textbf{r})|^2$                                                                                         (16)
$\textbf{p}=p\textbf{u}$，$\textbf{u}$電偶極向量(orientation)
*Purcell factor*  利用公式(15)公式(16)，腔體貢獻對於衰減率的表示可以簡化成$\Gamma_{cav}=\dfrac{2P^2}{\hbar\varepsilon_0\varepsilon_1}|\textbf{u}\cdot\textbf{f}(\textbf{r})|^2\dfrac{Q}{V}\dfrac{1}{1+4Q^2(\dfrac{\omega_{em}-\omega_c}{\omega_c})^2}$                                                                       (17)
因此，normalized衰減率可以被寫成(同時利用公式(6) $\lambda_{em}=\dfrac{2\pi{c}}{\omega_{em}}$ )$\dfrac{\Gamma_{cav}}{n_1\Gamma_0}=\dfrac{3}{4\pi^2}(\dfrac{\lambda_{em}}{n_1})^3\dfrac{Q}{V}\dfrac{|\textbf{u}\cdot\textbf{f}(\textbf{r})|^2}{1+4Q^2(\dfrac{\omega_{em}-\omega_c}{\omega_c})^2}$                                                                          (18)

###### 2.1.1 Summarize
腔體貢獻的衰減率遵循公式(18)並改寫成$\dfrac{\Gamma_{cav}}{n_1\Gamma_0}=F_P\dfrac{|\textbf{u}\cdot\textbf{f}(\textbf{r})|^2}{1+4Q^2(\dfrac{\omega_{em}-\omega_c}{\omega_c})^2}$ 
$F_P=\dfrac{3}{4\pi^2}(\dfrac{\lambda_{em}}{n_1})^3\dfrac{Q}{V}$，Purcell Factor
$\textbf{f}(\textbf{r})$表示位置依賴性（從節點處的抵消到波腹處的最大效應），分母 $[{1+4Q^2(\dfrac{\omega_{em}-\omega_c}{\omega_c})^2}]$顯示了發射頻率和腔體共振之間的失諧(detuning)效應。
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
電場向量和模態密度可以以下公式表示$\hat{\textbf{E}}(\textbf{r})=i\sqrt{\dfrac{\hbar\omega_c}{2\varepsilon_0\varepsilon_1A_{eff}L}}\textbf{f}(\textbf{r})\hat{a}+h.c.$                        (21)
$A_{eff}=\dfrac{\int\varepsilon(x,z)|\textbf{E}(\textbf{r}_xz)|^2dxdz}{Max[\varepsilon_1|\textbf{E}(\textbf{r}_xz)|^2]}$                                                                                                    (22)
$N(\omega)=\dfrac{L}{\pi}\dfrac{1}{v_g}$, with $v_g=\dfrac{d\omega}{dk_g}$                                                                                                      (23)
$A_{eff}$ 代表模態有效面積，$v_g$ 被引導的模態的群速度，
$N^{2D}=\dfrac{1}{\pi{v_g}}$被引導的模態的密度
延續前面的計算，可以將Purcell Factor簡化成
$F_P=\dfrac{\Gamma_{guided}}{n_1\Gamma_0}=\dfrac{3}{4\pi}\dfrac{(\frac{\lambda_{em}}{n_1})^2}{A_{eff}}\dfrac{n_g}{n_1}$                                                                                                    (24)
光子奈米光纖附近的 Purcell 因子由群指數控制$n_g=c/v_g$和橫向限制決定$A_{eff}$
高Purcell Factor需要低群速度和(或者)高限制模態
###### 2.1.3 Purcell factor in Fabry-Perot cavity
最終考慮1D面波導，被引導的模態的密度遵循$N^{1D}=\omega/2\pi{n_{eff}}n_g$
$n_{eff}$表示模態有效index，Purcell factor可以改寫成$F_P=\dfrac{\Gamma_{guided}}{n_1\Gamma_0}=\dfrac{3}{4}\dfrac{(\frac{\lambda_{em}}{n_1})}{L_{eff}}\dfrac{n_{eff}n_g}{{n_1}^2}$           (25)
$L_{eff}=\dfrac{\int\varepsilon(z)|\textbf{E}(\textbf{z})|^2dz}{Max[\varepsilon_1|\textbf{E}(\textbf{z})|^2]}$                                                                                                                (26)
$L_{eff}$模態有效長度
###### 2.1.4 Coupling effciency(β-factor)
已介紹Purcell factor，量化電偶極與光子晶體之間的耦合強度
由於發射器可以透過各種通道（腔模式、洩漏、非輻射能量傳輸）鬆弛到其基態，因此定義腔體模態的耦合效率也很有用。這就是所謂的 β 因子$\beta=\dfrac{\Gamma_{cav}}{\Gamma_{tot}}=\dfrac{\Gamma_{cav}}{\Gamma_{cav}+\Gamma_{other}}$                (27)
$\Gamma_{tot}$是總衰減率(包含relaxation channels)
在單模腔體中，relaxation channels通常式腔體模態的衰減率$\Gamma_{cav}$和洩漏(leak)模態的耦合
通常洩漏與初始輻射率$(\Gamma_{other}\simeq{n_1}\Gamma_0)$屬於同一數量級，因此$\beta\simeq\Gamma_{cav}/(\Gamma_{cav}+n_1\Gamma_0)\simeq{F_P}/(1+F_P)$。例如，約 Fp ~ 10 的 Purcell 因子對應於耦合效率 b ~ 90%。低閾值雷射需要高 β 因子
##### 2.2 Decay rate near lossy and dispersive materials
在有損色散介質存在的情況下，衰減速率的改變可以用典型的Lorentz振盪電偶極模型來描述，也可以用完整的量子來描述來描述。在這兩種情況下，這都會導致速率修改的以下表達式
$\dfrac{\Gamma_u(\textbf{r})}{n_1\Gamma_0}=\dfrac{6\pi}{n_1k_0}Im[g_{uu}(\textbf{r,r},\omega_{em})]$                                                                                                 (28)
G為發射器環境相關的Green's tensor，$G_{uu}$代表沿電偶極對角線分量$\textbf{u}$
此表達式量化了複雜環境中衰減率的變化，並確定電漿奈米結構對螢光衰減率影響。公式(28)是Fermi's golden rule則對色散和有損耗環境的推廣。事實上，Fermi's golden rule(4)可以改寫為$\Gamma(\textbf{r})=2\pi{g^2}(\textbf{r},\omega_{em})N(\omega_{em})$                                                                                             (29)
$\hbar{g}(\textbf{r},\omega_{em})=|\langle{a,\textbf{1}}|H_{cav}|b,0\rangle|$                                                                                                       (30)
$=\sqrt{\dfrac{\hbar{\omega_c}}{2\varepsilon_0\varepsilon_1V}}|\textbf{p}\cdot\textbf{f}(\textbf{r})|$                                                                                                                    (31)
g耦合強度，$N(\omega)$模態密度，
從散射形式可以知道，部分局部態密度 (partial local density of states, P-LDOS) 與格林二元組(Green's dyad)有關（單位：$s\cdot{m^3}$）$\rho_u(\textbf{r},\omega_{em})=\dfrac{k_0^2}{\pi\omega}Im[G_{uu}(\textbf{r},\textbf{r},\omega_{em})]$                               (32)
因此在非吸收介質中，公式(4)和公式(28)完全相等；自cQED角度，P-LDOS也可以改寫成$\rho_u(\textbf{r},\omega)=\dfrac{f_u(\textbf{r})}{2\epsilon_1V}N(\omega)$                                                                                                                  (33)
P-LDOS掌握了腔體模態$f_u(\textbf{r})$和可用光發模態$\rho(\omega)=N(\omega)/V$間的耦合之空間獨立，每單位角頻率和單位體積

#### SEC3 Plasmonic addressing and control of optical nanosource
談論電漿Purcell Factor前，簡介一下耦合發射極-SPP 配置的一些預期應用，這裡只談主要應用，並請讀者參考文獻以獲得更完整的描述。
##### 3.1 Surface enhanced spectroscopies
Surface enhanced Raman spectroscopy(SERS)大概是分子材料和電漿奈米結構間耦合的首個應用，也是新應用在單分子級，故預測出超靈敏化學品或生物感測。在這階段的Purcell factor，會談論SERS效率會遵循LSP特性的$\propto{Q}^2/V$原則
在 SERS 之後，金屬增強螢光導致增強因子達到了數十倍，可能應用於奈米治療診斷。螢光的增加是由於激發場增強和發射速率改變(Purcell effect)造成。然而，由於向金屬奈米結構的非輻射能量轉移，區分輻射速率和非輻射速率至關重要。最後，關鍵參數是發射體的量子產率，因此總增強通常受螢光分子固有量子產率的限制。值得注意的是，將發射器與等離子體奈米結構耦合，不僅為控制光物理過程開闢了道路，特別是閃爍效應和光漂白，還可以改變磁場與光子之間的比例。
##### 3.2 Nano-optical antennas
Since a plasmonic nanostructure efficiently interfaces a single molecule to far-field radiation the concept of optical nano-antenna has emerged a decade . Optical nano-antennas rely on plasmonics nanostructures to efficiently redirect the fluorescence emission and cQED-like description gives an insight of the coupling mechanism. Recently, a Purcell factor up to 1000 keeping a reasonable quantum yield and with a collection efficiency of 84% was demonstrated. Moreover, optical nano-antenna could efficiently interface molecular fluorescent emission and a nanophotonic waveguide with possible applications to realize a platform for quantum optics. In addition, coupling a single photon source to an optical nano-antenna permits control of its emission cadency. Realization of indistiguishable single photons is also a major issue.
SPP SPASER感覺較無關我第一篇的內容，先略
過

##### Dipole-dipole coupling
Finally, since an emitter can be efficiently coupled to a surface plasmon, it has been proposed to use plasmon to couple two emitters for applications such as long range resonant energy transfer (above 10 nm) or qubits entanglement.
In the following, we discuss the **plasmonic Purcell factor for typical configurations**. We first consider the well-known case of extended metal film that is the simplest case of delocalized **SPP** enabling to clearly identify the coupling mechanisms.              

#### SEC4 Quantum emitter decay rate near a metal mirror
--還沒讀完

#### Conclution
In this work, we transposed the cQED Purcell factor to plasmonics. 
	cQED應用在電漿學
The Purcell factor characterizes the capability of a structure to modify and control the emission of a nearby emitter. 
	Purcell Factor表徵了一個結構改變和控制附近發射體發射能力的特性
Both optical cavity and plasmon modes present high Purcell factors that favor efficient excitation by a dipolar emitter. 
	光學腔和電漿模態都具有高Purcell Factor，利於電偶極發射體的有效激發
However it originates from <mark style="background: #FFB86CA6;">high quality factors</mark> in case of optical cavities (but diffraction limited confinements) and on <mark style="background: #FFB86CA6;">strongly subwavelength confinements</mark> for plasmonics (but low quality factors). 
	然而，在光學腔的情況下，這源於<mark style="background: #FFB86CA6;">高Purcell Factor（但受Diffraction限制）</mark>；而在電漿體學中，則源於<mark style="background: #FFB86CA6;">強烈的亞波長約束（但具有低Purcell Factor）</mark>。
Therefore the Purcell factor reveals the new paradigm opened by quantum plasmonics for achieving efficient light–matter interaction at the nanoscale. 
	因此，Purcell Factor揭示了量子電漿體學在實現nano尺度上高效光物質相互作用方面開闢的新範式
This permits a scale law approach profiting from the strong maturity of cQED concepts and adapt them to nanophotonics. 
	這允許採用標度定律方法，利用腔量子電動力學概念的成熟性並將其應用於nano光子學
We also discussed the presence of losses that are inevitable at the nanoscale. 
	我們還討論了在nano尺度上不可避免的損耗問題
The Purcell factor includes <mark style="background: #FF5582A6;">Ohmic losses</mark> that are inherent to the excitation of plasmon in real metal so that it has to be manipulated with care. 
	Purcell Factor包含歐姆損耗，這是在真實金屬中激發電漿體所固有的，因此需要謹慎處理
In the particular case of plasmonic waveguides, the coupling efficiency to a guided mode is not affected by propagation losses. 
	特別是在電漿波導的情況下，耦合到導模的效率不受傳播損耗的影響
Obviously, only low loss systems such that crystalline nanowires or nano-platelets would permit realistics applications. 
	顯然，只有像晶體nano線或nano片這樣的低損耗系統才能實現實際應用
Finally, hybrid plasmonic/nanophotonic configurations would profit from the concept of Purcell factor through a common description of the coupling mechanism.
	最後，混合型電漿體/nano光子配置將通過對耦合機制的統一描述，從Purcell Factor概念中獲益。

光學腔和電漿體在實現高效光物質相互作用時的不同機制：前者依賴高品質因子，後者依賴強烈的亞波長約束。儘管存在歐姆損耗等限制，但通過適當的系統設計（如晶體奈米線）和混合配置，這一概念可以為奈米光子學的實際應用開闢新的途徑




