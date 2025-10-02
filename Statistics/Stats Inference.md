# Stats Inference

## Stats Fundamental

### Convergence

- Convergence in distribution

$$
\sqrt n(\bar X_n-\mu)\stackrel{d}{\longrightarrow} N(0,\sigma^2)
$$

- Convergence in probability

$$
\bar X_n\stackrel{p}{\longrightarrow} \mu
$$

If $X_n$ convergence in probability to $X$, then $X_n$ convergence in distribution to $X$.

### Law of Large numbers

$X_1,X_2,...,X_n$ is i.i.d random variables with mean $\mu$ and finite variance.
$$
\bar X_n=\frac{1}{n}\sum_{i=1}^nX_i\stackrel{p}{\longrightarrow}\mu
$$

### Central Limit Theorem

$X_1,X_2,...,X_n$ is i.i.d random variables with mean $\mu$ and finite variance.
$$
\sqrt n\frac{\bar X_n-\mu}{\sigma}\stackrel{d}{\longrightarrow}N(0,1)
$$

### Slutsky's Theorem

If $X_n\stackrel{d}{\longrightarrow}X$ and $Y_n\stackrel{p}{\longrightarrow}c$, then the following
$$
X_n+Y_n\stackrel{d}{\longrightarrow}X+c
$$

$$
X_nY_n\stackrel{d}{\longrightarrow}cX
$$

$$
If\ c\ne0,\frac{X_n}{Y_n}\stackrel{d}{\longrightarrow}\frac{X}{c}
$$

### Continuous Mapping Theorem

Let $\bold X_i\in R$, and $\bold X_i\stackrel{d}{\longrightarrow}\bold X$, then if $g$ is a continuous function, we have $g(\bold X_i)\stackrel{d}{\longrightarrow} g(\bold X)$ in distribution. 

### Delta Method

Suppose that $\sqrt n(T_n-t)\stackrel{d}{\longrightarrow}N(0,v)$. If $g(x)$ is a function with derivative $g'(t)$, then
$$
\sqrt n(g(T_n)-g(t))\stackrel{d}{\longrightarrow}g'(t)N(0,v)
$$

## Parameter Estimation

An estimator of $\theta_0\in \theta$ is a statistic whose primary goal is to estimate $\theta_0$, If {$X_1=x_1,...,X_n=x_n$} are observed, then $T(x_1,...,x_n)$ is called an estimate of $\theta_0$.

- An estimator $\theta_n$ of $\theta_0$ is unbiased if $E[\hat \theta_n]=\theta_0$
- An estimator $\theta_n$ of $\theta_0$ is consistent if $\hat \theta_n\stackrel{p}{\longrightarrow}\theta_0$

- Mean Square Error is a measure of accuracy of an estimator

$$
MSE(\hat \theta_n)=tr[var(\hat \theta_n)]+||bias(\hat \theta_n,\theta_0)||_2^2
$$

$$
Eff(\hat \theta_n, \tilde \theta_n)=\frac{MSE(\hat \theta_n)}{MSE(\tilde \theta_n)}
$$

### Method of Moments

- Population moments: $\mu_k(\theta_0)=E[X_1^k]$
- Empirical moments: $\hat \mu_k=\bar X_n^k=\frac{1}{n}\sum_{i=1}^n X_i^k$

When the sample size gets larger, the empirical moments will converge to the population moments. Typically we will choose the number of moments to match the dimension of the parameter that we want to estimate.
$$
\sqrt n(\hat \theta_n^{MM}-\theta_0)\stackrel{d}{\longrightarrow}N(0,V(\theta_0))
$$
The method of moments estimator is a consistent and asymptotically normally distributed, where $V(\theta_0)=[\triangledown\psi^{-1}(M(\theta_0))]\Sigma(\theta_0)[\triangledown\psi^{-1}(M(\theta_0))]^T$

### Maximum Likelihood Estimation

$X_1,...,X_n$ is i.i.d. sample of random variables with density function $f(x;\theta_0)$, the likelihood function is
$$
L(\theta;x_1,...,x_n)=\prod_{i=1}^nf(x_i;\theta)
$$

$$
\hat \theta_n^{MLE}=argmax\log L(\theta;X_1,...X_n)
$$

The maximum likelihood estimator is consistent and asymptotically normally distributed.
$$
I(\theta)=-E[\frac{\partial^2}{\partial \theta\partial \theta^T}\log L(\theta;X_1)]
$$

$$
I_n(\theta)=-\sum_{i=1}^n E[\frac{\partial^2}{\partial \theta\partial \theta^T}\log L(\theta;X_i)]=nI(\theta)
$$

