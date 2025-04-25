---
Paper:
  - "[[007-A scheme for efficient quantum computation with linear optics]]"
Page: 1/7
Paragraph:
---
>Quantum information processing (QIP) uses quantum mechanics for information storage, communication and computation. It enables large improvements in computational effciency and communication security by exploiting the superposition principle and non-classical correlations of quantum mechanics. Examples include Shor's quantum algorithm for factoring large integers, Grover's algorithm for accelerating combinatorial searches and quantum cryptography for secure communication. Initial concern that quantum coherence may be too fragile to be exploited has been dispelled by theoretical work showing that noise and decoherence are not fundamental obstacles to the implementation of QIP. Consequently, increasing effort is being devoted towards physically realizing quantum computers, and there are many proposals for implementing the necessary quantum devices. Examples of promising technologies include ion traps, quantum dots, Josephson junctions, nuclear spins in silicon and nuclear spins in molecules.

|       |                                                                                                                 |
| ----- | --------------------------------------------------------------------------------------------------------------- |
| 主旨    | 量子資訊處理QIP使用量子力學做為資料儲存，通訊與計算。                                                                                    |
| QIP優勢 | 以疊加原理和非典型相關性提高計算效率和通訊安全性                                                                                        |
| QIP應用 | 分解大整數的Shor量子演算法、加速組合搜尋用Grover演算法、安全通訊的量子密碼學                                                                     |
| QIP誤解 | 噪音和非同調不是QIP的根本障礙                                                                                                |
| QIP前景 | 離子阱(ion traps)、quantum dots、%Josephson junction、%矽原子核自旋(nuclear spins in Si)、%分子核自旋(nuclear spins in molecules) |

>Quantum effects are particularly easy to observe in optical systems, and it is therefore not surprising that one of the earliest proposals for QIP uses photons to implement quantum logic. Optical systems currently constitute the only realistic proposal for long-distance quantum communication and underlie experimental implementations of quantum cryptography. Until now the main obstacle to scalable optical QIP was the apparent need for nonlinear couplings between optical modes. Achieving such couplings at suffcient strengths is possible in principle but is technically diffcult. As a result, other proposals for using linear optics to benchmark quantum algorithms require exponentially large physical resources.

|     |                                                                                   |
| --- | --------------------------------------------------------------------------------- |
| 主因  | 光學系統中很容易觀察到量子效應，故QIP最早方案之一是 用光子實現量子邏輯<br>光學系統是目前(2001)可實現長距離量子通訊的方案<br>量子密碼學的實驗基礎 |
| 困境  | 光學模態之間的非線性耦合是可擴展光學QIP的一大困境(理論可行，技術困難)                                             |
| 需求  | 指數級成長的物理資源                                                                        |

>Here we show the surprising result that linear optics is suffcient for effcient QIP with photons. Effciency in the sense of the theory of computation means with polynomial resources, and we achieve low linear resources. Our proposal for QIP with linear optics requires single photon sources (implementable with active linear optics), beam splitters, phase shifters, photo-detectors, and feed-back from photo-detector outputs. A quantum bit (qubit) is realized by one photon in two optical modes (such as horizontal or vertical polarization). Effcient QIP is established by means of three results, each of which constitutes a breakthrough in linear optics QIP. The first result implies that non-deterministic quantum computation is possible with linear optics. It is based on a nonlinear sign shift between two qubits that uses two additional photons and post-selection. The sign shift succeeds with probability 1/16, and whether or not it succeeded is known. Although there are no practical applications of non-deterministic quantum computation, it implies that linear optics has features not available to classical deterministic or probabilistic computation. The second result shows that the probability of success of the quantum gates can be increased arbitrarily close to one. The result is based on using entangled states prepared non-deterministically and quantum teleportation. Thus quantum computation is possible in principle with linear optics. The resources needed to make the probability of success close to one with these methods are extremely demanding. The third result shows that with quantum coding, the resources for obtaining accurate encoded qubits are very effcient with respect to the accuracy achieved, thus completing the goal of effcient linear optics quantum computation (LOQC). The coding methods can be adapted to make LOQC fault-tolerant for photon loss, detector ineffciency and phase decoherence. As a result, LOQC can be robustly implemented with resources low enough to suggest practical scalability, making it as promising a technology for QIP as are other proposals.

|           |                                                                                                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 總結        | 線性光學可以實現光子的有效QIP                                                                                                                                                          |
| 需求        | 單光子源(用主動線性光學系統)、分束器、移相器、光電探測器、來自光電探測器輸出的回饋                                                                                                                                |
| 方法        | 量子位元（qubit）是由一個光子在兩種光學模式（如水平或垂直偏振）下實現<br>透過三個結果建立了高效的QIP                                                                                                                  |
| 第一種       | 線性光學可以實現非確定性量子計算<br>-基於兩個量子位元之間的非線性符號偏移，使用了兩個額外的光子和後選擇。符號轉換成功的機率為 1/16，並且可知成功與否<br>-非確定性量子計算沒有實際應用，但證實線性光學具有經典確定性或機率計算所不具備的特性                                             |
| 第二種       | 結果顯示量子閘的成功機率可以任意增加到接近於一<br>基於使用非確定性準備的糾纏態和量子隱形傳態<br>利用線性光學可以實現量子計算，使這些方法的成功機率接近 1 所需的資源相當苛刻                                                                               |
| 第三種(高度期望) | 透過量子編碼，獲得精確編碼量子位元的資源相對於所達到的精度是非常高效的，從而完成了高效線性光學量子計算（LOQC）的目標<br>可以調整編碼方法以使 LOQC 對光子缺失、偵測器效率低和相位非同調性具有容錯能力<br>LOQC 可以在資源足夠低的情況下穩健地實施，從而具有實際的可擴展性，這使得它與其他提案一樣，成為 QIP 有前途的技術 |
|           | @不愧是4000+引用的論文，光看這邊就很厲害，但沒辦法吸收                                                                                                                                            |

