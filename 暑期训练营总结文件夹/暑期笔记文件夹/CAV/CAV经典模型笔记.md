# CAV7.18-7.19学习笔记

### 摘要

本文提出了一种基于反馈的联网自动驾驶汽车（cav）在不同通信网络拓扑下的控制协议，用图论表示网络拓扑结构，利用李雅普诺夫技术和拉萨尔不变性原理分析了控制协议的稳定性和一致性。研究了不同通信网络拓扑结构对控制的收敛性和鲁棒性的影响。实验数值表明，所提出的协议在收敛时间和鲁棒性方面具有位置和速度一致性的有效性

### 介绍 

队列控制的目标是保证队列中所有车辆以相同的速度移动，同时保持理想的队列几何形状。提出了许多解决编队控制问题的方法，主要包括**领导者-追随者**，**虚拟领导者**等等

### 图论的基础知识

### 领导者对角线矩阵

定义：只有与领导者之间为邻居，能接受领导者信息的，对角线元素为K>0，否则为0

### 控制方程

关于追随者的控制方程，标号上有一点为导数
$$
\left\{\begin{array}{l}
\dot{x}_{i}(t)=v_{i}(t) \\
\dot{v}_{i}(t)=u_{i}(t)
\end{array}\right.
$$
关于领导者的控制方程
$$
\left\{\begin{array}{l}
\dot{x}_{L}(t)=v_{L}(t) \\
\dot{v}_{L}(t)=u_{L}(t)
\end{array}\right.
$$
关于领导者-追随者的系统控制协议
$$
\left\{\begin{aligned}
\dot{x}_{i}(t)=& v_{i}(t) \\
\dot{v}_{i}(t)=& \dot{v}_{L}(t)-\sum_{j=1}^{n} a_{i j}\left[\left(x_{i}(t)-x_{j}(t)-r_{i j}\right)+\beta\left(v_{i}(t)-v_{j}(t)\right)\right] \\
&-k_{i}\left[\left(x_{i}(t)-x_{L}(t)-r_{i}\right)+\gamma\left(v_{i}(t)-v_{L}(t)\right)\right] .
\end{aligned}\right.
$$
**注意：**这个领导者-追随者的系统控制协议v的导数求出来是a----加速度，故我们要使用v=v0+aΔt来得到下一个时刻瞬间的速度，同理，我们需要x=x0+vΔt来获得下一个时刻瞬间的位置

### 定理一

满足这个控制方程我们会有一个定理产生
$$
(i)  \lim _{t \rightarrow \infty}\left\|\tilde{x}_{i_{x}}\right\|=\left\|x_{i_{x}}-x_{L_{x}}-r_{i_{x}}\right\|=0 ; \lim _{t \rightarrow \infty}\left\|\tilde{x}_{i_{y}}\right\|=\left\|x_{i_{y}}-x_{L_{y}}-r_{i_{y}}\right\|=0 ;
$$

$$
(i1)

\lim _{t \rightarrow \infty}\left\|\tilde{v}_{i_{x}}\right\|=\left\|v_{i_{x}}-v_{L_{x}}\right\|=0 ; \lim _{t \rightarrow \infty}\left\|\tilde{v}_{i_{y}}\right\|=\left\|v_{i_{y}}-v_{L_{y}}\right\|=0 .
$$

表示的意思是当这个系统趋于一致时，当时间t趋于无穷时，追随者xi与领导者xl之间的距离趋近于期望距离

追随者vi与领导者vl的速度趋于一致，加速度为0，相对静止

### 实验复现结果

图一

![](https://ccd123.oss-cn-guangzhou.aliyuncs.com/img/w1.gif)

