# Machine Learning

## Concept

- **Supervised Learning:** The model learns from a labeled dataset, trying to predict outcomes for new, unseen data based on the knowledge it has acquired from the training dataset. Common tasks include classification and regression.
- **Unsupervised Learning:** The model works with unlabeled data and tries to find underlying patterns or groupings in the data, without any explicit instructions on what to find. Common tasks include clustering and dimensionality reduction.
- **Semi-supervised Learning:** A mix of supervised and unsupervised learning, where the model learns from a partially labeled dataset, using the labeled data to learn the structure and make predictions about the unlabeled data.
- **Reinforcement Learning:** The model learns to make decisions by performing certain actions and receiving feedback in the form of rewards or penalties, aiming to maximize the cumulative reward.

## Evaluation

### Regression

- **Mean Absolute Error (MAE):** The average of the absolute differences between the predicted values and actual values. It gives an idea of how wrong the predictions were.
- **Mean Squared Error (MSE):** The average of the squared differences between the predicted values and actual values. It penalizes larger errors more than MAE does.
- **Root Mean Squared Error (RMSE):** The square root of MSE. It is in the same units as the response variable and gives a relatively high weight to large errors.
- **R-squared (Coefficient of Determination):** Measures the proportion of the variance in the dependent variable that is predictable from the independent variable(s). It provides an indication of the goodness of fit of the predictions.

### Classification

- **Accuracy:** Measures the proportion of true results (both true positives and true negatives) among the total number of cases examined. It's a good measure when the classes are balanced but can be misleading when class distribution is imbalanced.
- **Precision (Positive Predictive Value):** The ratio of true positive predictions to the total positive predictions. It is important when the cost of false positives is high.
- **Recall (Sensitivity, True Positive Rate):** The ratio of true positive predictions to the total actual positives. It is crucial when the cost of false negatives is high.
- **F1 Score:** The harmonic mean of precision and recall, providing a balance between them. It is particularly useful when the class distribution is uneven.
- **Confusion Matrix:** A table that is often used to describe the performance of a classification model on a set of test data for which the true values are known. It breaks down predictions into four parts: true positives, false positives, true negatives, and false negatives.
- **ROC Curve and AUC:** The Receiver Operating Characteristic (ROC) curve is a graphical plot that illustrates the diagnostic ability of a binary classifier system as its discrimination threshold is varied. The Area Under the ROC Curve (AUC) measures the entire two-dimensional area underneath the entire ROC curve and provides an aggregate measure of performance across all possible classification thresholds.

### Cross-Validation

- Cross-validation is a technique for model evaluation that involves splitting the dataset into multiple subsets (folds). The model is trained and tested on different combinations of these folds to ensure robust evaluation.


- In k-fold cross-validation, the dataset is divided into k subsets. The model is trained on k-1 subsets and tested on the remaining subset. This process is repeated k times, and the results are averaged to obtain a reliable estimate of model performance.


## Regularization

### Overfitting and Underfitting 

**bias–variance tradeoff** describes the relationship between a model's complexity, the accuracy of its predictions, and how well it can make predictions on previously unseen data that were not used to train the model.

- Overfitting: High variance, model too complex, fit training data too closely, resulting in poor generalization to unseen data
- Underfitting: high bias, model too simple, fail to capture pattern of training data, low accuracy

Preventing Overfitting: Common techniques include:

- Regularization (L1, L2, or both).

- Cross-validation for hyperparameter tuning.

- Increasing the size of the training dataset.

- Feature selection or reduction.

- Early stopping during training.


### Method

1. **L1 Regularization (Lasso Regression):**
   - L1 regularization adds a penalty equal to the absolute value of the magnitude of coefficients. This can lead to some coefficients being exactly zero, which means L1 regularization can also perform feature selection by eliminating some features entirely.
   - The objective function with L1 regularization is $\text{Cost} = \text{Loss}(Y, \hat{Y}) + \lambda \sum_{i} |w_i|$
