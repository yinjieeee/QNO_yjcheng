**W-state**（W 態）是一種多體量子糾纏態，最常見的是三個量子比特（qubit）的情形，其數學表示為：$$|W\rangle = \frac{1}{\sqrt{3}} (|100\rangle + |010\rangle + |001\rangle)$$這代表三個量子比特中，只有一個處於激發態（1），其餘為基態（0），而三種可能的排列以等權重疊加[1](https://en.wikipedia.org/wiki/W_state)[3](https://www.quantiki.org/wiki/w-state)[5](https://tqsd.github.io/QuNetSim/examples/send_w.html)。

**W 態的主要特點：**

- 屬於三體糾纏的兩大代表之一（另一個是 [[Greenberger–Horne–Zeilinger state|GHZ 態]]），但兩者無法用局部操作和經典通訊（[[Local Operations and Classical Communication|LOCC]]）互相轉換[1](https://en.wikipedia.org/wiki/W_state)[5](https://tqsd.github.io/QuNetSim/examples/send_w.html)。
- **[[robustness|魯棒性]]高**：若丟失其中一個 qubit，剩下的兩個仍然保持糾纏，這與 GHZ 態完全不同（GHZ 態失去一個 qubit 後即完全可分離）[1](https://en.wikipedia.org/wiki/W_state)[5](https://tqsd.github.io/QuNetSim/examples/send_w.html)[6](https://demonstrations.wolfram.com/ThreeQubitWStatesOnAQuantumComputer/)。
- 這種魯棒性使得 W 態在量子通訊與量子記憶等應用中特別有價值[1](https://en.wikipedia.org/wiki/W_state)[8](https://www.nature.com/articles/srep16245)。
- W 態可推廣至 n 個 qubit，表示為所有只有一個 qubit 為 1，其餘為 0 的狀態的等權重疊加：$$|W\rangle = \frac{1}{\sqrt{n}} (|100...0\rangle + |010...0\rangle + ... + |00...01\rangle)$$[1](https://en.wikipedia.org/wiki/W_state)[3](https://www.quantiki.org/wiki/w-state)[5](https://tqsd.github.io/QuNetSim/examples/send_w.html)

**命名由來**：W 態名稱來自 Wolfgang Dür，他於 2000 年首次提出該態[1](https://en.wikipedia.org/wiki/W_state)[4](https://quantumcomputing.stackexchange.com/questions/8528/what-does-w-stand-for-in-the-w-entangled-state)。

**應用**：W 態常用於安全量子通訊、分散式量子計算、量子記憶等領域，因其即使部分粒子遺失仍能保有糾纏的特性[1](https://en.wikipedia.org/wiki/W_state)[8](https://www.nature.com/articles/srep16245)。

1. [https://en.wikipedia.org/wiki/W_state](https://en.wikipedia.org/wiki/W_state)
2. [https://en.wikipedia.org/wiki/Quantum_entanglement](https://en.wikipedia.org/wiki/Quantum_entanglement)
3. [https://www.quantiki.org/wiki/w-state](https://www.quantiki.org/wiki/w-state)
4. [https://quantumcomputing.stackexchange.com/questions/8528/what-does-w-stand-for-in-the-w-entangled-state](https://quantumcomputing.stackexchange.com/questions/8528/what-does-w-stand-for-in-the-w-entangled-state)
5. [https://tqsd.github.io/QuNetSim/examples/send_w.html](https://tqsd.github.io/QuNetSim/examples/send_w.html)
6. [https://demonstrations.wolfram.com/ThreeQubitWStatesOnAQuantumComputer/](https://demonstrations.wolfram.com/ThreeQubitWStatesOnAQuantumComputer/)
7. [https://arxiv.org/pdf/quant-ph/0307115.pdf](https://arxiv.org/pdf/quant-ph/0307115.pdf)
8. [https://www.nature.com/articles/srep16245](https://www.nature.com/articles/srep16245)
9. [https://www.sciencedirect.com/topics/physics-and-astronomy/quantum-entanglement](https://www.sciencedirect.com/topics/physics-and-astronomy/quantum-entanglement)