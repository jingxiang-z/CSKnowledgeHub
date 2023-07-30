# 模型推导

[toc]

## 线性回归

### 一元线性回归

**最小二乘法：**最小化均方误差
$$
J=\frac{1}{m}\sum_{i=1}^{m}(y_i-f(x_i))^2=\frac{1}{m}\sum_{i=1}^{m}(y_i-wx_i-b)^2
$$

$$
w,b=argmin_{(w,b)}\frac{1}{m}\sum_{i=1}^{m}(y_i-wx_i-b)^2
$$

**极大似然估计：**最大化极大似然函数等价于最小二乘
$$
L(\theta)=\prod_{i=1}^{n} P(x_i;\theta)
$$

$$
y=wx+b+\epsilon
$$

$$
p(\epsilon)=\frac{1}{\sqrt {2\pi}\sigma}exp(-\frac{\epsilon^2}{2\sigma^2})
$$

$$
p(y)=\frac{1}{\sqrt {2\pi}\sigma}exp(-\frac{(y-(wx+b))^2}{2\sigma^2})
$$

$$
\ln L(w,b)=\sum_{i=1}^m\ln p(y_i)=m\ln \frac{1}{\sqrt {2\pi}\sigma} - \frac{1}{2\sigma^2}\sum_{i=1}^m(y_i-wx_i-b)^2
$$

$$
w,b=argmin_{(w,b)}\frac{1}{m}\sum_{i=1}^{m}(y_i-wx_i-b)^2
$$

**凸函数概念：**

凸集：对任意的$x,y \in D$与任意$\alpha \in [0,1]$都有$\alpha x+(1-\alpha)y \in D$则称D为凸集

凸函数：对任意的$x,y \in D$与任意$\alpha \in [0,1]$都有$f(\alpha x_1+(1-\alpha)x_2)\le \alpha f(x_1)+(1-\alpha)f(x_2)$称$f$为凸函数

多元函数的一阶导数：对每个分量求偏导数，构成梯度向量

多元函数的二阶导数：Hessain矩阵，一阶导数组合，形成二阶导数矩阵

凸函数定理：若$f(x)$的Hessian矩阵是半正定的，则$f(x)$为凸函数

半正定矩阵的判定定理：实对称矩阵的所有顺序主子式均非负，则矩阵为半正定矩阵

通过上述定理可证明一元线性回归的目标函数是凸函数

**求解最优化问题：**

凸充分性定理：对于凸函数来说，全局最小值的充要条件是一阶导等于零
$$
\frac{\partial J}{\partial b}=\frac{1}{m}\sum_{i=1}^m(-2(y_i-wx_i)+2b)=0
$$

$$
b=\frac{1}{m}\sum_{i=1}^m(y_i-wx_i)=\bar y-w\bar x
$$

$$
\frac{\partial J}{\partial w}=\frac{1}{m}\sum_{i=1}^m(-2(y_i-b)x_i+2x_i^2w)=0
$$

$$
w\sum_{i=1}^mx_i^2=\sum_{i=1}^{m}(y_i-b)x_i=\sum_{i=1}^{m}(y_i-(\bar y-w\bar x))x_i
$$

$$
w=\frac{\sum_{i=1}^my_ix_i-\bar y\sum_{i=1}^mx_i}{\sum_{i=1}^mx_i^2-\bar x\sum_{i=1}^mx_i}
$$

### 多元线性回归

线性代数视角：

矩阵微分公式：https://en.wikipedia.org/wiki/Matrix_calculus

$\bold X$是$M * N$维的矩阵，$M$是样本数量，$N$是自变量维度，最终所求解可能不唯一
$$
f(\bold{x_i})=\bold w^T \bold{x_i} + b=\hat{\bold w}^T\hat{\bold{x_i}}
$$

$$
J(\bold w)=(\bold y - \bold X \bold{\hat w})^T(\bold y - \bold X \bold{\hat w})
$$

