## 定義

Bell states（貝爾態）是量子資訊科學中最基本且最重要的<font color="#ffc000">兩量子位元最大糾纏態</font>。這四個特殊的二量子位元（qubit）量子態，也稱為<font color="#ffc000">EPR對</font>，是量子糾纏最經典的例子。其數學表達式如下：

$$|\Phi^+⟩=\frac{1}{\sqrt{2}}\left(|00⟩+|11⟩\right)$$
$$|\Phi^-⟩=\frac{1}{\sqrt{2}}\left(|00⟩ - |11⟩\right)$$
$$|\Psi^+⟩=\frac{1}{\sqrt{2}}\left(|01⟩+|10⟩\right)$$
$$|\Psi^-⟩=\frac{1}{\sqrt{2}}\left(|01⟩-|10⟩\right)$$

這四個狀態合稱為「Bell基底」，是二量子位元希爾伯特空間的正交基底[1](https://en.wikipedia.org/wiki/Bell_state)[2](https://www.quera.com/glossary/bell-state)[3](https://eitca.org/quantum-information/eitc-qi-qif-quantum-information-fundamentals/quantum-information-properties/quantum-teleportation/examination-review-quantum-teleportation/what-are-the-four-bell-basis-states-and-why-are-they-important-in-quantum-information-processing-and-quantum-teleportation/)。

## 奇偶性（Parity）

Bell states 可依據「奇偶性」分類：

- **偶數態（Even parity）**：兩個qubit測量結果相同（00或11），即 $|\Phi^+\rangle$ 和 $|\Phi^-\rangle$。
- **奇數態（Odd parity）**：兩個qubit測量結果相異（01或10），即 $|\Psi^+\rangle$ 和 $|\Psi^-\rangle$。

這種奇偶性在量子電路與測量中非常重要，例如利用CNOT閘和[[Hadamard閘]]可以創建並檢測這些奇偶性[4](https://arxiv.org/html/2401.11684v1)。

## 主要特點

- **最大糾纏**：Bell states 是「最大糾纏」的狀態，兩個qubit的測量結果完全相關（或完全反相關），無論距離多遠[1](https://en.wikipedia.org/wiki/Bell_state)[5](https://postquantum.com/quantum-computing/bell-states-cybersecurity/)。
- **隨機但相關**：單獨測量任一qubit結果是隨機的，但一旦測量其中一個，另一個的結果立即確定（同或相反，取決於是哪個Bell state）。
- **違反局域實在論**：Bell states 的測量相關性違反了經典物理的「隱變量理論」，證明了量子力學的非定域性（Bell不等式違反）[1](https://en.wikipedia.org/wiki/Bell_state)。
- **應用廣泛**：Bell states 是量子通訊（如量子密碼、量子隱形傳態、超密編碼）的基礎資源[2](https://www.quera.com/glossary/bell-state)[3](https://eitca.org/quantum-information/eitc-qi-qif-quantum-information-fundamentals/quantum-information-properties/quantum-teleportation/examination-review-quantum-teleportation/what-are-the-four-bell-basis-states-and-why-are-they-important-in-quantum-information-processing-and-quantum-teleportation/)。
- **正交且可區分**：四個Bell states互相正交，可以通過適當的量子測量完全區分。
- **對稱與反對稱**：$|\Phi^+\rangle$、$|\Psi^+\rangle$ 為對稱態(描述Boson)，$|\Phi^-\rangle$、$|\Psi^-\rangle$ 為反對稱態(描述Fermion)。

## 小結

Bell states 是二量子位元系統最具代表性的糾纏態，具有明顯的奇偶性分類和極強的量子相關性，是量子資訊與量子通訊技術的核心基礎[1](https://en.wikipedia.org/wiki/Bell_state)[2](https://www.quera.com/glossary/bell-state)[3](https://eitca.org/quantum-information/eitc-qi-qif-quantum-information-fundamentals/quantum-information-properties/quantum-teleportation/examination-review-quantum-teleportation/what-are-the-four-bell-basis-states-and-why-are-they-important-in-quantum-information-processing-and-quantum-teleportation/)[5](https://postquantum.com/quantum-computing/bell-states-cybersecurity/)。

![Bell state - Wikipedia](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/The_Hadamard-CNOT_transform_on_the_zero-state.png/500px-The_Hadamard-CNOT_transform_on_the_zero-state.png)

![A nondestructive Bell-state measurement on two distant ...](https://media.springernature.com/lw1200/springer-static/image/art%3A10.1038%2Fs41566-021-00802-1/MediaObjects/41566_2021_802_Fig2_HTML.png)

1. [https://en.wikipedia.org/wiki/Bell_state](https://en.wikipedia.org/wiki/Bell_state)
2. [https://www.quera.com/glossary/bell-state](https://www.quera.com/glossary/bell-state)
3. [https://eitca.org/quantum-information/eitc-qi-qif-quantum-information-fundamentals/quantum-information-properties/quantum-teleportation/examination-review-quantum-teleportation/what-are-the-four-bell-basis-states-and-why-are-they-important-in-quantum-information-processing-and-quantum-teleportation/](https://eitca.org/quantum-information/eitc-qi-qif-quantum-information-fundamentals/quantum-information-properties/quantum-teleportation/examination-review-quantum-teleportation/what-are-the-four-bell-basis-states-and-why-are-they-important-in-quantum-information-processing-and-quantum-teleportation/)
4. [https://arxiv.org/html/2401.11684v1](https://arxiv.org/html/2401.11684v1)
5. [https://postquantum.com/quantum-computing/bell-states-cybersecurity/](https://postquantum.com/quantum-computing/bell-states-cybersecurity/)
6. [https://www.aliroquantum.com/blog/what-are-bell-states](https://www.aliroquantum.com/blog/what-are-bell-states)
7. [https://pennylane.ai/qml/glossary/what-are-bell-states](https://pennylane.ai/qml/glossary/what-are-bell-states)
8. [https://www.quantiki.org/wiki/bell-state](https://www.quantiki.org/wiki/bell-state)
9. [https://qmunity.thequantuminsider.com/2024/07/25/what-are-quantum-bell-states/](https://qmunity.thequantuminsider.com/2024/07/25/what-are-quantum-bell-states/)
10. [https://arxiv.org/abs/2401.11684](https://arxiv.org/abs/2401.11684)
11. [https://www.linkedin.com/pulse/quantum-recipes-bell-states-anthony-massobrio-hsmnf](https://www.linkedin.com/pulse/quantum-recipes-bell-states-anthony-massobrio-hsmnf)
12. [https://pubs.aip.org/aip/apq/article/1/2/026103/3282746/Generating-magnon-Bell-states-via-parity](https://pubs.aip.org/aip/apq/article/1/2/026103/3282746/Generating-magnon-Bell-states-via-parity)
13. [https://www.numberanalytics.com/blog/ultimate-guide-to-bell-states](https://www.numberanalytics.com/blog/ultimate-guide-to-bell-states)
14. [https://zh.wikipedia.org/zh-tw/%E8%B2%9D%E7%88%BE%E6%85%8B](https://zh.wikipedia.org/zh-tw/%E8%B2%9D%E7%88%BE%E6%85%8B)
15. [https://www.mdpi.com/2076-3417/13/23/12907](https://www.mdpi.com/2076-3417/13/23/12907)
16. [https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Quantum_Tutorials_(Rioux)/08:_Quantum_Teleportation/8.53:_Bell_State_Exercises](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Quantum_Tutorials_\(Rioux\)/08:_Quantum_Teleportation/8.53:_Bell_State_Exercises)
17. [https://ithelp.ithome.com.tw/m/articles/10332882](https://ithelp.ithome.com.tw/m/articles/10332882)
18. [https://link.aps.org/doi/10.1103/PhysRevB.87.081305](https://link.aps.org/doi/10.1103/PhysRevB.87.081305)
19. [https://qubit.guide/5.7-bell-states](https://qubit.guide/5.7-bell-states)
20. [https://www.researching.cn/articles/OJbfc4e1e19616be4f](https://www.researching.cn/articles/OJbfc4e1e19616be4f)