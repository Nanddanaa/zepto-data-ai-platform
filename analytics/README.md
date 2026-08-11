# Analytics Module

This module is done using the Titanic dataset. In this module I did data cleaning, EDA, visualization, classification and regression.

The dataset is loaded using seaborn in the EDA notebook and saved as `titanic.csv`. The modeling notebook reads this csv file instead of loading the dataset again.

The analytics module contains:

- `analytics_01_eda.ipynb` - Data cleaning, EDA and data story
- `analytics_02_modeling.ipynb` - Classification, regression and model evaluation
- `titanic.csv` - Offline copy of Titanic dataset
- `best_pipeline.joblib` - Saved final machine learning pipeline


## Part A - Data Cleaning and EDA

### Missing Values

After loading the dataset I checked the percentage of missing values.

The missing values were:

- age - 19.87%
- embarked - 0.22%
- embark_town - 0.22%
- deck - 77.22%

According to the given rule, if missing values are below 5% the rows should be dropped and if it is between 5% to 30% it should be imputed.

Age has 19.87% missing values, so I filled the missing age values using median.

Embarked and embark_town have only 0.22% missing values, so I dropped those rows.

Deck has 77.22% missing values. This is very high and imputing this much missing data may not give reliable information, so I dropped the deck column.


## Age and Fare Analysis

I used histogram and box plot to understand the distribution of age and fare.

Using the IQR method, age has 65 outliers and fare has 114 outliers.

Fare has many high value outliers. The mean of fare is greater than median and median is greater than mode.

So the fare distribution is right skewed because:

`Mean > Median > Mode`


## Survival Analysis

I calculated survival rate based on sex, passenger class and both sex and passenger class.

Female passengers have much higher survival rate compared to male passengers.

First class passengers have better survival rate compared to second and third class passengers.

When sex and passenger class are considered together, females have better survival rate in all passenger classes. Female passengers in first and second class have especially high survival rate.


## Correlation Analysis

I created the correlation matrix using only these six columns:

`survived`, `pclass`, `age`, `sibsp`, `parch`, `fare`

I did not include `adult_male` and `alone` because they are derived columns and the assignment asked to exclude them.

The two strongest correlations are:

1. pclass and fare = -0.548
2. sibsp and parch = 0.415

Pclass and fare have a negative correlation. This means when passenger class number increases from first class towards third class, fare generally decreases.

Sibsp and parch have a positive correlation. This shows that passengers travelling with siblings or spouse also have some tendency to travel with parents or children.


## Data Story

### Chart 1 - Survival based on Sex and Passenger Class

Female passengers have higher survival rate than male passengers in every passenger class.

First and second class females have very high survival rate. Third class passengers have lower survival compared to the higher classes.

This shows that both sex and passenger class had an effect on survival.


### Chart 2 - Survival based on Age and Sex

The median age of survived male and female passengers is almost same.

Most of the survived passengers are mainly in the younger and middle age groups. There are also some male infants who did not survive while many female infants survived.

There are many older male passengers among the passengers who did not survive.


### Chart 3 - Age, Fare, Sex and Survival

Passengers who paid higher fares include many survivors, especially female passengers.

Most passengers are concentrated in the lower fare range. The graph also shows some passengers who paid very high fares.

This shows that fare, sex and survival have some relationship, but fare alone cannot explain survival.


### Chart 4 - Fare by Passenger Class and Survival

The fare difference is very clear between passenger classes.

In first class, the median fare of survivors is higher than the median fare of non-survivors. Second and third class fares are much lower compared to first class.

There are also some very high fare outliers in first class.


## Standardization Check

I standardized age and fare using z-score standardization.

Before standardization, age and fare had different means and standard deviations. After standardization, both columns have approximately mean 0 and standard deviation 1.

This standardization was only done as an EDA check. It was not used for the modeling data because the modeling pipeline performs its own preprocessing using only the training data.


# Part B - Modeling

## Train Test Split

The target variable for classification is `survived`.

The dataset has around 61.62% not survived passengers and 38.38% survived passengers. Because the classes are not perfectly balanced, I used stratified train test split.

Stratification keeps approximately the same survived and not survived proportion in both training and testing data.


## Preprocessing

The train test split was done before preprocessing to avoid data leakage.

For numeric columns, missing values are handled using median imputation and the values are standardized using StandardScaler.

For categorical columns, missing values are handled using most frequent value and OneHotEncoder is used to convert categories into numeric form.

All these preprocessing steps are included inside the pipeline. They are fitted using training data and the test data is only transformed using the already fitted preprocessing steps.