$$
\bold {\hat w} = argmin(\bold y - \bold X \bold{\hat w})^T(\bold y - \bold X \bold{\hat w})
$$

$$
\frac{\partial J}{\partial \hat{\bold w}}=2\bold X^T(\bold X\bold{\hat w}-\bold y)
$$

$$
\frac{\partial^2 J}{\partial \hat{\bold w}^2}=2\bold X^T\bold X
$$

$$
\bold{\hat w}=(\bold{X^T}\bold{X})^{-1}\bold{X^T}\bold y
$$

经典统计视角：
$$
(Y| \bold X=\bold x)\sim N(\bold x \cdot \bold w,\sigma^2)
$$

$$
lnL(\bold w, \sigma^2)=-\frac{1}{2\sigma^2}\sum_{i=1}^{n}(y_i-\bold x_i \cdot\bold w)+\frac{n}{2}ln\frac{1}{\sigma^2}+C
$$

统计学习视角：

- Population risk: $E[(f(\bold X)-Y)^2]$
- Empirical risk: $\frac{1}{n}\sum_{i=1}^n(f(\bold X_i)-Y_i)^2$

## 逻辑回归

在线性模型的基础上加一个映射函数来实现分类功能（从实数域R映射到[0,1]）

**极大似然估计：**
$$
(Y_i|\bold X_i=\bold x_i)\sim Bernoulli(logistic(\bold x_i \cdot \bold w))
$$

$$
p_1=\frac{1}{1+e^{-(\bold w^T \bold x)}}=\frac{e^{\bold w^T \bold x}}{1+e^{\bold w^T \bold x}}
$$

$$
p_0=1-p_1=\frac{1}{1+e^{\bold w^T \bold x}}
$$

$$
p(y)=p_1^y\cdot p_0^{1-y}
$$

$$
Loss = -logL=\sum_{i=1}^my_i\cdot log(p_1)+(1-y_i)\cdot log(p_0)
$$

**信息论：**

信息熵：度量随机变量的不确定性，信息熵越大越不确定，公式为$H(X)=-\sum_x p(x)\log p(x)$

KL散度：度量两个分布的差异，也叫做相对熵，用来度量提议分布$q(x)$与真实分布$p(x)$的差距
$$
D_{KL}(p||q)=\sum_xp(x)log(\frac{p(x)}{q(x)})=\sum_xp(x)log(p(x))-\sum_xp(x)log(q(x))
$$
交叉熵：真实分布$p(x)$为常数，KL散度的后半部分称作交叉熵，公式是$-\sum_xp(x)\log q(x)$
$$
CrossEntropy=-y_i\log p_1-(1-y_i)\log p_0
$$

$$
Loss = \sum_{i=1}^my_i\cdot log(p_1)+(1-y_i)\cdot log(p_0)
$$

## LDA线性判别分析

目标：异类样本中心尽可能远，同类样本方差尽可能小
$$
max||\bold w^T\mu_0-\bold w^T\mu_1||_2^2
$$

$$
min\bold w^T\bold \sum_0\bold w
$$

$$
min\bold w^T\bold \sum_1\bold w
$$

$$
J = \frac{||\bold w^T\mu_0-\bold w^T\mu_1||_2^2}{\bold w^T\bold \sum_0\bold w+\bold w^T\bold \sum_1\bold w}=\frac{\bold w^T(\mu_0-\mu_1)(\mu_0-\mu_1)^T\bold w}{\bold w^T(\sum_0+\sum_1)\bold w}=\frac{\bold w^T\bold S_b \bold w}{\bold w^T\bold S_w \bold w}
$$

固定w的模长，求最优化问题来求解w的方向；通常固定分母大小，求负分子的最小化问题

带约束的优化问题可以通过拉格朗日乘子法求解
$$
L(\bold w, \lambda)=-\bold w^T\bold S_b\bold w+\lambda(\bold w^T\bold S_w\bold w-1)
$$