$$
\sqrt n(\hat \theta_n^{MLE}-\theta_0)\stackrel{d}{\longrightarrow}N(0,I(\theta_0)^{-1})
$$

Cramer-Rao Lower Bound: $X_1, X_2,...,X_n$ is i.i.d. sample of random variables with density function $f(x;\theta_0)$. For an unbiased estimator $T(\bold X)$
$$
var(T(\bold X))\ge \frac{1}{nI(\theta_0)}
$$

## Hypothesis Testing

### Confidence Interval

The random interval $[L(\bold X), U(\bold X)]$ is called a $\alpha$ level confidence interval for $\theta$ if 
$$
P[L(\bold X)\le\theta\le U(\bold X)]\ge \alpha
$$
$\R(\bold X)$ is a subset of $\theta$ depending on $\bold X$. $R(\bold X)$ is called a $\alpha$ confidence region if
$$
P[\bold \theta\in R(\bold X)]\ge\alpha
$$
A random variable $g(\bold X;\theta)=g(X_1,...,X_n;\theta)$ is a pivot if the distribution of $g(\bold X;\theta)$ is independent of the parameter $\theta$. Use $P(a\le g(\bold X;\theta)\le b)=\alpha$ to get the confidence interval $[a, b]$.

The bootstrap method is a powerful computer based alternative the construction of the confidence intervals.

### Hypothesis Testing

- H0: $\theta \in \theta_0$ is the null hypothesis
- H1: $\theta \in \theta_1$ is the alternative hypothesis
- Rejection region: R={X: H_0 rejected}
- Type 1 error: $\alpha=P_{\theta}(R)$, for all $\theta\in \theta_0$
- Type 2 error: $1-\beta=1-P_\theta(R)$, for all $\theta \in\theta/\theta_0$

$[L(X), U(X)]$ Is a $(1-\alpha)$ level confidence interval for parameter $\theta$. Then the test defined with rejection region ${\theta_0\notin [L(X),U(X)]}$ is a hypothesis test with significance level $\alpha$, where null hypothesis H0 and alternative hypothesis H1

p-value of a test statistics $T_n$ is the probability under H0 of obtaining the observed value of $T_n$ or a more extreme one.
$$
p=P_{H_0}[T_n\ge t_{obs}]
$$

- The smaller the p-value, the more confident we are about rejecting H0
- Commonly we consider he thresholds 0.05 or 0.01
- p-value do not give the probability the the null hypothesis is true and do not indicate which alternative is best supported

### Likelihood Ratio Test

Likelihood ratio test is method of hypothesis testing related to the maximum likelihood estimators. $\bold X=(X_1,...,X_n)$ is random variables with joint distribution depending on $\theta$, $L(\theta|\bold X)$ is the likelihood function. LRT statistic for the null hypothesis and alternative hypothesis is
$$
\lambda(\bold X)=\frac{sup_{\theta_0}L(\theta|\bold X)}{sup_{\theta_1}L(\theta|\bold X)}
$$
The rejection region is {$\bold X:\lambda(\bold X)\le c$}, where c is a number between 0 and 1.

### Comparison of Tests

The level of a test only controls the type 1 error. Given two tests that achieve the same rejection level, the better test among them will be the one that minimize the type 2 error.

Neyman-Pearson Lemma: suppose that $\bold X$ have joint density function $f(\bold x;\theta)$. The most powerful test at level $\alpha$ is given by
$$
R={\bold x: \frac{f_{\theta_1}(\bold x)}{f_{\theta_0}(\bold x)}>C_{\alpha}}
$$
Where $C_{\alpha}$ is a constant such that $P_{\theta_0}\le\alpha$.

### Wald Test

When the unknown parameter $\theta$ is multivariate many hypothesis can be expressed as linear combinations of the components of $\theta$.
$$
H_0: A\theta=a_0
$$

$$
H_1:A\theta\neq a_0
$$

$$
W_n=(A\hat \theta-a_0)^T(AI_n(\hat \theta)A^T)^{-1}(A\hat \theta-a_0)
$$

$$
W_n\stackrel{d}{\longrightarrow}X^2_q
$$

## Exponential Family

Let $X=(X_1,...,X_n)$ have a joint distribution $F_{\theta}$. The family of distributions $\{F_{\theta}\}$ is a said to be k-parameter exponential family if its density or probability function can be written in the form
$$
f(\bold x;\theta)=c(\theta)exp\{\sum_{j=1}^kQ_j(\theta)T_j(\bold x)\}h(\bold x)
$$

### Sufficient Statistic

