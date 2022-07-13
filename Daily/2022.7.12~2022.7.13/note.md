# DP7.11-7.12学习笔记

## lec5

### 松弛差分隐私：

由于我们的纯差分隐私假设的情况过于保守，它假设攻击者对数量为n邻接数据集已经知晓n-1个数据，这在现实中的极大数据库几乎不可能完成，故引入松弛差分隐私概念，松弛差分隐私概念满足

$\operatorname{Pr}[M(X) \in T] \leq e^{\varepsilon} \operatorname{Pr}\left[M\left(X^{\prime}\right) \in T\right]+\delta$

与纯差分隐私对比，松弛差分隐私虽然对隐私的保护程度略逊一筹，但是更符合实际情况，更容易应用

### 松弛差分隐私后处理：

松弛差分隐私算法经过后处理之后仍然是松弛差分隐私（纯差分隐私经过后处理只会也是纯差分隐私，隐私预算不变）

![](https://ccd123.oss-cn-guangzhou.aliyuncs.com/img/20220713211322.png)

这个定理表示，只要M是松弛差分隐私算法，不管F是任何什么算法（差分或不差分，差分的隐私预算是多少），F（M（D））都依然是松弛差分意思算法，隐私预算不变！！

### 松弛差分隐私的群体隐私：

若查询方式的敏感度为k，则由于是松弛差分隐私，所以不止e^(k），(纯差分隐私只有这个)

e)这一项改变，还增加了一项$e^{(k-1) \delta}$，完整公式如下：

$\operatorname{Pr}[M(X) \in T] \leq \exp (k \varepsilon) \operatorname{Pr}\left[M\left(X^{\prime}\right) \in T\right]+k e^{(k-1) \varepsilon} \delta$

### 松弛差分隐私的基本组合：

串行组合：假设有一个序列的松弛差分隐私算法，那么这一序列的松弛差分隐私算法作用完在数据库D上之后（注意：不是符合函数的形式，而是并列先后作用的形式），那么松弛差分隐私隐私预算e和δ都累加（纯差分隐私就是只有e累加），最终会导致隐私预算变高，隐私泄露的风险也变大

### 高斯机制Gaussian Mechanism

首先，敏感度相较拉普拉斯的有所更改

$\Delta_{2}^{(f)}=\max _{X, X^{\prime}}\left\|f(X)-f\left(X^{\prime}\right)\right\|_{2}$

高斯分布公式及曲线：

$p(x)=\frac{1}{\sqrt{2 \pi \sigma^{2}}} \exp \left(-\frac{(x-\mu)^{2}}{2 \sigma^{2}}\right)$

![](https://ccd123.oss-cn-guangzhou.aliyuncs.com/img/20220713212824.png)

又证明知基于高斯机制的差分隐私是松弛差分隐私，对与每一个坐标的加噪，高斯分布的参数为：$N\left(0,2 \ln (1.25 / \delta) \Delta_{2}^{2} / \varepsilon^{2} \cdot I\right)$

只需求出敏感度δ2即可

### 常见的统计学查询方式：

计数查询：这时候相邻数据集的最大敏感度为1，若用拉普拉斯机制，这参数λ为1/e

直方图查询（可以用于查询前10000个first name）：这种查询是先将数据集划分为几个子cells，然后由于改变一条数据也只会在一个子cell中改变，所以敏感度是1，所以如果还是用拉普拉斯机制的话，参数λ还是1/e

tips：对于使用拉普拉斯机制进行一般查询的情况，都有一个客观事实就是：

![](https://ccd123.oss-cn-guangzhou.aliyuncs.com/img/20220713213857.png)



## lec6

好像讲了一个叫做相对熵的东西

看差分隐私那本书补充一点感觉可能有点相关的知识点吧.....

### KL-Divergence（KL散度）：

讲两个在定义域的随机变量，有一个定义：

![](https://ccd123.oss-cn-guangzhou.aliyuncs.com/img/20220713220434.png)

### Max Divergence（最大散度）：

目前还没搞懂跟上面那个KL散度有什么区别，这里给出两种差分隐私的最大散度：

![](https://ccd123.oss-cn-guangzhou.aliyuncs.com/img/20220713220604.png)



## lec7

### 指数机制

指数机制属于纯e差分隐私

指数机制的灵敏度Δs定义如下：

$\Delta s=\max _{h \in \mathcal{H}} \max _{X, X^{\prime}}\left|s(X, h)-s\left(X^{\prime}, h\right)\right|$

其中s（）是打分函数

指数机制适合用于离散的非数值型的给出“best”值的查询上，他会需要一个打分函数，打分函数会需要输入的数据集和一个“小型范围”，打分函数对输入在“小型范围”内进行打分，在“小型范围”中给出一个得分较高的值，并输出。在指数机制中，输出的得分较高的值的概率会正比于$\exp \left(\frac{\varepsilon s(X, h)}{2 \Delta}\right)$

损失的隐私大约为：

$\left.\ln \left(\frac{\exp (\varepsilon u(x, r) / \Delta u)}{\exp (\varepsilon u(y, r) / \Delta u)}\right)=\varepsilon[u(x, r)-u(y, r)] / \Delta u\right) \leq \varepsilon$

u还是打分函数，r是“小范围”，x，y是相邻数据集

