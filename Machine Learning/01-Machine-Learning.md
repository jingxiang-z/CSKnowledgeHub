# 01 Machine Learning

## Table of Contents

- [Overview](#overview)
- [Learning Paradigms](#learning-paradigms)
- [Model Evaluation](#model-evaluation)
- [Regularization](#regularization)
- [Theoretical Foundations of Generalization](#theoretical-foundations-of-generalization)
- [Feature Engineering](#feature-engineering)
- [Supervised Learning Algorithms](#supervised-learning-algorithms)
- [Unsupervised Learning Algorithms](#unsupervised-learning-algorithms)
- [Ensemble Methods](#ensemble-methods)
- [Reinforcement Learning](#reinforcement-learning)
- [References](#references)

## Overview

Machine learning is a field of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. This document covers fundamental machine learning concepts organized into key domains: supervised learning (prediction from labeled data), unsupervised learning (discovering structure in unlabeled data), and reinforcement learning (sequential decision-making). The document addresses both practical algorithms and theoretical foundations including generalization, regularization, and the bias-variance tradeoff.

## Learning Paradigms

### Supervised Learning

The model learns from a labeled dataset, trying to predict outcomes for new, unseen data based on knowledge acquired from the training dataset. Common tasks include classification and regression.

**Key characteristics:**
- Requires labeled training data
- Goal is to learn mapping from inputs to outputs
- Performance measured against known correct answers

### Unsupervised Learning

The model works with unlabeled data and tries to find underlying patterns or groupings in the data, without explicit instructions on what to find. Common tasks include clustering and dimensionality reduction.

**Key characteristics:**
- No labeled data required
- Discovers hidden structure in data
- Used for exploratory data analysis

### Semi-supervised Learning

A combination of supervised and unsupervised learning, where the model learns from a partially labeled dataset, using the labeled data to learn the structure and make predictions about the unlabeled data.

**Applications:**
- When labeling data is expensive
- Large amounts of unlabeled data available
- Medical image analysis, speech recognition

### Reinforcement Learning

The model learns to make decisions by performing actions and receiving feedback in the form of rewards or penalties, aiming to maximize cumulative reward.

**Key components:**
- Agent: decision-making entity
- Environment: world the agent interacts with
- Actions: choices available to agent
- Rewards: feedback signal

## Model Evaluation

### Regression Metrics

**Mean Absolute Error (MAE):**
$$
MAE = \frac{1}{n}\sum_{i=1}^{n}|y_i - \hat{y}_i|
$$

Average of absolute differences between predicted and actual values.

**Mean Squared Error (MSE):**
$$
MSE = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2
$$

Average of squared differences, penalizes larger errors more than MAE.

**Root Mean Squared Error (RMSE):**
$$
RMSE = \sqrt{MSE}
$$

In same units as response variable, gives high weight to large errors.

**R-squared (Coefficient of Determination):**
$$
R^2 = 1 - \frac{SS_{residual}}{SS_{total}}
$$

Measures proportion of variance in dependent variable predictable from independent variables.

### Classification Metrics

**Accuracy:**
$$
Accuracy = \frac{TP + TN}{TP + TN + FP + FN}
$$

Proportion of correct predictions. Good when classes are balanced but misleading with imbalanced datasets.

**Precision (Positive Predictive Value):**
$$
Precision = \frac{TP}{TP + FP}
$$

Ratio of true positives to total positive predictions. Important when false positives are costly.

**Recall (Sensitivity, True Positive Rate):**
$$
Recall = \frac{TP}{TP + FN}
$$

Ratio of true positives to total actual positives. Important when false negatives are costly.

**F1 Score:**
$$
F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}
$$

Harmonic mean of precision and recall. Particularly useful with uneven class distribution.

**Confusion Matrix:**

|                  | Predicted Positive | Predicted Negative |
|------------------|-------------------|-------------------|
| Actual Positive  | True Positive (TP) | False Negative (FN) |
| Actual Negative  | False Positive (FP) | True Negative (TN) |

**ROC Curve and AUC:**

ROC (Receiver Operating Characteristic) curve plots true positive rate against false positive rate at various threshold settings. AUC (Area Under Curve) provides aggregate measure of performance across all classification thresholds.

### Cross-Validation

**k-Fold Cross-Validation:**

1. Split dataset into k equal-sized folds
2. For each fold:
   - Use fold as validation set
   - Use remaining k-1 folds as training set
   - Train and evaluate model
3. Average results across all k folds

Provides robust estimate of model performance and reduces overfitting.

## Regularization

### Bias-Variance Tradeoff

The **bias-variance tradeoff** describes the relationship between model complexity, prediction accuracy, and generalization to unseen data.

**Overfitting:**
- High variance, low bias
- Model too complex
- Fits training data too closely
- Poor generalization to unseen data

**Underfitting:**
- High bias, low variance
- Model too simple
- Fails to capture patterns in training data
- Low accuracy on both training and test data

**Total Error:**
$$
Error = Bias^2 + Variance + Irreducible\ Error
$$

### Regularization Methods

**L1 Regularization (Lasso):**
$$
Cost = Loss(Y, \hat{Y}) + \lambda \sum_{i} |w_i|
$$

- Adds penalty equal to absolute value of coefficients
- Can lead to sparse models (some coefficients exactly zero)
- Performs automatic feature selection

**L2 Regularization (Ridge):**
$$
Cost = Loss(Y, \hat{Y}) + \lambda \sum_{i} w_i^2
$$

- Adds penalty equal to square of coefficients
- Encourages smaller coefficients
- Does not eliminate features entirely

**Elastic Net:**
$$
Cost = Loss(Y, \hat{Y}) + \lambda_1 \sum_{i} |w_i| + \lambda_2 \sum_{i} w_i^2
$$

- Combines L1 and L2 penalties
- Useful when features are correlated
- Benefits of both feature selection and coefficient shrinkage

**Other Prevention Techniques:**
- Cross-validation for hyperparameter tuning
- Increasing training dataset size
- Feature selection or reduction
- Early stopping during training
- Dropout (for neural networks)

## Theoretical Foundations of Generalization

### Bias-Variance Tradeoff

The expected test error of a model can be decomposed into three components:
$$
\text{Expected Test Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Error}
$$

**Bias:**

Error from incorrect assumptions in the learning algorithm. High bias corresponds to underfitting.
- Simple models have high bias
- Model cannot capture true relationship
- Both training and test errors are high

**Variance:**

Error from sensitivity to small fluctuations in the training set. High variance corresponds to overfitting.
- Complex models have high variance
- Model learns noise in training data
- Low training error, high test error

**Tradeoff:**

- Increasing model complexity decreases bias but increases variance
- Optimal model balances both sources of error
- Sweet spot minimizes total expected test error

### Overfitting and Underfitting

**Underfitting:**

The model is too simple to capture the underlying structure of the data.

**Symptoms:**
- High training error
- High test error
- Model has high bias

**Solutions:**
- Increase model complexity
- Add more features
- Reduce regularization

**Overfitting:**

The model learns the training data too well, including noise and spurious patterns.

**Symptoms:**
- Low training error
- High test error
- Model has high variance

**Solutions:**
- Get more training data
- Reduce model complexity
- Apply regularization
- Use cross-validation
- Early stopping

### Double Descent Phenomenon

A modern observation that challenges the classical U-shaped bias-variance curve.

**Classical View:**

Test error decreases as model complexity increases, reaches minimum, then increases (U-shape).

**Modern Observation:**

For highly overparameterized models (parameters > data points):

1. **Underparameterized regime**: Classical bias-variance tradeoff applies
2. **Interpolation threshold**: Model can perfectly fit training data, test error peaks
3. **Overparameterized regime**: Test error decreases again as model size increases further

**Key Insights:**
- Very large models can generalize well despite perfect training fit
- Observed in deep neural networks
- Challenges traditional statistical wisdom
- Implicit regularization from optimization plays a role

### VC Dimension

Vapnik-Chervonenkis (VC) dimension measures the capacity or expressive power of a hypothesis class.

**Definition:**

The VC dimension of a hypothesis class $\mathcal{H}$ is the size of the largest set of points that can be shattered by $\mathcal{H}$.

**Shattering:**

A set of points is shattered if the hypothesis class can realize every possible labeling of those points.

**Examples:**
- Linear classifier in $\mathbb{R}^2$: VC dimension = 3
- Linear classifier in $\mathbb{R}^d$: VC dimension = $d+1$

**Sample Complexity:**

The number of training examples needed for good generalization is typically linear in the VC dimension:
$$
m = O\left(\frac{d}{\epsilon}\log\frac{1}{\delta}\right)
$$

where $d$ is VC dimension, $\epsilon$ is desired error, $\delta$ is confidence parameter.

**Implications:**
- Higher VC dimension requires more training data
- Provides theoretical bounds on generalization
- Connects model capacity to sample requirements

### Implicit Regularization

The phenomenon where the optimization algorithm itself introduces a bias toward solutions with better generalization.

**Characteristics:**
- No explicit regularization term in loss function
- Optimization dynamics (e.g., SGD) prefer certain solutions
- Mini-batch noise acts as implicit regularizer
- Early stopping provides implicit regularization

**Examples:**
- SGD tends toward flat minima in deep learning
- Gradient descent on linear models finds minimum norm solution
- Architecture choices (e.g., depth) provide inductive biases

## Feature Engineering

### Data Preprocessing

**Creating New Features:**
- Use domain knowledge to engineer features
- Polynomial features
- Interaction terms
- Aggregations and transformations

**Normalization and Scaling:**
- **Min-Max scaling**: $x' = \frac{x - x_{min}}{x_{max} - x_{min}}$
- **Z-score normalization**: $x' = \frac{x - \mu}{\sigma}$
- **Robust scaling**: Uses median and IQR

**Handling Missing Data:**
- Mean/median/mode imputation
- Forward/backward fill
- Model-based imputation
- Creating missingness indicator feature

**Dimensionality Reduction:**
- Principal Component Analysis (PCA)
- t-SNE for visualization
- Feature selection techniques

### Encoding Categorical Variables

**Label Encoding:**
- Converts categories to integers (0, 1, 2, ...)
- Suitable for ordinal data with inherent order
- Not recommended for nominal data

**One-Hot Encoding:**
- Creates binary column for each category
- Suitable for nominal data
- Increases dimensionality

**Target Encoding:**
- Encodes based on target variable statistics
- Can lead to overfitting if not done carefully
- Useful for high-cardinality features

### Feature Importance

**Methods to Calculate Importance:**
- Mean decrease in impurity (decision trees)
- Coefficient weights (linear models)
- SHAP (SHapley Additive exPlanations) values
- Permutation importance
- Feature elimination

**Applications:**
- Feature selection
- Model interpretability
- Understanding data relationships

## Supervised Learning Algorithms

### Generative vs Discriminative Algorithms

A fundamental distinction exists in how classification algorithms approach the learning problem:

**Discriminative Algorithms:**

Learn the conditional probability $P(y|\mathbf{x})$ directly or learn a direct mapping from inputs $\mathbf{x}$ to labels $y$. They find a decision boundary that separates classes.

**Examples**: Logistic Regression, Support Vector Machines, Decision Trees

**Characteristics**:
- More robust to incorrect modeling assumptions
- Typically require less training data when assumptions don't hold
- Focus directly on the classification task

**Generative Algorithms:**

Model the class priors $P(y)$ and the class-conditional probabilities $P(\mathbf{x}|y)$. They use Bayes' rule to compute the posterior $P(y|\mathbf{x})$:
$$
P(y|\mathbf{x}) = \frac{P(\mathbf{x}|y)P(y)}{P(\mathbf{x})}
$$

**Examples**: Gaussian Discriminant Analysis, Naive Bayes

**Characteristics**:
- More data-efficient when modeling assumptions are correct
- Can generate new data samples
- Can handle missing features more naturally

**Gaussian Discriminant Analysis (GDA):**

Assumes $P(\mathbf{x}|y)$ follows a multivariate normal distribution. For binary classification:
$$
P(\mathbf{x}|y=0) \sim \mathcal{N}(\mu_0, \Sigma)
$$
$$
P(\mathbf{x}|y=1) \sim \mathcal{N}(\mu_1, \Sigma)
$$

GDA and Logistic Regression often produce similar decision boundaries, but GDA is more data-efficient if its Gaussian assumption holds, while Logistic Regression is more robust when the assumption is violated.

### Linear Regression

Linear regression models the relationship between input variables and a continuous output variable using a linear function.

**Model:**
$$
y = \mathbf{w}^T\mathbf{x} + b
$$

**Matrix Form:**
$$
\mathbf{y} = \mathbf{X}\mathbf{w}
$$

**Least Squares Solution:**
$$
\mathbf{w} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}
$$

**Gradient:**
$$
\frac{\partial J}{\partial \mathbf{w}} = 2\mathbf{X}^T(\mathbf{X}\mathbf{w} - \mathbf{y})
$$

**Assumptions:**
- Linearity between features and target
- Independence of residuals
- Homoscedasticity (constant variance of residuals)
- Normal distribution of residuals

**Statistical View:**
$$
(Y|\mathbf{X}=\mathbf{x}) \sim N(\mathbf{x} \cdot \mathbf{w}, \sigma^2)
$$

**Optimization Methods:**

*Gradient Descent:* Iterative algorithm that updates parameters in the direction of steepest decrease:
$$
\mathbf{w} := \mathbf{w} - \alpha\frac{\partial J}{\partial \mathbf{w}}
$$

- **Batch Gradient Descent**: Updates after scanning entire training set
- **Stochastic Gradient Descent (SGD)**: Updates after each training example, more efficient for large datasets

*Normal Equations:* Closed-form analytical solution:
$$
\mathbf{w} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}
$$

Requires $\mathbf{X}^T\mathbf{X}$ to be invertible. No iteration needed but computationally expensive for large feature spaces.

**Probabilistic Interpretation:**

Under the assumption that errors $\epsilon^{(i)} = y^{(i)} - \mathbf{w}^T\mathbf{x}^{(i)}$ are IID Gaussian with mean zero, minimizing the least-squares cost function is equivalent to Maximum Likelihood Estimation (MLE).

### Locally Weighted Linear Regression

Locally Weighted Linear Regression (LWR) is a non-parametric regression method that fits a different linear model at each query point.

**Objective:**

For each query point $\mathbf{x}$, minimize weighted cost:
$$
J(\theta) = \frac{1}{2}\sum_{i=1}^m w^{(i)}(h_\theta(\mathbf{x}^{(i)}) - y^{(i)})^2
$$

where $w^{(i)} = \exp\left(-\frac{\|\mathbf{x}^{(i)} - \mathbf{x}\|^2}{2\tau^2}\right)$

**Characteristics:**
- Weights determined by distance from query point
- Bandwidth parameter $\tau$ controls locality
- Non-parametric: must store entire training set
- Prediction computationally expensive (requires fitting at each query)

### Logistic Regression

Logistic regression models the probability of a binary outcome.

**Model:**
$$
P(y=1|\mathbf{x}) = \frac{1}{1+e^{-\mathbf{w}^T\mathbf{x}}} = \frac{e^{\mathbf{w}^T\mathbf{x}}}{1+e^{\mathbf{w}^T\mathbf{x}}}
$$

**Loss Function (Cross-Entropy):**
$$
Loss = -\sum_{i=1}^m [y_i\log(p_1) + (1-y_i)\log(p_0)]
$$

**KL Divergence Interpretation:**
$$
D_{KL}(p||q) = \sum_x p(x)\log\frac{p(x)}{q(x)}
$$

**Assumptions:**
- Binary dependent variable
- Independent observations
- No multicollinearity
- Linearity between features and log-odds

### Decision Trees

Decision trees recursively partition the feature space based on feature values to make predictions.

**Splitting Criteria:**

**Entropy (Information Gain):**
$$
H(D) = -\sum_{k} p_k\log p_k
$$

$$
Gain(D,a) = H(D) - \sum_{v}\frac{|D^v|}{|D|}H(D^v)
$$

**Gini Impurity:**
$$
Gini(D) = 1 - \sum_{k}p_k^2
$$

$$
Gini\_index(D,a) = \sum_{v}\frac{|D^v|}{|D|}Gini(D^v)
$$

**Information Gain Ratio (C4.5):**
$$
Gain\_ratio(D,a) = \frac{Gain(D,a)}{IV(a)}
$$

where $IV(a) = -\sum_{v}\frac{|D^v|}{|D|}\log\frac{|D^v|}{|D|}$

**Tree Algorithms:**
- **ID3**: Uses entropy and information gain
- **C4.5**: Extension of ID3 with gain ratio, handles continuous attributes
- **CART**: Uses Gini impurity, supports regression

**Pruning:**
- Pre-pruning: Set maximum depth, minimum samples per split
- Post-pruning: Build full tree then remove branches

### Support Vector Machines

SVM finds the optimal hyperplane that maximally separates classes.

**Objective:**
$$
\min_{\mathbf{w},b} \frac{1}{2}\|\mathbf{w}\|^2
$$

**Subject to:**
$$
y_i(\mathbf{w}^T\mathbf{x}_i + b) \geq 1, \quad i=1,2,...,m
$$

**Lagrangian:**
$$
L(\mathbf{w}, b, \alpha) = \frac{1}{2}\|\mathbf{w}\|^2 + \sum_i\alpha_i(1 - y_i(\mathbf{w}^T\mathbf{x}_i + b))
$$

**Dual Form:**
$$
\max_\alpha \sum_i \alpha_i - \frac{1}{2}\sum_i\sum_j\alpha_i\alpha_jy_iy_j\mathbf{x}_i^T\mathbf{x}_j
$$

$$
\text{s.t. } \sum_i\alpha_iy_i = 0, \quad \alpha_i \geq 0
$$

**Key Concepts:**
- **Hyperplane**: Decision boundary separating classes
- **Margin**: Distance from hyperplane to nearest data points
- **Support Vectors**: Data points closest to decision boundary
- **Kernel Trick**: Map data to higher dimensions for non-linear separation

**Common Kernels:**
- Linear: $K(\mathbf{x}_i, \mathbf{x}_j) = \mathbf{x}_i^T\mathbf{x}_j$
- Polynomial: $K(\mathbf{x}_i, \mathbf{x}_j) = (\mathbf{x}_i^T\mathbf{x}_j + c)^d$
- RBF (Gaussian): $K(\mathbf{x}_i, \mathbf{x}_j) = \exp(-\gamma\|\mathbf{x}_i - \mathbf{x}_j\|^2)$

**Soft Margin Classification:**

To handle non-separable data and outliers, slack variables $\xi_i$ and regularization parameter $C$ are introduced:
$$
\min_{\mathbf{w},b,\xi} \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_{i=1}^m\xi_i
$$
$$
\text{s.t. } y_i(\mathbf{w}^T\mathbf{x}_i + b) \geq 1 - \xi_i, \quad \xi_i \geq 0
$$

The parameter $C$ controls the tradeoff between maximizing the margin and minimizing classification errors.

### Kernel Methods

Kernel methods enable algorithms to operate in high-dimensional feature spaces without explicitly computing the transformation.

**Feature Mapping:**

A feature map $\phi: \mathcal{X} \rightarrow \mathcal{F}$ transforms inputs into a higher-dimensional space where the data may be linearly separable.

**Kernel Trick:**

Instead of explicitly computing $\phi(\mathbf{x})$, we compute the inner product directly:
$$
K(\mathbf{x}, \mathbf{z}) = \langle\phi(\mathbf{x}), \phi(\mathbf{z})\rangle
$$

This allows algorithms to implicitly work in very high (even infinite) dimensional spaces efficiently.

**Mercer's Theorem:**

A function $K(\mathbf{x}, \mathbf{z})$ is a valid kernel if and only if the kernel matrix $\mathbf{K}$ formed from any finite set of points is symmetric and positive semi-definite:
$$
\mathbf{K}_{ij} = K(\mathbf{x}_i, \mathbf{x}_j)
$$

**Valid Kernels:**
- Must be symmetric: $K(\mathbf{x}, \mathbf{z}) = K(\mathbf{z}, \mathbf{x})$
- Kernel matrix must be positive semi-definite
- Sum and product of valid kernels are valid kernels

**Applications:**
- Support Vector Machines
- Kernel Ridge Regression
- Kernel PCA
- Gaussian Processes

### K-Nearest Neighbors

k-NN classifies data points based on the majority class of their k nearest neighbors.

**Algorithm:**
1. Choose number of neighbors k
2. Calculate distance to all training points
3. Select k nearest neighbors
4. For classification: majority vote
5. For regression: average of neighbor values

**Distance Metrics:**
- Euclidean: $d(\mathbf{x}, \mathbf{y}) = \sqrt{\sum_i(x_i - y_i)^2}$
- Manhattan: $d(\mathbf{x}, \mathbf{y}) = \sum_i|x_i - y_i|$
- Minkowski: $d(\mathbf{x}, \mathbf{y}) = (\sum_i|x_i - y_i|^p)^{1/p}$

**Characteristics:**
- Non-parametric (no training phase)
- Lazy learning (computation at prediction time)
- Sensitive to feature scaling
- Computationally expensive for large datasets

### Naive Bayes

Naive Bayes applies Bayes' theorem with the "naive" assumption of feature independence.

**Bayes' Theorem:**
$$
P(C_k|\mathbf{x}) = \frac{P(\mathbf{x}|C_k) \cdot P(C_k)}{P(\mathbf{x})}
$$

**Naive Independence Assumption:**
$$
P(C_k|x_1, x_2, ..., x_n) \propto P(C_k) \cdot \prod_{i=1}^{n}P(x_i|C_k)
$$

**Variants:**
- **Gaussian NB**: Assumes features follow normal distribution
- **Multinomial NB**: For discrete counts (e.g., word counts)
- **Bernoulli NB**: For binary features

**Advantages:**
- Fast training and prediction
- Works well with high-dimensional data
- Requires small training data
- Handles missing values well

## Unsupervised Learning Algorithms

### K-Means Clustering

K-means partitions data into K clusters by minimizing within-cluster variance.

**Algorithm:**
1. Initialize K centroids randomly
2. **Assignment**: Assign each point to nearest centroid
3. **Update**: Recalculate centroids as mean of assigned points
4. Repeat steps 2-3 until convergence

**Objective Function:**
$$
J = \sum_{i=1}^K\sum_{\mathbf{x}\in C_i}\|\mathbf{x} - \mu_i\|^2
$$

**Characteristics:**
- Simple and fast
- Requires specifying K in advance
- Sensitive to initialization (use k-means++)
- Assumes spherical clusters
- Sensitive to outliers

### Hierarchical Clustering

Builds hierarchy of clusters without requiring K to be specified in advance.

**Agglomerative (Bottom-up):**
1. Start with each point as its own cluster
2. Merge closest pair of clusters
3. Update distance matrix
4. Repeat until single cluster remains

**Linkage Methods:**
- **Single linkage**: Minimum distance between clusters
- **Complete linkage**: Maximum distance between clusters
- **Average linkage**: Average distance between clusters
- **Ward's method**: Minimizes within-cluster variance

**Advantages:**
- No need to specify K
- Produces dendrogram for visualization
- Can capture non-spherical clusters

### Principal Component Analysis (PCA)

PCA transforms data to new coordinate system where variance is maximized along new axes.

**Covariance Matrix:**
$$
\Sigma = \frac{1}{n}\sum_{i=1}^n(\mathbf{x}_i - \mu)(\mathbf{x}_i - \mu)^T
$$

**Eigendecomposition:**
$$
\Sigma = \sum_{i=1}^d\lambda_i\mathbf{v}_i\mathbf{v}_i^T
$$

where $\lambda_1 \geq \lambda_2 \geq ... \geq \lambda_d$ are eigenvalues and $\mathbf{v}_i$ are eigenvectors.

**Dimensionality Reduction:**

Project data onto top k eigenvectors:
$$
\mathbf{z} = \mathbf{V}_k^T(\mathbf{x} - \mu)
$$

**Variance Explained:**
$$
\frac{\sum_{i=1}^k\lambda_i}{\sum_{i=1}^d\lambda_i}
$$

**Applications:**
- Dimensionality reduction
- Data visualization
- Noise reduction
- Feature extraction

### Singular Value Decomposition (SVD)

Any matrix can be decomposed as:
$$
\mathbf{A} = \mathbf{U}\Sigma\mathbf{V}^T
$$

where:
- $\mathbf{U}$: left singular vectors
- $\Sigma$: diagonal matrix of singular values
- $\mathbf{V}$: right singular vectors

**Matrix Approximation:**
$$
\|\mathbf{A} - \mathbf{A}_k\|_F^2 = \sum_{i=k+1}^{rank(\mathbf{A})}\sigma_i^2
$$

**Relationship to PCA:**
$$
\mathbf{A}^T\mathbf{A} = \mathbf{V}\Sigma^2\mathbf{V}^T
$$

### t-SNE

t-SNE (t-Distributed Stochastic Neighbor Embedding) is a dimensionality reduction technique optimized for visualization.

**Key Features:**
- Converts similarities to joint probabilities
- Uses Gaussian distribution in high-dimensional space
- Uses t-distribution in low-dimensional space
- Minimizes KL divergence between distributions
- Preserves local structure

**Applications:**
- Visualizing high-dimensional data
- Exploring clusters in data
- Quality assessment of embeddings

**Limitations:**
- Computationally expensive
- Non-deterministic (different runs give different results)
- Mainly for visualization, not for dimensionality reduction

### Expectation-Maximization Algorithm

The Expectation-Maximization (EM) algorithm is used for finding maximum likelihood estimates of parameters in models with latent (unobserved) variables.

**Algorithm:**

The EM algorithm alternates between two steps:

1. **E-step (Expectation)**: Compute the posterior probability of the latent variables given the data and current parameters
$$
Q_i(z^{(i)}) = P(z^{(i)}|\mathbf{x}^{(i)};\theta)
$$

2. **M-step (Maximization)**: Update model parameters to maximize the expected log-likelihood
$$
\theta := \arg\max_\theta \sum_i\sum_{z^{(i)}}Q_i(z^{(i)})\log\frac{P(\mathbf{x}^{(i)},z^{(i)};\theta)}{Q_i(z^{(i)})}
$$

**Key Properties:**
- Iteratively maximizes a lower bound (ELBO) on the data's log-likelihood
- Guaranteed to converge (monotonically increases likelihood)
- May converge to local maximum
- Sensitive to initialization

**Applications:**
- Gaussian Mixture Models (GMM)
- Hidden Markov Models
- Missing data imputation
- Clustering with probabilistic assignments

**Mixture of Gaussians Example:**

In GMM, the E-step computes "soft" cluster assignments, and the M-step updates cluster means, covariances, and mixing coefficients.

### Independent Component Analysis

Independent Component Analysis (ICA) aims to separate a multivariate signal into additive, independent, non-Gaussian subcomponents.

**Problem Formulation:**

Given observed mixed signals $\mathbf{x} = \mathbf{A}\mathbf{s}$, where:
- $\mathbf{s}$: vector of independent source signals
- $\mathbf{A}$: unknown mixing matrix
- $\mathbf{x}$: observed mixed signals

Goal: Find unmixing matrix $\mathbf{W}$ such that $\hat{\mathbf{s}} = \mathbf{W}\mathbf{x}$ recovers the sources.

**Key Assumptions:**
- Source signals are statistically independent
- Source signals are non-Gaussian
- Mixing matrix is square and invertible

**Classic Application - Cocktail Party Problem:**

Separate individual speakers' voices from multiple microphone recordings where each microphone records a mixture of all speakers.

**Contrast with PCA:**
- PCA finds orthogonal components maximizing variance
- ICA finds independent components (stronger condition)
- PCA only requires second-order statistics
- ICA requires higher-order statistics (non-Gaussianity)

### Self-Supervised Learning and Foundation Models

The modern paradigm that has revolutionized AI, particularly in Natural Language Processing and Computer Vision.

**Core Idea:**

A large, general-purpose foundation model is first pre-trained on massive amounts of broad, unlabeled data using a self-supervised objective. This model is then adapted to a wide range of specific downstream tasks, often with very little labeled data.

**Pre-training Methods:**

*Contrastive Learning (Vision):*
- Learn similar representations for different augmented views of the same image (positive pairs)
- Learn dissimilar representations for views from different images (negative pairs)
- Examples: SimCLR, MoCo, BYOL

*Language Modeling (NLP):*
- Predict next word in a sequence: $P(x_t|x_1,...,x_{t-1})$
- Learns grammar, semantics, and world knowledge from text
- Examples: GPT, BERT (masked language modeling)

**Adaptation Methods:**

*Linear Probe:*
- Freeze pre-trained model
- Train new linear classifier on top of feature representations
- Tests quality of learned representations

*Fine-tuning:*
- Use pre-trained weights as initialization
- Train all or part of model on downstream task's labeled data
- Most common adaptation method

*Zero-Shot and In-Context Learning (Language Models):*
- No weight updates required
- Task described in natural language as a prompt
- Few examples included in prompt for in-context learning
- Model performs task on new queries

**Advantages:**
- Dramatically reduces labeled data requirements
- Transfers knowledge across tasks
- State-of-the-art performance on many benchmarks
- Enables few-shot and zero-shot learning

**Examples of Foundation Models:**
- Vision: CLIP, DINO, MAE
- Language: GPT-3/4, BERT, T5
- Multimodal: CLIP, Flamingo

## Ensemble Methods

### Bagging (Bootstrap Aggregating)

**Algorithm:**
1. Create M bootstrap samples from training data
2. Train model on each bootstrap sample
3. Aggregate predictions (voting for classification, averaging for regression)

**Average Prediction:**
$$
f_{avg}(\mathbf{x}) = \frac{1}{M}\sum_{t=1}^M f_t(\mathbf{x})
$$

**Variance Reduction:**
$$
E[(f_{avg}(\mathbf{X}) - Y)^2] = \frac{1}{M}\sum_{t=1}^M E[(f_t(\mathbf{X}) - Y)^2] - \frac{1}{2M^2}\sum_{s=1}^M\sum_{t=1}^M E[(f_s(\mathbf{X}) - f_t(\mathbf{X}))^2]
$$

**Examples:**
- Random Forest
- Bagged Decision Trees

### Boosting

Boosting sequentially trains weak learners, each focusing on examples misclassified by previous learners.

**AdaBoost Algorithm:**

For each iteration t = 1, 2, ..., T:
1. Train weak learner $h_t$ on weighted data $D_t$
2. Calculate error: $\epsilon_t = \sum_{i=1}^n D_t(i) \cdot \mathbb{1}\{h_t(\mathbf{x}_i) \neq y_i\}$
3. Calculate weight: $\alpha_t = \frac{1}{2}\log\frac{1-\epsilon_t}{\epsilon_t}$
4. Update distribution: $D_{t+1}(i) = \frac{D_t(i)}{Z_t} \exp(-\alpha_t y_i h_t(\mathbf{x}_i))$

**Final Classifier:**
$$
f(\mathbf{x}) = \text{sign}\left(\sum_{t=1}^T \alpha_t h_t(\mathbf{x})\right)
$$

**Examples:**
- AdaBoost
- Gradient Boosting
- XGBoost

## Reinforcement Learning

Reinforcement Learning (RL) is a framework for training an agent to make a sequence of decisions in an environment to maximize cumulative reward.

### Markov Decision Process (MDP)

An MDP formalizes the RL problem as a tuple $(S, A, P_{sa}, \gamma, R)$:

**Components:**
- $S$: Set of states
- $A$: Set of actions
- $P_{sa}$: State transition probabilities $P(s'|s,a)$
- $\gamma$: Discount factor $(0 \leq \gamma < 1)$
- $R$: Reward function $R(s)$ or $R(s,a)$

**Goal:**

Learn a policy $\pi: S \rightarrow A$ that maximizes the expected discounted sum of future rewards.

**Value Function:**

The value of a state under policy $\pi$:
$$
V^\pi(s) = \mathbb{E}\left[\sum_{t=0}^\infty \gamma^t R(s_t) \mid s_0=s, \pi\right]
$$

**Bellman Equation:**
$$
V^\pi(s) = R(s) + \gamma\sum_{s'}P_{s\pi(s)}(s')V^\pi(s')
$$

**Optimal Value Function:**
$$
V^*(s) = \max_\pi V^\pi(s)
$$

**Optimal Policy:**
$$
\pi^*(s) = \arg\max_a \sum_{s'}P_{sa}(s')V^*(s')
$$

### Model-Based Algorithms

These algorithms assume knowledge of transition probabilities $P_{sa}$ and reward function $R$.

**Value Iteration:**

Iteratively computes the optimal value function by applying the Bellman backup operator:
$$
V(s) := R(s) + \max_a \gamma\sum_{s'}P_{sa}(s')V(s')
$$

Algorithm:
1. Initialize $V(s) = 0$ for all states
2. Repeat until convergence:
   - For each state, update $V(s)$ using Bellman equation
3. Extract policy: $\pi(s) = \arg\max_a \sum_{s'}P_{sa}(s')V(s')$

**Policy Iteration:**

Alternates between policy evaluation and policy improvement:

1. **Policy Evaluation**: Compute $V^\pi$ for current policy by solving:
$$
V^\pi(s) = R(s) + \gamma\sum_{s'}P_{s\pi(s)}(s')V^\pi(s')
$$

2. **Policy Improvement**: Update policy to be greedy with respect to $V^\pi$:
$$
\pi(s) := \arg\max_a \sum_{s'}P_{sa}(s')V^\pi(s')
$$

### Continuous State Spaces

For problems with continuous states (e.g., robotics), discretization suffers from the curse of dimensionality.

**Value Function Approximation:**

Approximate $V(s)$ with a parameterized function:
$$
V(s) \approx \theta^T\phi(s)
$$

where $\phi(s)$ is a feature vector.

**Fitted Value Iteration:**

1. Sample states from environment
2. Compute target values using Bellman equation
3. Use supervised learning to fit $V_\theta$ to target values
4. Repeat until convergence

### Model-Free Algorithms

These algorithms learn directly from interaction without knowing $P_{sa}$ or $R$.

**Policy Gradient Methods (REINFORCE):**

Directly optimize the policy $\pi_\theta$ by performing gradient ascent on expected reward:
$$
\nabla_\theta \eta(\theta) = \mathbb{E}_\tau\left[\left(\sum_{t=0}^T \nabla_\theta \log\pi_\theta(a_t|s_t)\right) R(\tau)\right]
$$

where $\tau$ is a trajectory and $R(\tau)$ is the total reward.

**Variance Reduction with Baselines:**

Subtract a baseline $b(s_t)$ (often an estimate of the value function) to reduce variance:
$$
\nabla_\theta \eta(\theta) = \mathbb{E}\left[\sum_{t=0}^T \nabla_\theta\log\pi_\theta(a_t|s_t)(R(\tau) - b(s_t))\right]
$$

**Q-Learning:**

Learn action-value function $Q(s,a)$ off-policy:
$$
Q(s,a) := Q(s,a) + \alpha\left(r + \gamma\max_{a'}Q(s',a') - Q(s,a)\right)
$$

**Advantages:**
- Model-free: doesn't require knowing dynamics
- Can learn from experience
- Handles stochastic environments

**Challenges:**
- Sample efficiency
- Credit assignment
- Exploration vs exploitation

### Advanced Control

**LQR (Linear Quadratic Regulation):**

For finite-horizon MDPs with linear dynamics and quadratic costs:
$$
s_{t+1} = A_ts_t + B_ta_t
$$
$$
\text{cost} = s_T^TU_Ts_T + \sum_{t=0}^{T-1}(s_t^TU_ts_t + a_t^TV_ta_t)
$$

Optimal controller is linear: $a_t = -K_ts_t$

**DDP (Differential Dynamic Programming):**

For non-linear systems:
1. Linearize dynamics around nominal trajectory
2. Apply LQR to linearized system
3. Update nominal trajectory
4. Iterate until convergence

**LQG (Linear Quadratic Gaussian):**

Extends LQR to partially observable systems:
1. Use Kalman Filter to maintain belief over states
2. Apply LQR controller to mean of belief
3. Separation principle: estimation and control can be solved independently

## References

**Course Materials:**
- CS229 Machine Learning - Stanford University
- COMS W4721 Machine Learning for Data Science - Columbia University

**Foundational Resources:**

- Christopher Bishop, *Pattern Recognition and Machine Learning*
- Trevor Hastie, Robert Tibshirani, Jerome Friedman, *The Elements of Statistical Learning*