A statistic $T=T(\bold X)$ is a sufficient statistic for a parameter $\theta$ if for all sets A, $P[\bold X\in A|T=t]$ is independent of $\theta$ for all t in rane of T.

Suppose that $X=(X_1,...,X_n)$ has a joint density or frequency function $f(\bold x;\theta)$. Then $T=T(\bold X)$ is sufficient for $\theta$ if and only if,
$$
f(\bold x, \theta)=g(T(\bold x);\theta)h(\bold x)
$$
A sufficient statistic $T(\bold X)$ is called a minimal sufficient statistics if, for any other sufficient statistic $T'(\bold X)$, $T(\bold x)$ is a function of $T'(\bold x)$
$$
\frac{f(\bold x;\theta)}{f(\bold y;\theta)}=\frac{g(T(\bold x);\theta)h(\bold x)}{g(T(\bold y);\theta)h(\bold y)}=H(\bold x, \bold y)
$$

### Estimation

If the data generating distribution belongs to the exponential family it follows that

- MLE will be a function of sufficient statistics
- Under regularity conditions, consistency and asymptotic normality of the MLE can used for statistical inference
- Optimality: minimal sufficient statistics can be shown to be complete for full-rank exponential families. Because of this, they can be used to find the unique Minimum Variance Unbiased Estimators(MVUE) via Rao-Blackwellization

Let $X_1,...,X_n$ be an i.i.d. sample of random variables with density or frequency function $f(x;\theta)$. Let $T(\bold X)$ be a sufficient statistic for $\theta_0$ and $U(\bold X)$ and unbiased estimator of $\theta_0$. If $\tilde U(\bold X)=E[U(\bold X)|T(\bold X)]$, then $\tilde U(\bold X)$ is an unbiased estimator of $\theta$, and $var[\tilde U(\bold X)]\le var[U(\bold X)]$ for all $\theta$.

## Multivariate Normal

$$
f(\bold x)=\prod_{i=1}^d\frac{1}{\sqrt{2\pi}}exp(-\frac{1}{2}x_i^2)=\frac{1}{(2\pi)^{d/2}}exp(-\frac{1}{2}\sum_{i=1}^dx_i^2)=\frac{1}{(2\pi)^{d/2}}exp(-\frac{1}{2}\bold x^T\bold x)
$$

$$
f(\bold x;\mu,\Sigma)=\frac{1}{(2\pi)^{d/2}|\Sigma|^{1/2}}exp(-\frac{1}{2}(\bold x-\mu)^T\Sigma^{-1}(\bold x-\mu))
$$

### Maximum Likelihood Estimation

$$
\hat\mu_{ML}=\bar {\bold X}_n=\frac{1}{n}\sum_{i=1}^n\bold X_i
$$

$$
\Sigma_{ML}=\bold S_n=\frac{1}{n}\sum_{i=1}^n (\bold X_i - \bar{\bold X}_n)(\bold X_i - \bar{\bold X}_n)^T
$$

### Central Limit Theorem

$$
\bar X_n\stackrel{P}{\longrightarrow}\mu
$$

$$
\sqrt n(\bar X_n-\mu)\stackrel{D}{\longrightarrow}N(0,C)
$$

### Conditional Distribution

$$
\mu_{A|B}=\mu_A+\Sigma_{AB}\Sigma_{BB}^{-1}(x_B-\mu_B)
$$

$$
\Sigma_{A|B}=\Sigma_{AA}-\Sigma_{AB}\Sigma_{BB}^{-1}\Sigma_{BA}
$$

## Missing Data

### Missing Pattern

- Missing completely at random(MCAR): Missing data are independent of the variable itself.

$$
P(R=0|Y,X)=P(R=0)
$$

- Non-ignorable non-response: The missing pattern is function of the variable itself.

$$
P(R=0|Y,X)
$$

- Missing at Random: The missing pattern is only a function of the auxiliary variable X.

$$
P(R=0|Y,X)=P(R=0|X)
$$

### Covariance Matrix Estimation

- Complete Case Analysis: drop all observations containing missing entries, and only look at the complete records.
- Available Case Analysis: we use all univariate information available.
- Imputation: replaces the missing entries by mean of corresponding column.

- EM Algorithm: replace the unobserved part of likelihhod with its conditional expectation given the data.
  - E-step: compute $Q(\theta,\theta^{(k)})=E[log f(Y,U;\theta)|Y=y;\theta^{(k)}]$
  - M-step: maximize $Q(\theta;\theta^{(k)})$ Over $\theta$ to obtain $\theta^{(k+1)}=argmax_{\theta}Q(\theta;\theta^{(k)})$