$$
\frac{\partial L}{\partial \bold w}=-2\bold S_b\bold w+2\lambda \bold S_w \bold w=0
$$

$$
\bold w = \frac{\gamma}{\lambda}\bold S_w^{-1}(\mu_0-\mu_1)=\bold S_w^{-1}(\mu_0-\mu_1)
$$

不关心$\bold w$的大小，只关心方向，可以令$\gamma = \lambda$，求解完毕

广义特征值：$\bold A\bold x=\lambda \bold B\bold x$，$\lambda$称作$\bold A$相对于$\bold B$的广义特征值

广义瑞利商：$\frac{\bold x^T \bold A \bold x}{\bold x^T\bold B \bold x}$，称作$\bold A$相对于$\bold B$的广义瑞利商

广义瑞利商的最小值等于最小广义特征值，最大值等于最大广义特征值

## 树模型

### 决策树基础

决策树通过if else结构来将数据集进行划分，实现分类预测

- 数值变量：每个节点都是与一个固定值进行比较划分子节点
- 分类变量：每个节点将不同类别划分为不同集合来划分子节点

决策树构建步骤(greedy learning heuristic)

- 初始化树：初始化决策树桩，遍历所有可能的分割点，选出最小错误的分割点
- 提高决策树：选择叶子节点，使得目标函数减小幅度最大
- 停止迭代：目标函数不改变（可能过早停止）；树的深度达到预先设定值（可能欠拟合）；每个叶子节点纯（可能过拟合）；

### ID3分类树

随机变量的信息熵：$H(x)=-\sum_x p(x)\log p(x)$

信息熵最大时，不确定性最高；信息熵等于零时，不确定性最低

对于随机变量$X$来说，当$X$的某个取值概率为1时信息熵最小；当$X$的每个取值概率均等时信息熵最大

条件熵：$H(Y|X)=\sum_x p(x)H(Y|X=x)$

信息增益：在已知属性a的取值后，y的不确定性减少的量
$$
Gain(D,a)=H(D)-\sum_v\frac{|D^v|}{D}H(D^v)
$$
ID3决策树以信息增益为准则来选择划分属性的决策树

### C4.5分类树

信息增益准则对可能取值数目较多的属性有所偏好，选择信息增益率代替信息增益
$$
Gain\_ratio(D,a)=\frac{Gain(D,a)}{IV(a)}\
$$

$$
IV(a)=-\sum_v \frac{|D^v|}{|D|}\log \frac{|D^v|}{|D|}
$$

a的可能取值个数越大，固有值$IV(a)$越大，但这种方法对于取值数目少的属性有所偏好

通常情况，C4.5算法先使用信息增益选出所有高于平均信息增益的特征，再从中选择信息增益率最大的

### CART分类树

基尼值：从样本集合中随机抽取两个样本，类别标记不一致的概率
$$
Gini(D)=\sum_kp_k(1-p_k)=1-\sum_kp_k^2
$$
基尼指数：类似于基尼值的条件熵
$$
Gini\_index(D,a)=\sum_v\frac{|D^v|}{|D|}Gini(D^v)
$$
与ID3决策树与C4.5决策树不同的是，CART决策树是一个二叉树，在用属性划分数据集时，将数据集分为等于与不等于两部分，之后选择基尼指数最小的属性以及对应的取值作为最优划分属性和划分点

### CART回归树

目标函数：平均平方误差Mean Squared Error
$$
MSE=\frac{1}{N}\sum_{n=1}^N(f(x_n)-y_n)^2
$$

- 对于连续数值变量，遍历每一个特征每一个数据点的取值，选出MSE最小的作为最优分割变量和最优分割点
- 对于离散变量，遍历每一个特征的每一个组合，选出MSE最小的作为最优分割变量和集合

### 决策树剪枝

