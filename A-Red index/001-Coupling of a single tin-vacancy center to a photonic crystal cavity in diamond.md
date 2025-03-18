---
Cite as: Appl. Phys. Lett. 118, 230601 (2021)
DOI: 10.1063/5.0051675
Submitted: 26 March 2021
Accepted: 4 May 2021
Author:
  - "[[Kazuhiro Kuruma]]"
  - Benjamin Pingault
  - Cleaven Chia
  - Dylan Renaud
  - Patrick Hoffmann
  - Satoshi Iwamoto
  - Carsten Ronning
  - "[[Marko Lončar]]"
tags:
  - coupling
  - ZPL
  - color_center_in_Diamond
  - red_index
Source from: LINE-QNO Group
---
#### Related links
- [[Kazuhiro Kuruma]]
- [[Group Ozeki]]
- [[Marko Lončar]]
- [[yet-Tin-Vacancy Color Centers in Diamond]]
- [[Coupling of a single tin-vacancy center to a photonic crystal cavity in diamond.pdf]]
---
#### ABSTRACT
We demonstrate optical coupling between a <mark style="background: #FFB8EBA6;">single tin-vacancy (SnV) center in diamond</mark> and a <mark style="background: #FFB8EBA6;">free-standing photonic crystal nanobeam cavity</mark>.
The cavities are fabricated using <mark style="background: #BBFABBA6;">quasi-isotropic etching</mark> and <mark style="background: #BBFABBA6;">feature experimentally measured quality factors as high as 11000</mark>. 
We investigate the dependence of a single SnV center’s emission by <mark style="background: #D2B3FFA6;">controlling the cavity wavelength</mark> using a laser-induced gas desorption technique. 
Under resonance conditions, we observe an intensity enhancement of the SnV emission by a factor of 12 and a 16-fold reduction of the SnV lifetime. 
Based on the large enhancement of the SnV emission rate inside the cavity, we estimate the Purcell factor for the SnV zero-phonon line to be 37 and the coupling efficiency of the SnV center to the cavity, the b factor, to be 95%. 
Our work paves the way for the realization of quantum photonic devices and systems based on efficient photonic interfaces using the SnV color center in diamond.
#### KEYWORD
- **材料與系統**
    -  single tin-vacancy (SnV)
    - Photonic crystal(PhC) cavity
    - Nanobeam cavity
    - Diamond-based quantum systems
    - Single-photon emitters
- **光學與物理性質**
    - Purcell factor
    - Quality factor (Q factor)
    - Zero-phonon line (ZPL)
    - Spin-photon interface
- **製程技術**
    - Ion implantation
    - Quasi-isotropic etching
    - Electron beam lithography
    - Reactive ion etching (RIE)
    - Gas tuning technique
    - Photoluminescence (PL) measurements
- **量子資訊應用**
    - Quantum photonic devices
    - Quantum networks
    - Efficient photon sources
    - Spin coherence
- **相關參數與特性**
    - Coupling efficiency (β factor)
    - Lifetime reduction
    - Strain effects
    - Spectral alignment
    - High-Q/V cavity designs

#### 簡述
**色心優勢 (color center)**
	- 單光子自旋
	- 量子記憶體
>*Color centers in diamond are promising solid state quantum emitters, of interest for realization of single photon sources1 and quantum memories leveraging their long-lived spins.*

**NV目前研究最多**
	**缺點** (易有雜訊的意思？)表面外部電場高敏度(*high susceptibility to external electric field fluctuations from surface*)
		- zero-phonon line (ZPL) emission(*~3% of total emission*)
		- unstable (*blinking, spectral diffution, etc.*)
--> **漸漸研究3-5族元素色心**
	- **優勢**  stable & large ZPL emission, even inside nanosructures
	- **aim**  抑制光子在基態能代之間引起的**自旋退相干** (*suppress spin decoherence caused by phonon-induced transitions between ground state levels*)
	- **op.**  **for SiV GeV**
		- 超低操作溫度mK
		- 靜應變環境 
		- (*SiV and GeV centers require operation at mK or under static strain*)
	- **op. for SnV**
		- 基態更加分裂 ->  長自旋相干時間(at 1K) 
		- (*SnV centers have a much larger splitting between these levels (850 GHz) and can, thus, support long spin coherence times at 1 K*)
		- from another paper, as SnV at 2.9K, the spin coherence time~10 ms