## Classification Models

I trained three classification models using the same train and test split:

- Logistic Regression
- Decision Tree
- Random Forest

The Decision Tree was also visualized using `plot_tree` with feature names and class names.


## Classification Model Comparison

| Model | Accuracy | Precision | Recall | F1 | AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.804 | 0.793 | 0.667 | 0.724 | 0.843 |
| Decision Tree | 0.821 | 0.794 | 0.725 | 0.758 | 0.791 |
| Random Forest | 0.810 | 0.769 | 0.725 | 0.746 | 0.830 |

Decision Tree has the highest accuracy of 0.821, precision of 0.794 and F1 score of 0.758.

Logistic Regression has the highest AUC of 0.843.

Decision Tree and Random Forest have the highest recall of 0.725. Overall Decision Tree performed better across most of the main classification metrics.


## ROC Curve

Logistic Regression has the highest AUC of 0.843, followed by Random Forest with 0.830 and Decision Tree with 0.791.

This shows that Logistic Regression has better ability to separate survived and not survived passengers compared to the other two models.


## Imbalance Handling

The original target distribution is:

- Not survived - 61.62%
- Survived - 38.38%

I compared baseline Logistic Regression, class weight balanced Logistic Regression and SMOTE.

| Method | Precision | Recall | F1 |
|---|---:|---:|---:|
| Baseline | 0.793 | 0.667 | 0.724 |
| Class Weight | 0.730 | 0.783 | 0.755 |
| SMOTE | 0.740 | 0.783 | 0.761 |

Baseline has the highest precision of 0.793.

Class Weight and SMOTE both have the highest recall of 0.783. SMOTE has the highest F1 score of 0.761.

So among the three methods, SMOTE performed better based on F1 score and it also improved recall compared to baseline. SMOTE was applied only to training data to avoid data leakage.


## Random Forest Hyperparameter Tuning

I used GridSearchCV to find the best combination of `n_estimators`, `max_depth` and `max_features` for Random Forest.

The best parameters were:

- n_estimators = 50
- max_depth = 5
- max_features = log2

The OOB score of the best Random Forest model was around 0.827.

OOB score gives another way to check Random Forest performance using the training samples which were not selected for individual trees.


# Regression

I also created a multivariate Linear Regression model to predict fare from the other available features.

The regression results are:

| Model | MAE | RMSE | R2 | Adjusted R2 |
|---|---:|---:|---:|---:|
| Linear Regression | 20.898 | 30.533 | 0.398 | 0.369 |

The Linear Regression model has MAE of 20.898 and RMSE of 30.533.

The R2 score is 0.398, which means the model explains around 39.8% of the variation in fare.

The Adjusted R2 is 0.369, which is slightly lower than R2 because it also considers the number of features used in the model.


## Residual Plot

The residual plot shows heteroscedasticity because the residuals are not evenly spread around zero.

As the predicted fare increases, the spread of residuals becomes larger. There are also some large positive and negative residuals for higher predicted fare values.

This means the prediction errors do not have constant spread across all predicted fare values.


# Final Model Comparison

Classification and regression metrics are shown separately because they measure different types of model performance and cannot be directly compared.

### Classification

| Model | Accuracy | Precision | Recall | F1 | AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.804 | 0.793 | 0.667 | 0.724 | 0.843 |
| Decision Tree | 0.821 | 0.794 | 0.725 | 0.758 | 0.791 |
| Random Forest | 0.810 | 0.769 | 0.725 | 0.746 | 0.830 |

### Regression

| Model | MAE | RMSE | R2 | Adjusted R2 |
|---|---:|---:|---:|---:|
| Linear Regression | 20.898 | 30.533 | 0.398 | 0.369 |


# Final Recommendation

Decision Tree performed better overall compared to Logistic Regression and Random Forest.

It has the highest accuracy of 0.821, precision of 0.794 and F1 score of 0.758. Decision Tree and Random Forest have the highest recall of 0.725, while Logistic Regression has the highest AUC of 0.843.

So I would choose Decision Tree as the final classifier because it performed better across most of the main classification metrics.


## Saving the Final Model

I selected Decision Tree as the final model based on the overall classification performance.

I saved the complete Decision Tree pipeline using joblib. The saved pipeline contains both preprocessing steps and the trained model.

After loading the saved pipeline again, the original pipeline and loaded pipeline gave the same predictions on raw test data.

This confirms that the complete pipeline was saved correctly and can be used on new raw data without manually doing preprocessing again.