- 预剪枝策略
  - 定义一个高度，当决策树达到该高度时就可以停止决策树的生长
  - 达到某个结点的实例具有相同的特征向量，即使这些实例不属于同一类，也可以停止决策树的生长
  - 定义一个阈值，当达到某个结点的实例个数小于该阈值时就可以停止决策树的生长
  - 定义一个阈值，通过计算每次扩张对系统性能的增益，并比较增益值与该阈值的大小来决定是否停止决策树的生长

- 后剪枝策略：删除一些子树，然后用其叶子节点代替
  - REP：可用的数据被分成两个样例集合：一个训练集用来形成学习到的决策树，一个分离的验证集用来评估这个决策树在后续数据上的精度，确切地说是用来评估修剪这个决策树的影响
  - PEP：悲观错误剪枝，悲观错误剪枝法是根据剪枝前后的错误率来判定子树的修剪

##  神经网络

M-P神经元：接收n个输入，给予输入权重并求加权和，跟自身阈值进行比较，经过激活后得到输出

单个神经元：感知机（阶跃函数sgn作为激活函数）、逻辑回归（sigmoid函数做激活函数）

多个神经元：神经网络

### 感知机

感知机智能解决线性可分的数据集，求解目标是用一个超平面划分正负样本
$$
f(x)=sgn(\bold w^T\bold x+b)
$$
- 超平面方程不唯一


- 法向量$w$垂直于超平面


- 法向量$w$与位移项$b$确定一个唯一的超平面


- 法向量指向的空间为正空间，另一半是负空间


策略：随机初始化模型参数w和b，最小化误分类样本
$$
L(\bold w, \theta)=\sum_x (\hat y -y)(\bold w^T \bold x-\theta)
$$
误分类点越小，误分类点离超平面越近，损失函数越小

学习算法：随机梯度下降法，一次随机选取一个误分类点使其梯度下降

### 神经网络

多个神经元构成的神经网络，可以分类线性不可分数据集

BP反向传播算法：目标函数回归任务使用均方误差，分类任务使用交叉熵

目标函数通常是一个非凸函数，所以梯度下降法不一定能到全局最小值

![8.png](../../../Images/U3iEf2QnpCOFqsS.png)
$$
E_k=\frac{1}{2}\sum_j^l(\hat y_j^k-y_j^k)^2
$$

$$
\frac{\partial E_k}{\partial v_{ih}}=\sum_j^l\frac{\partial E_k}{\partial \hat y_j^k}\cdot \frac{\partial \hat y_j^k}{\partial \beta_j}\cdot \frac{\partial \beta_j}{\partial b_h}\cdot \frac{\partial b_h}{\partial \alpha_h}\cdot \frac{\partial \alpha_h}{\partial v_{ih}}
$$

sigmoid函数的导数：$f'(x)=f(x)(1-f(x))$
$$
\frac{\partial E_k}{\partial v_{ih}}=\sum_j^l(\hat y_j^k-y_j^k)\hat y_j^k(1-\hat y_j^k)w_{hj}b_h(1-b_h)x_i=\sum_j^l-g_jw_{hj}b_h(1-b_h)x_i
$$

$$
\frac{\partial E_k}{\partial v_{ih}}=-b_h(1-b_h)\sum_j^lg_jw_{hj}x_i=-e_hx_i
$$

## 支持向量机

### 拉格朗日乘子法

$$
min f(x)
$$

$$
s.t. g_i(x)\le 0,i=1,2,...,m
$$

$$
h_j(x)=0,j=1,2,...,n
$$

拉格朗日乘子法可以求解上述带约束的优化问题
$$
L(x,\mu,\lambda)=f(x)+\sum \mu_ig_i(x)+\sum\lambda_jh_j(x)
$$
定义$\Gamma(\mu,\lambda)$为拉格朗日函数的对偶函数，对偶函数恒为凹函数，构成拉格朗日函数的下确界($\mu_i>0$)
$$
\Gamma(\mu,\lambda)=inf(L(x,\mu,\lambda))\le L(x,\mu,\lambda)\le f(x)
$$
强对偶性：若主问题是凸优化问题，且可行集中存在一点使得所有不等式约束的不等号成立，强对偶性成立