2. **L2 Regularization (Ridge Regression):**
   - L2 regularization adds a penalty equal to the square of the magnitude of coefficients. This encourages smaller coefficients but does not necessarily eliminate them entirely, as L1 does.
   - The objective function with L2 regularization is $\text{Cost} = \text{Loss}(Y, \hat{Y}) + \lambda \sum_{i} w_i^2$
3. **Elastic Net:**
   - Elastic Net is a middle ground between L1 and L2 regularization, combining both penalties. It is useful when there are multiple features correlated with each other. Elastic Net can bring the benefits of both L1 (feature selection) and L2 (smooth coefficient shrinkage) regularization.
   - The objective function for Elastic Net is $\text{Cost} = \text{Loss}(Y, \hat{Y}) + \lambda_1 \sum_{i} |w_i| + \lambda_2 \sum_{i} w_i^2$

## Feature Engineering

- **Creating New Features:** Employing domain knowledge to create new features or engineer existing features for better model performance.
- **Normalization and Scaling:** Using techniques like Min-Max scaling or Z-score normalization to scale numerical features to a similar range.
- **Handling Missing Data:** Dealing with missing values through imputation techniques or encoding missingness as a separate feature.
- **Dimensionality Reduction:** Exploring methods like PCA, t-SNE, or feature selection techniques to reduce the number of features and focus on the most important ones.

### Encoding

- **Label Encoding:** Converting categorical features to ordinal values, useful when dealing with ordinal data.
- **One-Hot Encoding:** Transforming categorical variables into a binary matrix, suitable for nominal data.
- **Target Encoding:** Encoding categorical variables based on target variable statistics, which can be effective in certain situations.
- **Handling High-Cardinality Features:** Techniques for managing features with a large number of distinct categories to prevent the curse of dimensionality.

### Feature Importance

- **Understanding Feature Importance:** Realizing the role of different features in predicting the target variable.
- **Techniques to Calculate Feature Importance:** Employing methods like mean decrease in impurity (for decision trees), coefficient weights (for linear models), SHAP values, or permutation importance.
- **Feature Selection Based on Importance:** Selecting a subset of features based on their importance to improve model performance and interpretability.v

## Supervised Learning

### Linear Regression

**Linear regression** is a supervised learning algorithm used for predicting and forecasting values that fall within a continuous range, such as sales numbers or housing prices. It is a technique derived from statistics and is commonly used to establish a relationship between an input variable (X) and an output variable (Y) that can be represented by a straight line.

- **Linearity:** The relationship between the independent and dependent variables is linear.
- **Independence:** The residuals (errors) are independent.
- **Homoscedasticity:** The residuals have constant variance at every level of the independent variable(s).
- **Normal Distribution of Residuals:** The residuals are normally distributed for any value of the independent variable(s).

**Linear Algebra:**
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

**Statistical: **
$$
(Y| \bold X=\bold x)\sim N(\bold x \cdot \bold w,\sigma^2)
$$

$$
lnL(\bold w, \sigma^2)=-\frac{1}{2\sigma^2}\sum_{i=1}^{n}(y_i-\bold x_i \cdot\bold w)+\frac{n}{2}ln\frac{1}{\sigma^2}+C
$$

**Statistical Learning**

- Population risk: $E[(f(\bold X)-Y)^2]$
- Empirical risk: $\frac{1}{n}\sum_{i=1}^n(f(\bold X_i)-Y_i)^2$

### Logistic Regression

Logistic Regression models the probability that a binary outcome belongs to a particular category. 

- **Binary Outcome:** The dependent variable is binary (0/1, Yes/No, True/False).
- **Observations are Independent:** Each observation is independent of all other observations.
- **No Multicollinearity:** The independent variables should not be too highly correlated with each other.
- **Linearity of Independent Variables and Log Odds:** Although the dependent variable in logistic regression is not linear, there should be a linear relationship between the independent variables and the log odds.

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

**Information Theory: **
$$
D_{KL}(p||q)=\sum_xp(x)log(\frac{p(x)}{q(x)})=\sum_xp(x)log(p(x))-\sum_xp(x)log(q(x))
$$

