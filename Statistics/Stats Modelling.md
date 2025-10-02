# Stats Modelling

[toc]

## Markov Model

$X_t$ denote a process taking values in a state space $S=\{1,...,S\}$. The data is of the form $X_0=s_0,...X_k=s_{t_k}$
$$
P(X_0=s_0,...X_k=s_{t_k})=P(X_0=s_0)\prod_{j=1}^nP(X_{t_j}=s_j|X_0=s_0,X_{t_1}=s_1,...,X_{t_{j-1}}=s_{j-1})
$$

- Markov Property: given the present, the future is independent of the past(first order)

$$
P(X_0=s_0,...X_k=s_{t_k})=P(X_0=s_0)\prod_{i=1}^nP(X_{t_j}|X_{t_{i-1}}=s_{i-1})
$$

- Stationary: the conditional probabilities only depend on the time differences. $P(X_t=s|X_u=r)=P(X_{t-u}=s|X_0=r)$
- Transition Probabilities: $p_{rs}=P(X_1=s|X_0=r)$

### Likelihood

$$
P(X_0=s_0,...X_k=s_{t_k})=P(X_0=s_0)\prod_{i=1}^{k-1}p_{s_is_{i+1}}=p_0\prod_{r=1}^S\prod_{s=1}^Sp_{rs}^{n_{rs}}
$$

$$
l(\bold P)=\sum_{r=1}^S\sum_{s=1}^Sn_{rs}\log p_{rs}+\log p_0
$$

## Time Series

### Measure of Dependence

- Auto Covariance: $\gamma(s,t)=cov(Y_s,Y_t)=E[(Y_t-\mu_t)(Y_s-\mu_s)]$
- Auto Correlation: $\rho(t,s)=corr(Y_t,Y_s)=\frac{\gamma(t,s)}{\sqrt{\gamma(t,t)\gamma(s,s)}}$
- Partial Auto Correlation: $\rho'_t=corr(Y_0,Y_t|Y_1,...,Y_{t-1})$

### Stationarity

- Strict Stationarity: for any finite subset, the joint distribution of $Y_{t+s}$ and $Y_s$ is the same
- Weak Stationarity: $E[Y_t]=\mu$ and $cov(Y_s,Y_{s+t})=\gamma_t$ does not depend on s
- White Noise: A stochastic process $\{Y_t\}$ is called white noise if its elements are uncorrelated with mean 0 and variance $\sigma^2$

### Autoregressive Models

AR model of order p:
$$
Y_t-\mu=\sum_{j=1}^{p}\alpha_j(Y_{t-k}-\mu)+\epsilon_t
$$

- $Y_t$ is stationary
- AR(p) is a p-order Markov process
- The partial autocorrelation is $\alpha_1$, ..., $\alpha_p$

### Moving Average Models

MA model of order q:
$$
Y_t-\mu=\sum_{j=1}^q\beta_j\epsilon_{t-j}+\epsilon_t
$$

- $E[Y_t]=\mu$ and $var(Y_t)=\sigma^2(1+\beta_1^2+...+\beta_q^2)$ for all t
- This process is stationary and such that $\rho_t=0$ For $t>q$
- Stationary autoregressive processes and moving average processes are linear processes

### ARMA Models

ARMA model of order p and q:
$$
Y_t-\mu=\sum_{j=1}^p\alpha_j(Y_{t-j}-\mu)+\sum_{j=1}^q\beta_j\epsilon_{t-j}+\epsilon_t
$$

### Maximum Likelihood Estimation

$Y_t$ is a Gaussian time series with mean zero and autocovariance function $\gamma(i,j)=E[X_iX_j]$. $\bold X_n=(X_1,...,X_n)^T$ and its covariance matrix $\bold T_n=E[\bold X_n\bold X_n^T]$.
$$
L_n(\bold T_n)=\frac{1}{(2\pi)^{-n/2}|\bold T_n|}exp(-\frac{1}{2}\bold X_n^T\bold T_n\bold X_n)
$$