**以下便是透過更種方法做出高效SnV**

**main purpose** take advantage of the full potential 
->**inderect purpose** realize an efficient spin-photon interface for SnV
	- <mark style="background: #FFF3A3A6;">improve the ZPL collection efficincy</mark>
	- <mark style="background: #FFF3A3A6;">enhance the coherent ZPL emmision</mark>
	**method** 
		- using optical micro/nanocavities with high quality (Q) factors.
			- Photonic crystal (PhC) nanocavities are particularly promising platforms 
			- **adv.** enhancing the light–matter interaction
				- high Q factors
				- small mode volumes (V)
				- high-frequency (10 GHz) & high-Q mechanical modes
					-> realize spin–phonon interfaces

---
**short summery**
	report on optical coupling of a single SnV center to a PhC nanobeam cavity in diamond. 
	We use a quasi-isotropic undercut method to fabricate free-standing PhC nanobeam cavities in bulk diamond crystal, featuring Q factors as high as 11 000.
	Next, we select a cavity (Q  3000) with a good coupling to a single SnV center, introduced via ion-implantation, and tune the cavity into resonance with the SnV center using a laser-induced gas desorption technique. 
	At resonance, we observe a strong enhancement of the SnV emission intensity by a factor of 12 and a 16-fold reduction in the SnV lifetime (compared to centers in bulk). 
	Due to the significant enhancement of the spontaneous emission rate, we estimate a Purcell factor for the SnV ZPL of 37 and a near-unity cavity coupling efficiency b (probabil-ity of emitted photons being channeled into the cavity mode) of 95%. 
	These results provide a step toward the development of quantum information processing devices, including efficient quantum light sources, and the creation of spin–photon interfaces using single SnV centers coupled to high-Q PhC cavities.

---
#### structure
**basic**  diamond-cubic PhC nanobeam cavity
**waveguide**
	- width(w)  330nm
	- thickness(d)  170nm
	-  airhole radius(r)  65 nm
	-  lattice constant (a) ranges from 188 to 196 nm, used 196 nm ( a1=0.84a, a2=0.844a, a3=0.858a, a4=0.88a, a5=0.911a,and a6=0.951a)
	- quality factor (Q) 6x10^5
	- mode volume ~0.42($\lambda/n)^3$  (calculated by 3D finite-difference time domain, where refractive index of diamond slab(n) is 2.4)
	- 1(a) design 1(b) SEM

---
#### tech
01. **Surface Damage Removal via Argon/Chlorine and Oxygen Plasma Etching**
	The surface damage caused by polishing was removed using argon/chlorine etching followed by oxygen plasma etching.
02. **Tri-Acid Cleaning and Tin (117Sn) Ion Implantation**
	The sample was cleaned by immersion in a 1:1:1 boiling tri-acid mixture (perchloric, nitric, and sulfuric acids) for one hour, followed by tin (117Sn) ion implantation at an energy of 350 keV. The mean ion range was approximately 86 nm with a straggling of 17 nm, as simulated using the SRIM software.
03. **Low Ion Fluence for Single SnV Center Optical Experiments**
	Ion implantation fluence of 2×10102 \times 10^{10}2×1010 ions/cm² was used to prepare for optical experiments with a single SnV center.
04. **Tilted Implantation to Avoid Channeling Effects**
	The sample was tilted by 7° during implantation to avoid channeling effects.
05. **Post-Implantation Tri-Acid Cleaning**
	The sample underwent tri-acid cleaning again after ion implantation.
06. **Annealing at 1200°C to Form SnV Complexes**
	The sample was annealed at 1200°C for approximately 5 hours to mobilize vacancies and form SnV complexes with the implanted tin atoms.
