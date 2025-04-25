**Introduction**

Nanophotonics enables light-matter interactions at the nanoscale, down to single-photon/single-atom levels. Applications range from nano-optical imaging, environmental sensing, and healthcare diagnostics to the miniaturization of photonic components for integrated ultrafast devices. However, due to the mismatch between the optical cross-section of molecules and the diffraction-limited focus area of light beams, enhancing light-matter interaction remains challenging.

Strategies to enhance such interactions include:

1. Increasing absorption cross-section by lowering temperature.
2. Extending interaction duration using optical microcavities with high quality factors.
3. Confining excitation beams below the diffraction limit using near-field optics or plasmonics.

The Purcell factor (Fp) quantifies emitter-cavity coupling efficiency and is crucial for controlling spontaneous emission rates. High Purcell factors can be achieved by either high quality factors (Q) or low modal volumes (V).
奈米光學技術使光與物質的相互作用能夠達到單光子/單原子層級的奈米尺度，應用範圍涵蓋奈米光學成像、環境感測與健康診斷，以及光子元件的小型化與高速化。然而，由於分子光學截面與光束繞射極限焦點面積之間的不匹配，提升光與物質的交互作用仍面臨挑戰。

提升光與物質交互作用的策略包括：
1. 降低溫度以增加吸收截面。
2. 使用具有高品質因子的光學微腔來延長交互作用時間。
3. 利用近場光學或電漿子技術將激發光束侷限於繞射極限以下。

Purcell 因子（Fp）量化了發射源與腔體之間的耦合效率，是控制自發輻射速率的關鍵參數。高 Purcell 因子可以透過高品質因子（Q）或低模態體積（V）來實現。



---

#### Objective

This study aims to:

1. Analyze the Purcell factor in plasmonic systems, both delocalized surface plasmon polaritons (SPPs) and localized surface plasmons (LSPs).
2. Derive expressions for coupling efficiency and quantify mode confinement and quality factors.
3. Explore applications in nanophotonics, such as surface-enhanced spectroscopy, nano-optical antennas, and plasmonic nanolasers.
本研究旨在：
1. 分析電漿子系統中的 Purcell 因子，包括去侷限表面電漿極化子（SPP）與局域表面電漿子（LSP）。
2. 推導耦合效率的表達式並量化模態侷限性與品質因子。
3. 探討 Purcell 因子在奈米光學中的應用，如表面增強光譜技術、奈米光學天線與電漿子奈米雷射。

---

#### Method Overview

The authors derive closed-form expressions for the Purcell factor and coupling rates by considering plasmonic resonance profiles (Lorentzian and Fano shapes). They focus on:

1. Extended metal films supporting delocalized SPPs.
2. Plasmonic waveguides.
3. Localized surface plasmons (LSPs) in nanoparticles.

The analysis involves:

- Calculating decay rates near plasmonic structures.
- Estimating quality factors and effective mode volumes.
- Quantifying coupling efficiency (β-factor) for various configurations.

作者透過考慮電漿子共振輪廓（Lorentzian 和 Fano 輪廓）推導 Purcell 因子與耦合率的封閉形式表達式。研究重點包括：
1. 支援去侷限 SPP 的金屬薄膜。
2. 電漿子波導。
3. 局域表面電漿子（LSP）於奈米粒子中的行為。

分析方法包含：
- 計算電漿子結構附近的衰減率。
- 估算品質因子與有效模態體積。
- 量化不同配置下的耦合效率（β 因子）。

---

#### Design

The study designs and models several configurations:

1. **Thick metal mirrors**: Used to understand fundamental relaxation channels (radiative, SPP, and lossy waves).
2. **Thin metal films**: These create leaky and bound SPP modes, characterized by Fano resonance profiles.
3. **Plasmonic waveguides**: Metal nanowires are modeled for strong lateral mode confinement and high Purcell factors.
4. **Localized surface plasmons (LSPs)**: The quasi-static regime for spherical nanoparticles is analyzed, with mode confinement estimated using Mie theory.
研究設計並模擬了以下配置：

1. **厚金屬鏡**：用於了解基礎的鬆弛通道（輻射波、SPP 與損耗波）。
2. **薄金屬膜**：產生洩漏與束縛 SPP 模態，並以 Fano 共振輪廓表徵其行為。
3. **電漿子波導**：模擬金屬奈米線的強側向模態侷限與高 Purcell 因子。
4. **局域表面電漿子（LSP）**：使用準靜態近似來分析球形奈米粒子的模態侷限，並透過 Mie 理論進行擴展討論。

---

#### Fabrication

(Not explicitly discussed in the document but generally involves nanostructuring metal films, waveguides, and nanoparticles using electron-beam lithography, chemical synthesis, or self-assembly techniques.)

---

#### Setup

1. **Decay Rate Measurements**: Dipolar emitters are positioned near plasmonic structures to measure total decay rates, distinguishing between radiative, non-radiative, and SPP contributions.
2. **Mode Analysis**: The spatial profile and resonance quality of plasmonic modes are analyzed using numerical methods and analytical models.
3. **Spectral Characterization**: Lorentzian and Fano resonance profiles are fitted to experimental data to derive quality factors and effective mode volumes.
1. **衰減率測量**：將偶極發射源放置於電漿子結構附近，以測量總衰減率，並區分輻射、非輻射與 SPP 貢獻。
2. **模態分析**：使用數值方法與解析模型分析電漿子模態的空間輪廓與共振品質。
3. **光譜特性化**：透過對實驗數據擬合 Lorentzian 與 Fano 共振輪廓來推導品質因子與有效模態體積。