- $\bold T_n$ is expressible in terms of $\theta=(\alpha_1,...,\alpha_p,\beta_1,...,\beta_q)^T$ and $\sigma^2$ for an ARMA(p,q)
- Large sample distribution $\sqrt n(\hat \theta-\theta)\stackrel{d}{\longrightarrow}N(0,I(\theta)^{-1})$

### ARIMA Models

d-fold differencing can be shown to remove a polynomial trend of order d

ARMA(p, q) with d-fold difference of $Y_t$ is known as integrated autoregressive moving average ARIMA(p, d, q)

### ARCH Models

$$
Y_t=\sigma_t\epsilon_t
$$

$$
\sigma_t^2=\beta_0+\beta_1Y_{t-1}^2
$$

- $\sigma_t^2$ is increased if the previous observation was far from 0
- Model captures changing volatility common in financial time series
- GARCH Model: $\sigma_t^2=\beta_0+\beta_1Y_{t-1}^2+\delta\sigma_{t-1}^2$

### SARIMA Models

differencing can remove seasonality by lag-d differencing, but it is not the same as d-differencing which removes trends of order d

## Linear Regression

### Straight Line Regression

$$
Y_i=\beta_0+\beta_1X_{i1}+...+\beta_dX_{id}+\epsilon_i,i=1,...,n
$$

- Response variable: $Y_i$
- Covariates: $X_{i1}, X_{i2}, ..., X_{id}$
- Noise term: $\epsilon_i$, assumed to be i.i.d. with $E[\epsilon_i]=0$ and $var[\epsilon_i]=\sigma^2$ and independent of $X_{ij}$

$$
\hat \beta=argmin||\bold Y -\bold X\bold \beta||_2^2=(\bold X^T\bold X)^{-1}\bold X^T\bold Y=\beta+(\bold X^T\bold X)^{-1}\bold X^T\epsilon
$$

- Consistency: $\hat \beta\stackrel{p}{\longrightarrow} \beta$
- Asymptotic normality: $\sqrt n(\hat \beta-\beta)\stackrel{d}{\longrightarrow}N(\bold 0,\sigma^2\bold Q^{-1})$, where $\bold Q=E[\bold X_1\bold X_1^T]$

### Normal Linear Model

$$
\hat \beta\sim N(\beta,\sigma^2(\bold X^T\bold X)^{-1})
$$

- $\hat \sigma^2=\frac{1}{n-p}||\bold Y-\bold X\hat \beta||_2^2$ is an unbiased estimator of $\sigma^2$.
- $\hat \beta$ and $\hat \sigma^2$ are independent, and $\bar Y$ and $\sum_{i=1}^n(Y_i-\bar Y)$ are independent
- for each parameter, $(\hat \beta_j-\beta_j)/\hat \sigma_{\hat \beta_j}\sim t_{n-p}$

### Likelihood Ratio

$$
\hat \beta=(\bold X^T\bold X)^{-1}\bold X^T\bold Y
$$

$$
\hat \beta_1=(\bold X_1^T\bold X_1)^{-1}\bold X_1^T\bold Y
$$

$$
2(l(\hat \beta)-l(\hat \beta_1))=n\log (1+\frac{n-p}{p-q}\frac{p-q}{n-p}\frac{||\bold Y-\bold X_1\hat \beta_1||_2^2-||\bold Y-\bold X\hat \beta||_2^2}{||\bold Y-\bold X\hat \beta||_2^2})
$$

$$
2(l(\hat \beta)-l(\hat \beta_1))=n\log (1+\frac{p-q}{n-p}F)
$$

### Box-Cox transformation

$$
y^{(\lambda)}=(y^{\lambda}-1)/\lambda, \lambda=0\ else\ \log(y)
$$

$$
f(\epsilon)=\frac{1}{\sqrt{2\pi \sigma^2}}exp(-\frac{\epsilon^2}{2\sigma^2})
$$