07. **Final Tri-Acid Cleaning**
	A final tri-acid cleaning was performed after annealing.
08. **Fabrication of Free-Standing PhC Nanobeam Cavities via EB Lithography and Dry Etching**
	Free-standing photonic crystal (PhC) nanobeam cavities were fabricated using a combination of electron beam (EB) lithography and dry etching processes.
09. **Deposition of 100 nm SiN Layer via PECVD**
	A 100 nm-thick SiN layer was deposited on the bulk diamond using plasma-enhanced chemical vapor deposition (PECVD).
10. **EB Lithography to Define Cavity Structure on 400 nm EB Resist**
	Electron beam lithography was used to define the cavity structure on a 400 nm-thick EB resist (ZEP-520A).
11. **ICP-RIE Etching of SiN Mask with SF6 and C4F8 Gases**
	The SiN mask layer was etched using induced coupled plasma reactive ion etching (ICP-RIE) with SF6 and C4F8 gases.
12. **Pattern Transfer to Diamond via Oxygen Plasma RIE**
	The cavity pattern was transferred onto the diamond substrate using oxygen plasma reactive ion etching (RIE).
13. **Al2O3 Deposition and RIE Etching for Conformal Coverage**
	A 20 nm-thick Al2O3 layer was deposited by atomic layer deposition for conformal coverage of the sample and then etched using RIE while keeping the nanobeam sidewalls covered with Al2O3.
14. **Quasi-Isotropic Undercut Technique for Free-Standing Cavities**
	A quasi-isotropic undercut technique using oxygen-based RIE was employed to realize free-standing cavity structures.
15. **Removal of SiN and Al2O3 Layers via Hydrofluoric Acid**
	The SiN and Al2O3 layers were removed by immersion in hydrofluoric acid (HF).
---
#### Figure
01. We used a diamond based PhC nanobeam cavity, as schematically shown in Fig. 1(a). 
02. Figure 1(b) shows the cavity design, overlaid with the calculated electric field (Ey) distri-bution of the fundamental cavity mode.
03. Figure 1(c) shows the scanning electron microscope (SEM) image of one of the fabricated nanobeam cavity. 
04. Figure 1(d) shows a PL spectrum for the fundamental cavity mode with the highest Q factor among 153 measured cavities.
05. Figure 2(a) shows the PL spectra taken under various cavity-SnV detunings.
06. Figures 2(b) and 2(c) show PL spectra under off-resonance ($\Delta=$-1.0 nm) and on-resonance ($\Delta$ ~ 0 nm) condi-tions. 
07. Figure 3(a) shows the measured PL decay curves with five different detunings of $\Delta=$ 0.88 nm, 0.38 nm, 0.27 nm, 0.17 nm, and ~ 0 nm.
08. The extracted emission rates of the PL curves are plotted in Fig. 3(b),showingaclear enhancement of the spontaneous emission rate of the SnV near reso-nance. 提取的PL曲線的發射率如圖3(b)所示，顯示SnV在共振附近的自發發射率明顯增強。
09. Figure 3(c) shows the inten-sity correlation histogram measured when the SnV is slightly detuned from the cavity resonance by 0.23 nm (see inset).

---
#### aynalization
We excited the sample with a 520 nm continuous wave diode laser, and the PL signal from the sample was collected through an objective lens (Olympus MPLFLN, 100 magnification and 0.9 NA) and analyzed by a spectrometer (Princeton Instruments) equipped with a Si CCD camera.

#### measurent
By fitting the spectrum with a Lorentzian function (red line), the measured Q was deduced to be ~**11 000**, which is comparable to that of visible-wavelength nanobeam cavities realized by quasi-isotropic etching


### Optical coupling(single SnV center and a nanobeam cavity)
#### investigation
we investigated the **optical coupling** between a **single SnV center and a nanobeam cavity with a= 196 nm**. The measured Q factor of the cavity was ~**3000**. 
The cavity was tuned in and out of resonance with a single SnV ZPL transition at **624 nm** using the gas tuning method discussed below.
 **620nm to 624nm：**
	 The longer wavelength of this SnV compared to the usual 620 nm reported in other works, is due to **residual strain, induced by the ion implantation and/or the fabrica-tion**. <mark style="background: #FF5582A6;">Unstrained SnV centers were also present in cavities, but single ones could not be spectrally isolated. </mark>