$$
CrossEntropy=-y_i\log p_1-(1-y_i)\log p_0
$$

$$
Loss = \sum_{i=1}^my_i\cdot log(p_1)+(1-y_i)\cdot log(p_0)
$$

### Decision Trees

Decision Trees are a type of supervised learning algorithm (having a pre-defined target variable) that is used for both classification and regression tasks.

- **Selection of the Best Attribute:** Decision Trees use various metrics to identify the attribute that best divides the dataset into subsets of maximum homogeneity. Common metrics include Gini Impurity, Information Gain, and Variance Reduction for regression trees.
- **Tree Construction:** Starting from the root, the dataset is split based on the selected attribute into groups. This process is recursively repeated on each derived subset in a recursive manner called recursive partitioning. The recursion is completed when one of the conditions is met:
  - All tuples in a subset belong to the same attribute value.
  - There are no more remaining attributes.
  - There are no more instances.
- **Pruning:** Once a tree is built, it may be necessary to prune it to avoid overfitting. Pruning can be done by setting a maximum depth of the tree or setting a minimum number of samples required to split a node.

**Tree Models: **

- **ID3 (Iterative Dichotomiser 3):** Uses Entropy and Information Gain.

$$
H(x)=-\sum_x p(x)\log p(x)
$$

$$
Gain(D,a)=H(D)-\sum_v\frac{|D^v|}{D}H(D^v)
$$

- **C4.5:** An extension of ID3 that uses Information Gain Ratio to handle both continuous and categorical attributes.

$$
Gain\_ratio(D,a)=\frac{Gain(D,a)}{IV(a)}\
$$

$$
IV(a)=-\sum_v \frac{|D^v|}{|D|}\log \frac{|D^v|}{|D|}
$$

- **CART (Classification and Regression Trees):** Uses Gini Impurity as a metric and can be used for both classification and regression tasks.

$$
Gini(D)=\sum_kp_k(1-p_k)=1-\sum_kp_k^2
$$

$$
Gini\_index(D,a)=\sum_v\frac{|D^v|}{|D|}Gini(D^v)
$$

### Support Vector Machines

- **Hyperplane:** In SVM, a hyperplane is a decision boundary that separates different classes in the feature space. For a two-class classification problem, the goal of SVM is to find the optimal hyperplane that not only separates the two classes but does so with the maximum margin.
- **Margin:** The margin is defined as the distance between the hyperplane (decision boundary) and the closest data points from either class, known as support vectors. SVM aims to maximize this margin to improve the model's generalization ability.
- **Support Vectors:** Support vectors are the data points that lie closest to the decision boundary and are the critical elements of the dataset. The position of the hyperplane is determined based on these support vectors, hence the name "Support Vector Machine."
- **Kernel Trick:** SVMs can perform linear classification but also are capable of handling non-linear boundaries by using the kernel trick. The kernel trick involves mapping the input data into a higher-dimensional space where a linear separation is possible. Common kernels include the linear, polynomial, radial basis function (RBF), and sigmoid.


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

$$
max\sum_i \alpha_i-\frac{1}{2}\sum_i\sum_j\alpha_i\alpha_jy_iy_j\bold x_i^T\bold x_j
$$

$$
s.t. \sum_i\alpha_iy_i=0,\alpha_i\ge0
$$

### K-Nearest Neighbors

- **Distance Calculation:** When a new data point is introduced and needs to be classified (or predicted in regression), the k-NN algorithm calculates the distance from that new point to every other point in the training dataset. Common methods for calculating distance include Euclidean, Manhattan, and Minkowski distances.
- **Identify Nearest Neighbors:** After calculating the distances, the algorithm identifies the *k* nearest data points in the training dataset to the new point, where *k* is a user-specified number. These *k* data points are the "nearest neighbors."
- **Decision Rule:**
  - **For Classification:** The algorithm assigns the new data point to the class most common among its *k* nearest neighbors. If *k*=1, then the new point is simply assigned to the class of its nearest neighbor.
  - **For Regression:** The algorithm predicts the output for the new point based on the average (or another aggregate function) of the values of its *k* nearest neighbors.