$$
f_Y(y)=f_{\epsilon}(g^{-1}(y))|\frac{\partial g^{-1}(y)}{\partial y}|=\frac{y_i^{\lambda-1}}{\sqrt{2\pi\sigma^2}}exp(-\frac{1}{2\sigma^2}(y_i-x_i^T\beta)^2)
$$

$$
l=-\frac{1}{2}(n\log \sigma^2+\sum(y_i-\bold x_i^T\beta)^2)+(\lambda-1)\sum \log y_i
$$

### Goodness of fit

$$
R^2=1-\frac{SS(\hat \beta)}{SS_0}
$$

$$
Adjusted-R^2=1-\frac{SS(\hat \beta)}{SS_0}\frac{n-1}{n-d-1}
$$

### Stepwise Methods

- Forward Selection: greedy model selection by sequentially increasing the dimension of the. problem by including the covariates that leas to the best imporvement of the model fit.
- Backward Selection: Backward selection starts from the model containing all terms, and then successively drops the least significant term at each stage.

Akaike Information Criterion (AIC)
$$
AIC(\hat \beta)=n\log SS(\hat \beta)+2p
$$
Bayesian Information Criterion (BIC)
$$
BIC(\hat \beta)=n\log SS(\hat \beta)+p\log n
$$
LASSO Regression
$$
\hat \beta_{lasso}=argmin\sum_{i=1}^n(y_i-\beta_0-\sum_{j=1}^px_{ij}\beta_j)^2
$$

$$
s.t. \sum_{j=1}^p|\beta_j|\le t
$$

## Generalized Linear Model

### Introduction

- The response Y to follow any exponential family distribution, not just the normal distribution
- Link the expectation of the response variable through a function g instead of making them equal to each other. The conditional variance is a known function of the mean parameter

$$
g(\mu)=g(E[Y|\bold X=\bold x])=\bold x^T\beta=\eta
$$

$$
V[Y_i|\bold X_i=\bold x_i]=\phi V(\mu_i)
$$

- Canonical link: use the function that maps the mean of our response distribution to the parameter $\theta$ which we get by writing our density in the form