**線寬低於儀器設備極限**
	The linewidth of the SnV emission is below the spectral resolution limit of our spectrometer (~10 GHz). 

奈米束腔中的 SnV 發射並未超過儀器的**光譜儀分辨率**的大光譜偏移，這表明 SnV 中心適合整合到奈米光子結構中
	Note that the SnV emission in the nanobeamcavity **did not exhibit** any large spectral shifts over our spectrometer resolution through the whole experiment, suggesting the suitability of SnV centers for integration into nanophotonic structures.

控制$\Delta$：使用<mark style="background: #FF5582A6;">聚焦雷射激發的局部加熱的氣體調諧技術</mark>
 For the control of the detuning between the SnV and the cavity wavelengths ($\Delta=\lambda_{SnV}-\lambda_{cavity}$ ) , we employed a **gas tuning technique based on local heating using focused laser excitation**.
	**method**
		 - After injecting the N2 gas in the cryostat chamber, the gas condenses on the cavity resulting into a red-shift of the cavity wavelength over the target SnV emission. 
		 - used high excitation powers (>1 mW) of the CW laser at 520 nm to locally heat the cavity close to its center
	**result**
		results in the desorption of the N2 gas from the sample and enables a controlled blue-shift of the cavity wavelength. 
	**調變項**
		$\Delta$ can be controlled by varying the **laser power** and **excitation time**. It is noteworthy that we **did not see significant changes in the Q factors during the gas tuning**

**as the cavity is resonant with the SnV emission 腔體&SnV共振**
	**Purcell effect**造成自發性輻射率增加12倍

**estimation of the enhancement factor**
	**method**
		compared the **peak area under the Lorentzian fit curves** of the SnV emission in the **on-** and **off-** resonance cases.
	**result**
		We note that out of 32 cavities we measured, all featuring the same a and typical Q factor >103, only one could be tuned on- and off-resonance with a spectrally isolated single SnV center. 
		**reason**
			This low yield is mainly because many cavities contain multiple SnV emitters with close or overlapping ZPL emissions, or the cavity-SnV wavelength detuning is large.
		測量的 32 個空腔中，所有空腔都具有相同的 a 和典型 Q 因子 >1000，只有一個空腔可以透過光譜隔離的單一 SnV 中心進行**調諧和失諧振**。
		這種**低產率**主要是因為許多腔體包含多個具有接近或重疊ZPL發射的SnV發射器，或腔體-SnV波長失諧很大。
	**solution for yield**
		 increase the yield of devices with good SnV-cavity coupling
			 needed to employ **ion implantation with lower doses** and **lower energies**, to **reduce the number of centers per cavity and residual strain**, as well as employ **techniques with precise spectral and spatial alignment of cavities with respect to single color centers**.

**one of result**
We also carried out time-resolved PL measurements on the same SnV for different values of the SnV-cavity detuning. We excited the sample using a supercontinuum laser (SuperK EXTREME) with a cen-tral wavelength of 535 nm, pulse width of 100 nm, and a repetition rate of 9.74 MHz. The averaged pump power was fixed to 300 lW. Spectral filtering of the SnV emission was performed using a home-made monochromator.
對相同 SnV 的不同 SnV 腔失諧值($\Delta$)進行了時間分辨 PL 測量。我們使用中心波長為 535 nm、脈衝寬度為 100 nm、重複率為 9.74 MHz 的超連續譜雷射 (SuperK EXTREME) 激發樣品。平均泵浦功率固定為 300 lW。 SnV 發射的光譜過濾是使用自製的單色儀進行的。

濾波後的訊號被傳送到雪崩光電二極體（APD、Excelitas SPCM）並由單光子計數模組（PicoHarp 300）進行分析。我們系統的時間分辨率測量為 600 ps。
The filtered signal was sent to an avalanche photodiode (APD, Excelitas SPCM) and analyzed by a single photon counting module (PicoHarp 300). The time resolution of our system was measured to be 600 ps. 