弱对偶性：若主问题非凸优化问题，对偶函数恒为凸优化问题

KKT条件：若强对偶性成立，$x^*,\mu^*,\lambda^*$分别为主问题和对偶问题的最优解，则最优解满足KKT条件

### 硬间隔SVM

给定线性可分的数据集，找距离正负样本都最远的超平面$\bold w^T\bold x+b$，存在唯一解，泛化性能好

几何间隔：$\gamma_i=\frac{y_i(\bold w^T\bold x_i +b)}{||\bold w||}$，对于数据集而言，几何间隔是所有点几何间隔的最小值

模型：给定线性可分数据集，求数据集关于超平面的几何间隔，使得几何间隔达到最大
$$
max_{\bold w,b}\frac{1}{||\bold w||}=min_{\bold w,b}\frac{1}{2}||w||^2
$$

$$
s.t. y_i(\bold w^T\bold x_i+b)\ge 1, i=1,2,...,m
$$

$$
L(\bold w, b,\alpha)=\frac{1}{2}||\bold w||^2+\sum_i\alpha_i(1-y_i(\bold w^T\bold x_i+b))
$$

$$
L(\bold w, b,\alpha)=\frac{1}{2}||\bold w||^2+\sum_i \alpha_i-\sum_i \alpha_iy_i\bold w^T\bold x_i-b\sum_i\alpha_iy_i
$$

$$
\bold w=\sum_i\alpha_iy_i\bold x_i
$$

$$
\sum_i\alpha_iy_i=0
$$

转化上述问题为如下约束优化问题：
$$
max\sum_i \alpha_i-\frac{1}{2}\sum_i\sum_j\alpha_i\alpha_jy_iy_j\bold x_i^T\bold x_j
$$

$$
s.t. \sum_i\alpha_iy_i=0,\alpha_i\ge0
$$

### 软间隔SVM

允许部分样本不满足约束条件，不满足约束条件的样本尽可能少
$$
J(\bold w)=min_{w,b}\frac{1}{2}||\bold w||^2+C\sum_{i=1}^ml_{0/1}(y_i(\bold w^T\bold x_i+b)-1)
$$
$l_{0/1}$是0/1损失函数，当不满足约束条件时为0，否则为1；C是一个常数，用于调节随时权重，C趋近于正无穷时，原损失函数退化成硬间隔SVM

0/1损失函数时间断的，性质不好，常用hinge损失来代替0/1损失$hinge(z)=max(0,1-z)$

引入松弛变量$\xi_i$，原优化问题等价于以下
$$
min_{w,b}\frac{1}{2}||\bold w||^2+C\sum_{i=1}^m \xi_i
$$

$$
s.t. y_i(\bold w^T\bold x_i+b)\ge1-\xi_i,\xi_i\ge0
$$

### 支持向量回归

相比于线性回归用一条线来拟合样本，支持向量回归采用一条线$\bold w^T\bold x+b$为中心，宽度为$2\epsilon$的间隔带来拟合训练样本，不在间隔带的样本计算损失，最小化损失函数
$$
J(\bold w)=min_{w,b}\frac{1}{2}||\bold w||^2+C\sum_{i=1}^ml_{\epsilon}(f(\bold x_i)-y_i)
$$
上述损失函数可以写成下面形式
$$
min\frac{1}{2}||\bold w||^2+C\sum_{i=1}^m(\xi_i+\hat \xi_i)
$$

$$
s.t. -\epsilon-\hat \xi_i\le f(\bold x_i)-y_i\le \epsilon+\xi_i
$$


$$
Ee=0.75(1-Eo)+0.25Eo
$$

$$
Eo=3/2-2Ee
$$

## 矩阵分解

### PCA

Properties of the covariance matrix cov(X):