---

#### Result

1. **Thick Metal Mirror**: The study shows that dipolar emission near a thick metal mirror leads to three relaxation channels: radiative waves, SPPs, and lossy waves. High coupling efficiency (β-factor) up to 70% is achieved for perpendicular dipoles at specific distances.
2. **Thin Metal Film**: Coupled leaky and bound SPP modes are observed, with Fano resonance profiles fitting the experimental data. Up to 93% coupling efficiency is achieved for perpendicular dipoles.
3. **Plasmonic Waveguides**: Metal nanowires exhibit strong lateral confinement, resulting in Purcell factors up to 1000 and high β-factors (~83%) for emitters near the wire surface.
4. **Localized Surface Plasmons**: For spherical nanoparticles, mode confinement is estimated, and the quasi-static approximation provides analytical expressions for Purcell factors and quality factors.
1. **厚金屬鏡**：研究顯示，偶極發射源在厚金屬鏡附近的發射會產生三種鬆弛通道：輻射波、SPP 與損耗波。對於特定距離的垂直偶極，可達到高達 70% 的耦合效率（β 因子）。
2. **薄金屬膜**：觀測到洩漏與束縛 SPP 模態耦合，並以 Fano 共振輪廓擬合實驗數據。對於垂直偶極，耦合效率可達 93%。
3. **電漿子波導**：金屬奈米線展現出強側向侷限，導致 Purcell 因子高達 1000，且波導表面附近的偶極耦合效率（β 因子）達 83%。
4. **局域表面電漿子**：針對球形奈米粒子，估算出模態侷限，並透過準靜態近似給出 Purcell 因子與品質因子的解析表達式。

---

#### Discussion

The results demonstrate that plasmonic structures can significantly enhance spontaneous emission rates via the Purcell effect. Key findings include:

1. High Purcell factors are achievable even in lossy plasmonic systems.
2. The β-factor is critical for applications such as low-threshold nanolasers and efficient single-photon sources.
3. The combination of high confinement and moderate quality factors in plasmonic systems enables room-temperature operation, unlike traditional high-Q microcavities that require low temperatures.
結果證明，透過 Purcell 效應，電漿子結構能顯著增強自發輻射速率。關鍵發現包括：

1. 即使在具有高損耗的電漿子系統中，仍能實現高 Purcell 因子。
2. β 因子對於低閾值奈米雷射與高效能單光子源等應用至關重要。
3. 電漿子系統結合高侷限性與適中的品質因子，可在室溫下運行，這與傳統高 Q 微腔需要低溫條件形成鮮明對比。


---

#### Challenge & Future Work

**Challenges**:

1. High ohmic losses in metals limit the propagation length of SPPs.
2. Accurate control of emitter positioning relative to plasmonic structures is technically demanding.
3. Distinguishing radiative and non-radiative contributions in lossy systems requires precise measurement techniques.

**Future Work**:

1. Development of low-loss plasmonic materials for improved propagation lengths.
2. Integration of plasmonic structures with photonic circuits for on-chip quantum photonics.
3. Exploration of plasmonic cavities with tunable geometries for enhanced control over light-matter interactions.
**挑戰**：
1. 金屬中的高歐姆損耗限制了 SPP 的傳播長度。
2. 精確控制發射源相對於電漿子結構的位置具有技術難度。
3. 在具有損耗的系統中區分輻射與非輻射貢獻需要精確的測量技術。
**未來工作**：
1. 開發低損耗電漿子材料以提升傳播長度。
2. 將電漿子結構與光子電路整合，用於片上量子光學。
3. 探索具有可調幾何結構的電漿子腔體，以增強光與物質的交互作用。

---
$A_{eff}=\pi{w}_0^2$
${C_0}\propto{\frac{\sigma_0}{A_{eff}}}$
$C_0=4C_0\frac{F}{\pi}$

(1) $C=\frac{g^2}{2\kappa_{cav}n_1\Gamma_0}$ ooperativity in cavity quantum electrodynamics(cQED)
	$g$         coupling rate between the atom and the cavity mode 
	$\kappa_{cav}$    cavity losses rate
	$\Gamma_0$       atom decay rate in vacuum
	$n_1\Gamma_0$   atom decay rate in the homogeneous medium of optical index $n_1$

- strong coupling regime, $g\gg\kappa_{cav}$,  $\Gamma_0(C\gg1)$ leads to a reversible energy exchange between the cavity and the atom.
- weak coupling regime, the cavity opens a new channel for the atom (irreversible) relaxtion with a decay rate:
	$\Gamma=(1+2C)\Gamma_0$
	$\Gamma_{cav}=\Gamma-n_1\Gamma_0$
	$F_P=\frac{\Gamma_{cav}}{n_1\Gamma_0}=\frac{3}{4\pi^2}(\frac{\lambda_{em}}{n_1})^3\frac{Q}{V_{eff}}$

$\frac{1}{Q}=\frac{1}{Q_{at}}+\frac{1}{Q_{cav}}$
$Q_{at}$    Q factor of the atom emission spectrum
$Q_{cav}$   Q factor of the cavity