正如預期的那樣，SnV 的發射壽命隨著失諧變小而縮短。我們用一個或兩個指數函數與高斯響應函數和我們系統的時間解析度進行卷積來擬合 PL 曲線。
As expected, the emission lifetime of the SnV is reduced as the detuning becomes smaller. We fitted the PL curves with one or two exponential functions convolved with the Gaussian response function with our system’s time resolution.

（$\gamma_{on}$）**0.38 ns**/  **16 倍**（使用圖 3(a) 中的黑點繪製）/共振時的 PL 曲線緩慢衰減 **4.6 ns**/ 源自於**裸腔發射**，透過測量遠失諧條件下的腔室壽命證實為**4.4 ns**
 the fastest lifetime, near zero detuning (on-resonance, $\gamma_{on}$), is **0.38 ns**, which is approximately **16 times** faster than that measured for SnV in bulk (plotted using black dots in Fig. 3(a)). We noticed that the PL curve at resonance also exhibits a slow decay with a lifetime of 4.6 ns. This slow decay component mainly originates from the **bare cavity emission**, which was confirmed by measuring the cavity lifetime under a far-detuned condition to be 4.4 ns.

ZPL (FpZPL) 的 Purcell 因子
From the extracted lifetimes, we estimate the Purcell factor of the investigated ZPL (FpZPL) using the following equation
$F_{p}^{ZPL}=\frac{(\gamma_{bulk}/\gamma_{on}-\gamma_{bulk}/\gamma_{off})}{\xi_{ZPL}}=\frac{6.0/0.38-6.0/7.4}{0.4}\simeq{37}$
$\gamma_{bulk}=6.0ns$ ：the lifetime of SnV in bulk
$\gamma_{off}=\gamma_{0.88nm}=7.4ns$： the lifetime of SnV off-resonance

$\xi_{ZPL}$ is defined by the fraction of the total emission into the stronger of the two ZPL transitions visible at 4K for SnV in  bulk diamond (~0.4)->Debye-Waller factor of 57%(data from ''Spectroscopic investigations of negatively charged'')

該值仍然小於使用測量的 Q~3000 和 V~0.42 (k/n)^3 估計的理論 Purcell factor=362，並考慮 SnV 躍遷 <111> 的偶極矩與腔局部之間的極化失配電場<110 >
 This value is still smaller than the theoretical Purcell factor36 of 362 estimated using the measured Q~3000, and V~0.42 (k/n)3 and considering the polarization mismatch between the dipole moment of the SnV transition <111> and the cavity local electric field <110>
Purcell 因子降低的原因可能是由於注入過程的隨機性，SnV 中心相對於腔電場波腹的位置不是最佳。
The reason for the reduced Purcell factor could be a sub-optimal position of the SnV center with respect to the antinode of the cavity electric field, due to the stochastic nature of the implantation process. 
為了進一步提高 Purcell 係數，可能需要使用色心精確定位技術以及高 Q/V 腔體設計。利用開諧振和非諧振壽命，我們也獲得了 SnV 向腔模式轉變的高耦合效率，

為了進一步提高 Purcell 係數，可能需要使用色心精確定位技術以及高 Q/V 腔體設計。利用開諧振和非諧振壽命，我們還獲得了 SnV 躍遷到腔模式的高耦合效率（95%），表明從 SnV 躍遷發射的光子被引導到所研究的腔模式的機率接近一致。
$\beta=\frac{1/\gamma_{on}}{\gamma_{on}+\gamma_{off}}=95\%$
For further improvement of the Purcell factor, the use of pre-cise positioning techniques of color centers, as well as high Q/V cavity designs could be necessary. Using the lifetimes on- and off-resonance, we also obtain a high coupling efficiency of the SnV transi-tion to cavity mode, 95%, indicating a near unity probability for emitted photons from the SnV transition to be channeled into the investigated cavity mode. 