$$
g(\mu)=(b')^{-1}(\mu)
$$

- Consistency and asymptotic normality

$$
Consistency:\hat \beta\stackrel{p}{\longrightarrow} \beta
$$

$$
Asymptotic\ normality:\sqrt n(\hat \beta-\beta)\stackrel{d}{\longrightarrow} N(0,I(\beta)^{-1}),I(\beta)=E[-\frac{\partial^2}{\partial \beta\partial \beta^{T}}\log f(Y_i,X_i,\beta)]
$$

### Goodness of fit

One way to access the adequacy of a model is to compare its fit with a saturated model. The maximum likelihood achievable in a model with n parameters is $l_n(y, y)$. The one evaluated at the maximum likelihood fits $\hat \mu_i=g^{-1}(x_i^T\hat \beta)$

- Scaled deviance generalizes the sum of squares errors used in linear regression

$$
D^*(\bold y,\hat \mu)=\sum_{i=1}^n2[l_n(y_i;y_i)-l_n(\hat \mu_i;y_i)]=\sum_{i=1}^n d_i
$$

- Pearson's Statistic

$$
P=\sum_{i=1}^n\frac{(y_i-\hat\mu_i)^2}{\phi V(\hat \mu_i)}
$$

## Survival Data

- The data of interest represent the length of time until some event happens
- Frequently survival data are note completely observed because the event of interest has not occurred at the time the data was recorded

### Function

- Survival function: survival function is the complement of the cdf which gives the probability of surviving at time t

$$
S(t)=P(T>t)=1-P(T\le t)=1-F(t)
$$

- Harzard function

$$
h(t)=lim_{\delta->0}\frac{P(t\le T\le t+\delta|T\ge t)}{\delta}=\frac{f(t)}{1-F(t)}=-\frac{\partial S(t)}{\partial t}
$$

### Censoring

$$
(Y_i,\delta_i)=\{min(T_i,C_i),||-_{T_i<C_i}\},i=1,2,...,n
$$

- $Y_i$ will take on the value of the event if it already happened, otherwise it will take on the value of the censoring time $C_i$.

- Random censoring: We record different experiments independently at different times.

$$
(Y_i,\delta_i)=(y_i,1)\ when\ T_i=y_i,C_i>y_i\ (event\ happened)
$$

$$
(Y_i,\delta_i)=(y_i,0)\ when\ T_i\ge y_i,C_i=y_i\ (event\ not\ happened\ yet)
$$

### Likelihood

$$
P(Y_i=y_i,\delta_i=1)=f_{\theta}(y_i)(1-G(y_i))
$$

$$
P(Y_i=y_i,\delta_i=0)=(1-F_{\theta}(y_i))g(y_i)
$$

$$
L(\theta;y,\delta)=\prod f_{\theta}(y_i)^{\delta_i}(1-F_{\theta}(y_i))^{1-\delta_i}
$$

$$
\hat \theta_{ML}=argmax\sum(\delta_i\log f_{\theta}(y_i)+(1-\delta_i)\log (1-F_{\theta}(y_i)))
$$

### Kaplan-Meier Estimator

$$
\hat S(t)=\prod (1-\frac{d_i}{r_i})
$$

$$
d_i=\sum_{j=1}^n\delta_j 1_{Y_j=t_i}(failures\ at\ t_i)
$$

$$
r_i=\sum_{j=1}^n1_{Y_j\ge t_i}(at\ risk\ at\ t_i)
$$

### Cox Regression

$$
\lambda(t|X)=\lambda_0(t)exp(X^T\beta)
$$

$\lambda_0(t)=\lambda(t|X=0)$ is called baseline hazard function. This is a semi-parametric model because the baseline hazard function is fully non-parametric.
$$
\frac{\lambda(t|X=1)}{\lambda(t|X=0)}=exp(\beta)
$$

$$
\log(\frac{\lambda(t|X_1=x_1,...,X_j=x_j+1,...,X_k=x_k)}{\lambda(t|X_1=x_1,...,X_j=x_j,...,X_k=x_k)})=\beta_j
$$

With one unit increase in $X_j$ while other covariates remain the same, the log ratio of hazard functions is $\beta_j$ times of originial log ratio of hazard function.

## Nonparameteric Regression

### Statistical Model

$$
Y_i=f(X_i)+\epsilon_i,i=1,2,...,n
$$

- $Y_i$: Response variable
- $X_i$: Covariate
- Unknown smooth regression function f
- Noise term $\epsilon_i$, assumed to be i.i.d. and independent of $X_i$

### Kernel Smoothing

$$
\hat f_h(x)=\frac{1}{nh}\sum_{i=1}^nK(\frac{x_i-x}{h})
$$

Nadaraya-Watson Estimator: a weighted average of the response variables Y within the bandwidth centered at X
$$
\hat f_{NW}(x)=\sum_{i=1}^n\frac{K(\frac{x-x_i}{h})y_i}{\sum_{j=1}^nK(\frac{x-x_j}{h})}
$$
Local Polynomials Regression: Taylor's theorem can motivate the use of local polynomial fits since it suggests that f(x) can be estimated using the observed points $x_i$
$$
f(x)=\beta_0+\beta_1(x-x_i)+...+(\beta_p)(x-x_i)^p
$$

$$
\hat \beta_x=argmin(\sum_{i=1}^n(y_i-\beta_{x0}-\beta_{x1}(x-x_i)-...-\beta_{xp}(x-x_i)^p)^2K(\frac{x-x_i}{h}))
$$

$$
\hat \beta_x=argmin((y-X_x\beta_x)^TW_x(y-X_x\beta_x))=(X_x^TW_xX_x)^{-1}X_x^TW_xy
$$

### Spline Smoothing

Approximate $f(x)$ with a linear combination of known functions $b_j(x)$
$$
f(x)=\sum_{j=0}^K\beta_j b_j(x)
$$