- Symmetric matrix
- d non-negative real eigenvalues $\lambda_1\ge \lambda_2\ge...\ge\lambda_d$ and corresponding eigenvectors $\vec v_1,\vec v_2,...,\vec v_d$
- Eigenvalue decomposition: $cov(\vec X)=\sum_{i=1}^d\lambda_i\vec v_i\vec v_i^T$

Let eigenvalues of $cov(\vec X)$ be $\lambda_1\ge \lambda_2\ge ...\ge \lambda_d \ge0$, and let $\vec v_1, \vec v_2,..., \vec v_d$ be corresponding orthonormal eigenvectors.
$$
\vec X\rightarrow \vec \mu+\Pi_W(\vec X-\vec \mu)
$$

$$
E[||\Pi_W(\vec X-\vec \mu)||^2_2]=E[||\sum_{i=1}^k\vec \alpha_i\vec \alpha_i^T(\vec X-\vec \mu)||^2_2]= E[(\sum_{i=1}^k\vec \alpha_i^T(\vec X-\vec \mu))^2]=\sum_{i=1}^k var(\vec \alpha \cdot \vec X)
$$

$$
var(\vec \alpha\cdot \vec X)=\vec \alpha^Tcov(\vec X)\vec \alpha=\vec \alpha^T(\sum_{i=1}^d\lambda_i \vec v_i\vec v_i^T)\vec \alpha=\sum_{i=1}^d \lambda_i(\vec \alpha\cdot \vec v_i)^2
$$

Top eigenvector computation: If t is sufficiently large, multiplying $(A^TA)^t$ by any vector yields a vector that is in span of $\vec v_1$
$$
(A^TA)^t=\lambda_1^t(\vec v_1\vec v_1^T+\sum_{i=2}^d(\frac{\lambda_i}{\lambda_1})^t\vec v_i\vec v_i^T))\approx \lambda_1^t\vec v_1\vec v_1^T
$$

### SVD

$$
J(B,C)=||A-BC||_F^2=(\sqrt{\sum_{i=1}^n\sum_{j=1}^dM_{ij}^2})^2
$$

$$
A=USV^T=\sum_{i=1}^rs_i\vec u_i\vec v_i^T
$$

$$
||A-A_k||_F^2=\min ||A-M||_F^2=\sum_{i=k+1}^{rank(A)}s_i^2
$$

$$
A^TA=(VSU^T)(USV^T)=VS^2V^T=\sum_{i=1}^rs_i^2\vec v_i\vec v_i^T
$$

## Ensemble Method

### Bagging

$$
f_{avg}(\vec x)=\frac{1}{M}\sum_{t=1}^Mf_t(\vec x)
$$

$$
E[(f_{avg}(\vec X)-Y)^2]=\frac{1}{M}\sum_{t=1}^ME[(f_t(\vec X)-Y)^2]-\frac{1}{2M^2}\sum_{s=1}^M\sum_{t=1}^ME[(f_s(\vec X)-f_t(\vec X))^2]
$$

- Randomly sample M independent data set $S_1,...,S_M$, each of size $n=|S|$ (Bootstrap sampling)
- Run ML algorithm on each S to get predictors $f_1,f_2,...,f_M$
- Return $f_{avg}=\frac{1}{M}\sum_{t=1}^M f_t$

### Boosting

For different time 1, 2, ..., T

- Construct probability distribution $(D_t(1), D_t(2),...,D_t(n))$
- Run weak learning algorithm on $D_t$ weighted training examples
- Return final classifier

$$
\epsilon_t=\sum_{i=1}^nD_t(i)\cdot 1\{h_t(\vec x)\neq y_i\}
$$

$$
D_{t+1}(i)=\frac{D_t(i)}{Z_t}\times exp(-\alpha_ty_ih_t(\vec x_i))
$$

$$
\alpha_t=\frac{1}{2}\log (\frac{1-\epsilon_t}{\epsilon_t})
$$

$$
f(\vec x)=sign(\sum_{t=1}^T\alpha_t h_t(\vec x))
$$