### Naive Bayes

$$
P(C_k|x) = \frac{P(x|C_k) \cdot P(C_k)}{P(x)}
$$

$$
P(C_k|x_1, x_2, ..., x_n) \propto P(C_k) \cdot \prod_{i=1}^{n}P(x_i|C_k)
$$

The class that gives the highest posterior probability is chosen as the output prediction. This formula effectively allows Naive Bayes to classify new instances by assuming independence between the features in the context of the target class.

## Unsupervised Learning

### K-Means

K-means clustering is a popular unsupervised machine learning algorithm used for partitioning a dataset into K distinct, non-overlapping subsets (clusters). Each data point belongs to the cluster with the nearest mean, serving as a prototype of the cluster.

1. **Initialization:** The process begins by selecting *k* initial centroids, either randomly or based on some heuristic. Each centroid is the center of a cluster.
2. **Assignment Step:** Each data point in the dataset is assigned to the nearest centroid based on some distance metric, typically Euclidean distance. This forms *k* clusters with their respective data points.
3. **Update Step:** After all data points have been assigned to clusters, the centroids are recalculated by taking the mean of all points in each cluster.
4. **Iteration:** Steps 2 and 3 are repeated until the centroids no longer change significantly, indicating that the algorithm has converged, or until a predefined number of iterations is reached.

- **Centroids:** The center points of the clusters, which may not necessarily be a data point in the dataset.
- **Euclidean Distance:** The distance metric commonly used to measure the closeness between data points and centroids.
- **Convergence:** The algorithm is said to have converged when the assignments of data points to clusters no longer change between iterations.

### Hierarchical Clustering

Hierarchical clustering is another unsupervised machine learning algorithm used for grouping similar data points into clusters. Unlike K-means, hierarchical clustering doesn't require the pre-specification of the number of clusters (K). Instead, it creates a hierarchy of clusters, often represented as a tree-like structure (dendrogram).

1. **Initialization:**
   - Treat each data point as a singleton cluster.
   - Compute the distance (similarity) matrix between all pairs of clusters.
2. **Merge:**
   - Find the closest (most similar) pair of clusters based on the distance matrix.
   - Merge these two clusters into a new cluster.
   - Update the distance matrix.
3. **Repeat:**
   - Repeat steps 2 until only a single cluster remains, or a desired number of clusters is obtained.

### PCA

Principal Component Analysis (PCA) is a dimensionality reduction technique commonly used in data analysis and machine learning. Its primary goal is to transform a dataset into a new coordinate system, called the principal component space, where the data's variability is maximized along the new axes (principal components).

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

### T-SNE

- **High-Dimensional Space to Low-Dimensional Space:** t-SNE aims to reduce the dimensions of data by converting similarities between data points to joint probabilities and then minimizing the Kullback-Leibler divergence between the joint probabilities of the high-dimensional and low-dimensional spaces. This process preserves the local structure of the data, making it effective for visualizing clusters or groups within the data.
- **Similarity Measures:** In the high-dimensional space, t-SNE calculates the similarity between pairs of data points using the Gaussian distribution. In the low-dimensional space, it uses a t-distribution, which has heavier tails than a Gaussian distribution. This choice helps to alleviate the crowding problem, where moderate distances in the high-dimensional space collapse to very small distances in the low-dimensional space.
- **Crowding Problem:** One of the challenges in reducing dimensions is the crowding problem, which occurs because the volume of the space increases exponentially with the number of dimensions. t-SNE addresses this by using the t-distribution in the low-dimensional space, allowing it to effectively spread out data points that are moderately far apart in the high-dimensional space.
- **Optimization:** The Kullback-Leibler divergence between the probability distributions in the high-dimensional and low-dimensional spaces is minimized using gradient descent. This optimization process ensures that similar objects are modeled close together and dissimilar objects are modeled far apart in the low-dimensional space.

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