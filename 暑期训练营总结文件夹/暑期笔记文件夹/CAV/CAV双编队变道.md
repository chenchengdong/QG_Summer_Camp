# CAV8.05-8.06学习笔记

## 基于事件触发机制的双编队车辆换到决策模型

### 摘要：

​		本论文针对由联网自动化车辆组成的双编队车辆换道问题进行研究，提出了基于事件触发的分布式换道决策模型，设计了一种编队内和编队间的一致性控制协议

### 单个编队：

​		单个编队的拓扑结构

![](https://ccd123.oss-cn-guangzhou.aliyuncs.com/img/20220807091513.png)

### 事件触发器的设计：

​		采用组合测量误差的方法，其中定义智能体i在t时刻中的组合状态为
$$
q_{i}^{p}=   \sum_{j=1}^{N} a_{i j}(t)\left[\left(x_{j}^{p}(t)-x_{i}^{p}(t)\right)+\left(v_{j}^{p}(t)-v_{i}^{p}(t)\right)\right] 
$$
​		此时的测量误差定义为
$$
e_{i}^{p}(t)=q_{i}^{p}\left(t_{i}^{k}\right)-q_{i}^{p}
$$
​		定义触发条件如下
$$
\begin{array}{c}
h\left(e_{i}^{p}(t), q_{i}^{p}(t)\right)=\left\|e_{i}^{p}(t)\right\|-\eta_{i}^{p}(T)\left\|q_{i}^{p}(t)\right\|= \\
\| \sum_{j \in N_{i}} a_{i j}(t)\left(\left(x_{j}^{p}\left(t_{i}^{k}\right)-x_{i}^{p}\left(t_{i}^{k}\right)\right)+\left(v_{j}^{p}\left(t_{i}^{k}\right)-v_{i}^{p}\left(t_{i}^{k}\right)\right)\right)- \\
\sum_{i \in N_{i}} a_{i j}(t)\left(\left(x_{j}^{p}(t)-x_{i}^{p}(t)\right)+\left(v_{j}^{p}(t)-v_{i}^{p}(t)\right)\right) \|- \\
\boldsymbol{\eta}_{:}^{p}(T)\left\|\sum_{j \in N_{i}} a_{i j}(t)\left(\left(x_{j}^{p}(t)-x_{i}^{p}(t)\right)+\left(v_{j}^{p}(t)-v_{i}^{p}(t)\right)\right)\right\|
\end{array}
$$

### 编队内分布式控制协议的设计：

​		各个编队内跟随车加速度
$$
\begin{array}{l}
u_{i}^{p}(t)=-\sum_{j \in N_{i}(s(t))} a_{i j}(t)\left[\gamma_{1}\left(x_{i}^{p}\left(t_{i}^{k}\right)-x_{j}^{p}\left(t_{i}^{k}\right)-r_{i j}^{p}(T)\right)+\gamma_{2}\left(v_{i}^{p}\left(t_{i}^{k}\right)-\right.\right. \\
\left.\left.v_{j}^{p}\left(t_{i}^{k}\right)\right)\right]-\pi_{i}^{p}\left[\gamma_{3}\left(x_{i}^{p}\left(t_{i}^{k}\right)-x_{L}^{p}\left(t_{i}^{k}\right)-r_{i L}^{p}(T)\right)+\gamma_{4}\left(v_{i}^{p}\left(t_{i}^{k}\right)-v_{L}^{p}\left(t_{i}^{k}\right)\right)\right]
\end{array}
$$

### 编队间分布式控制协议的设计：

​		从编队领导车加速度
$$
\begin{array}{c}
u_{L}^{p}\left(t_{L}\right)=-\pi_{L}^{P}\left[\gamma_{5}\left(x_{L}^{\text {follower }}\left(t_{L}\right)-x_{L}^{\text {major }}\left(t_{L}\right)-r_{L}(T)\right)+\right. \\
\left.\gamma_{6}\left(v_{L}^{\text {follower }}\left(t_{L}\right)-v_{L}^{\text {major }}\left(t_{L}\right)\right)\right]
\end{array}
$$

### 整个过程：

1. 首先是两个编队内跟随车与领导车行程期望距离，从编队领导车与主编队领导车形成期望距离（使用基于事件触发的分布式控制协议分别控制）
2. 然后计算出换到需要拉伸的期望距离，并在现编队进行拉伸（使用基于事件触发的分布式控制协议分别控制）
3. 拉伸完毕后所有车断开拓扑连接，若是跟随车则仅仅只保留与需要换到所属的领导车的联系进行换道，从领导车依旧与主领导车保持联系
4. 车辆换道完之后仍然属于拉伸状态，这是再重新设定期望距离，根据每个编队重新形成拓扑结构和拉普拉斯矩阵来进行收缩（使用基于事件触发的分布式控制协议分别控制）

### 复现结果：

#### 小车的x坐标随时间变化图

![](https://ccd123.oss-cn-guangzhou.aliyuncs.com/img/20220807091118.png)

#### 车辆变化动图

![](./gif1.gif)