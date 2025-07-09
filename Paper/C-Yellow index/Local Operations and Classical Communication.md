**LOCC** 是 “Local Operations and Classical Communication”（局域操作與古典通訊）的縮寫，是量子資訊科學中用來描述對分布於不同位置的量子系統進行操作的一種標準方式[4](https://zh.wikipedia.org/zh-tw/LOCC)[8](http://mp.ihep.ac.cn/article/pdf/preview/12123)。

其基本概念如下：
- **Local Operations（局域操作）**：各方只能對自己手上的量子系統單獨進行量子操作（如測量、單位操作、加入輔助量子比特等），不能直接對其他人的量子系統進行操作。
- **Classical Communication（古典通訊）**：各方可以通過經典通訊（如電話、網路等）交換操作結果或協調後續操作，但不能傳送量子資訊。

**LOCC 的重要性：**
- LOCC 是量子糾纏研究中的一個核心概念。兩個量子態若能僅靠 LOCC 互相轉換，則它們的糾纏性質被認為是等價的。
- LOCC 操作下，量子糾纏度不會增加，也就是說，僅靠 LOCC 無法創造新的糾纏，只能消耗或重新分配現有糾纏[3](https://wuli.iphy.ac.cn/cn/article/pdf/preview/10.7693/wl20130802.pdf)[7](https://www.zhihu.com/question/20322494/answer/2645861744)。
- 許多量子資訊任務（如糾纏蒸餾、量子隱形傳態等）都以 LOCC 為操作限制[1](https://github.com/PaddlePaddle/Quantum/blob/master/tutorials/locc/EntanglementDistillation_LOCCNET_CN.ipynb)。

**舉例說明：**
- Alice 和 Bob 各自持有一個糾纏粒子，他們可以分別對自己的粒子做測量或操作，並用電話溝通測量結果，協調下一步操作，這就是 LOCC。
- 但他們不能直接將自己的量子比特傳送給對方，也不能對對方的粒子做操作。

**總結：**  
LOCC 是量子資訊中描述「只能做本地操作＋經典溝通」的操作集合，是判定量子態糾纏性質與可轉換性的基本標準[4](https://zh.wikipedia.org/zh-tw/LOCC)[8](http://mp.ihep.ac.cn/article/pdf/preview/12123)。

1. [https://github.com/PaddlePaddle/Quantum/blob/master/tutorials/locc/EntanglementDistillation_LOCCNET_CN.ipynb](https://github.com/PaddlePaddle/Quantum/blob/master/tutorials/locc/EntanglementDistillation_LOCCNET_CN.ipynb)
2. [https://zh.wikipedia.org/zh-tw/%E9%87%8F%E5%AD%90%E7%BA%8F%E7%B5%90](https://zh.wikipedia.org/zh-tw/%E9%87%8F%E5%AD%90%E7%BA%8F%E7%B5%90)
3. [https://wuli.iphy.ac.cn/cn/article/pdf/preview/10.7693/wl20130802.pdf](https://wuli.iphy.ac.cn/cn/article/pdf/preview/10.7693/wl20130802.pdf)
4. [https://zh.wikipedia.org/zh-tw/LOCC](https://zh.wikipedia.org/zh-tw/LOCC)
5. [https://www.phy.pku.edu.cn/jhchen/files/Q-3.pdf](https://www.phy.pku.edu.cn/jhchen/files/Q-3.pdf)
6. [https://wuli.wiki/book/LZJC.html](https://wuli.wiki/book/LZJC.html)
7. [https://www.zhihu.com/question/20322494/answer/2645861744](https://www.zhihu.com/question/20322494/answer/2645861744)
8. [http://mp.ihep.ac.cn/article/pdf/preview/12123](http://mp.ihep.ac.cn/article/pdf/preview/12123)
9. [https://wuli.iphy.ac.cn/cn/article/pdf/preview/31621.pdf](https://wuli.iphy.ac.cn/cn/article/pdf/preview/31621.pdf)