最後，為了確認所研究的 SnV 發射的單光子性質，我們使用配備兩個 APD 的 Hanbury Brown-Twiss 裝置對 SnV 躍遷進行了二階相關測量。我們使用的雷射重複率為 77.9 MHz，平均泵浦功率為 2.7 mW。圖 3(c) 顯示了當 SnV 與腔諧振稍微失諧 0.23 nm 時測量的強度相關直方圖（參見插圖）。
Finally, in order to confirm the single photon nature of the inves-tigated SnV emission, we performed second-order correlation mea-surements for the SnV transition using a Hanbury Brown–Twiss setup equipped with two APDs. We used a laser repetition rate of 77.9 MHz with an average pump power of 2.7 mW. Figure 3(c) shows the inten-sity correlation histogram measured when the SnV is slightly detuned from the cavity resonance by 0.23 nm (see inset).
零延遲時間的二階相關函數 g^2(0) 表現出明顯的反聚束，值為 0.27，證實所研究的 SnV 是單光子發射器。我們認為 g^2(0) 的非零值可能主要是由於腔內其他非共振 SnV 中心提供的背景腔發射的貢獻。為了降低g^2(0)的值，需要使用較低的離子注入劑量或確定性注入技術來大幅降低單腔內的SnV中心密度。 g^2($\tau$) 直方圖也表現出在前幾個峰上可見的聚束行為，這表明 SnV 中除了激發態和基態之外還存在擱置態。
The second-order correlation function at zero delay time, g^2(0), exhibits a clear anti-bunching with a value of 0.27, confirming that the investigated SnV is a single photon emitter. We consider that the non-zero value of g^2(0) could be primarily due to the contribution of the background cavity emission supplied by other off-resonant SnV centers inside the cav-ity. In order to reduce the value of g^2(0), it would be necessary to use lower ion implantation doses or deterministic implantation techni-ques to largely reduce the SnV center density inside a single cavity. The g^2($\tau$) histogram also exhibits a bunching behavior visible on the first few peaks, which suggests the existence of a shelving state other than the excited and ground states in the SnV.


#### SUMMERY
**證實**  
	單一 SnV 中心和 PhC 奈米束腔之間的光學耦合(optical coupling between a single SnV center and a PhC nanobeam cavity)
**特點**   cavity with a Q factor of ~3000
	-  腔諧振耦合的 SnV 發射強度明顯增強了 12 倍(intensity enhancement of the SnV emission resonantly coupled to the cavity by a factor of 12)
		->ZPL 的 Purcell 因子達到 37(Purcell factor for the ZPL of 37 )
		->腔體耦合效率 $\beta$ 高達 95%high cavity coupling efficiency $\beta$ of 95%
	-  SnV 壽命縮短了 16 倍(16-fold reduction in the SnV lifetime)
**還須改進**  
	- **Purcell factor**
		- 使用具有極小 V 和高 Q 值的腔體設計(using cavity designs with extremely small Vsandhigh Qs)
		- 使用單發射器的精確位置對準技術(using precise position alignment techniques of single emitters)
	- 使用光纖耦合和光柵耦合器的錐形波導可以大幅提高增強型單光子發射的收集效率(collection efficiency of the enhanced single photon emission can be largely improved using tapered waveguide for fiber coupling and grating couplers)
**重要性**  
	- 奈米束設計與色心轉變的應變介導的調整方法相容。(nanobeam design is compatible with strain-mediated tuning approaches of color center transitions)
	- 將這些功能納入所展示的 SnV-奈米腔耦合系統對於自旋光子介面的開發非常重要，以便未來將色心大規模整合到積體光子電路和量子網路中(The incorporation of these functionalities into the demonstrated SnV-nanocavity coupled system is important for the development of spin–photon interfaces for future large-scale integration of color centers into integrated photonic circuits and quantum networks.)


---
#### Question
01. reason why the lattice constent become bigger?(a1=0.84a, a2=0.844a, a3=0.858a, a4=0.88a, a5=0.911a,and a6=0.951a)
	In order to form the cavity, the air holes are shifted near the waveguide center quadratically
