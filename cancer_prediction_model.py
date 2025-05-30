# -*- coding: utf-8 -*-
"""Cancer_prediction_model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14b36rYX-UeLVePKYUFpI-YMQ-rshyBhk

**Cancer Prediction using Machine Learning (SVM, Random Forest, XGBoost)**

#Introduction

In this project, we develop a machine learning model to predict whether a tumor is benign or malignant using the Breast Cancer Wisconsin dataset. The goal is to build a classification model with high accuracy using:

#Support Vector Machine (SVC)

#Random Forest

#XGBoost



We also apply hyperparameter tuning with GridSearchCV and evaluate the models using metrics like accuracy, confusion matrix, and classification report.

import libraries
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import numpy as np
import pandas as pd
import seaborn as s
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
#optimum parameter choosing
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from xgboost import XGBClassifier
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

"""Load the dataset"""

# Data file is in the user’s folder
from google.colab import files
uploaded = files.upload()
data = pd.read_csv('data.csv')
display (data)

"""Display shape"""

display (data.shape)

"""create variable dataset"""

df = data
display (df)

"""print distinct value count"""

display (df['diagnosis'].value_counts())

"""Print Data Types"""

print (df.dtypes)

"""Update Date Type to Category - Diagnosis"""

df['diagnosis'] = df['diagnosis']. astype('category')
print (df.dtypes)

"""Label encoding"""

df['diagnosis'] = df['diagnosis'].cat.codes
print ('********')
print(df.dtypes)

df.head()

"""Create X & Y variable with out diagnosis column"""

x= df.drop ('diagnosis',axis =1).drop('id',axis =1)
display (x)

y = df['diagnosis']
display (y)

"""Extract all column names

"""

col = x. columns
display (col)

"""Null Check"""

display (x.isnull().sum())

"""Print Co relation"""

co_rel= x.corr()
display (co_rel)

"""
Heat map with co relation"""

plt.rcParams['figure.figsize']=(20,12)
s.set(font_scale=1.4)
# In co relation 1 is the highest and -1 is lowest
s.heatmap (co_rel,cmap = 'coolwarm',annot = True)
plt.show()

"""
Heat map with out corelation value – Annot = None
"""

plt.rcParams['figure.figsize']=(20,12)
s.set(font_scale=1.4)
# In co relation 1 is the highest and -1 is lowest
s.heatmap (co_rel,cmap = 'coolwarm',annot = None)
plt.show()

"""Create Box plot"""

#box plot to check the outliers. Not going to remove outliers since this data is important.
# Observation, when 'diagnosis' is "B", the values are lower
plt.rcParams['figure.figsize']=(20,8)
f, (ax1,ax2,ax3,ax4,ax5) = plt.subplots (1,5)
s.boxplot ( x= df['diagnosis'], y = df['radius_mean'], ax = ax1)
s.boxplot (x= df['diagnosis'], y = df['texture_mean'], ax = ax2)
s.boxplot (x= df['diagnosis'], y = df['perimeter_mean'], ax = ax3)
s.boxplot (x= df['diagnosis'], y = df['area_mean'] , ax = ax4)
s.boxplot (x= df['diagnosis'], y = df['smoothness_mean']  , ax = ax5)
f .tight_layout()

f, (ax1,ax2,ax3,ax4,ax5) = plt.subplots (1,5)
s.boxplot (x= df['diagnosis'], y = df['compactness_mean'], ax = ax1)
s.boxplot (x= df['diagnosis'], y = df['concavity_mean'] , ax = ax2)
s.boxplot (x= df['diagnosis'], y = df['concave points_mean'] , ax = ax3)
s.boxplot (x= df['diagnosis'], y = df['symmetry_mean'], ax = ax4)
s.boxplot (x= df['diagnosis'], y = df['fractal_dimension_mean'] , ax = ax5)
f .tight_layout()
plt.show()

"""Distribution plot

"""

g = s.FacetGrid (df,col = 'diagnosis', hue = 'diagnosis')
g.map (s.distplot, "radius_mean", hist = False, rug = True)

g = s.FacetGrid (df,col = 'diagnosis', hue = 'diagnosis')
g.map (s.distplot, 'texture_mean', hist = False, rug = True)

g = s.FacetGrid (df,col = 'diagnosis', hue = 'diagnosis')
g.map (s.distplot, 'perimeter_mean', hist = False, rug = True)

g = s.FacetGrid (df,col = 'diagnosis', hue = 'diagnosis')
g.map (s.distplot, "area_mean", hist = False, rug = True)

g = s.FacetGrid (df,col = 'diagnosis', hue = 'diagnosis')
g.map (s.distplot, "smoothness_mean", hist = False, rug = True)

g = s.FacetGrid (df,col = 'diagnosis', hue = 'diagnosis')
g.map (s.distplot, "compactness_mean", hist = False, rug = True)

g = s.FacetGrid (df,col = 'diagnosis', hue = 'diagnosis')
g.map (s.distplot, "concavity_mean", hist = False, rug = True)

g = s.FacetGrid (df,col = 'diagnosis', hue = 'diagnosis')
g.map (s.distplot, "concave points_mean", hist = False, rug = True)

g = s.FacetGrid (df,col = 'diagnosis', hue = 'diagnosis')
g.map (s.distplot, "symmetry_mean", hist = False, rug = True)

g = s.FacetGrid (df,col = 'diagnosis', hue = 'diagnosis')
g.map (s.distplot, "fractal_dimension_mean", hist = False, rug = True)
plt.show()

"""Box plot"""

plt.rcParams['figure.figsize']=(20,8)
f, (ax1,ax2,ax3,ax4,ax5) = plt.subplots (1,5)
s.boxplot (x= df['diagnosis'], y = df['radius_se'], ax = ax1,palette = 'cubehelix')
s.boxplot (x= df['diagnosis'], y = df['texture_se'], ax = ax2,palette = 'cubehelix')
s.boxplot (x= df['diagnosis'], y = df['perimeter_se'] , ax = ax3,palette = 'cubehelix')
s.boxplot (x= df['diagnosis'], y = df['area_se'], ax = ax4,palette = 'cubehelix')
s.boxplot (x= df['diagnosis'], y = df['smoothness_se'], ax = ax5,palette = 'cubehelix')
f .tight_layout()

f, (ax1,ax2,ax3,ax4,ax5) = plt.subplots (1,5)
s.boxplot (x= df['diagnosis'], y = df['compactness_se'], ax = ax1,palette = 'cubehelix')
s.boxplot (x= df['diagnosis'], y = df['concavity_se'], ax = ax2,palette = 'cubehelix')
s.boxplot (x= df['diagnosis'], y = df['concave points_se'],  ax = ax3,palette = 'cubehelix')
s.boxplot (x= df['diagnosis'], y = df['symmetry_se'], ax = ax4,palette = 'cubehelix')
s.boxplot (x= df['diagnosis'], y = df['fractal_dimension_se'], ax = ax5,palette = 'cubehelix')
f .tight_layout()
plt.show()

"""Box plot"""

plt.rcParams['figure.figsize']=(20,8)
f, (ax1,ax2,ax3,ax4,ax5) = plt.subplots (1,5)
s.boxplot (x= df['diagnosis'], y = df['radius_worst'], ax = ax1,palette = 'coolwarm')
s.boxplot (x= df['diagnosis'], y = df['texture_worst'], ax = ax2,palette = 'coolwarm')
s.boxplot (x= df['diagnosis'], y = df['perimeter_worst'], ax = ax3,palette = 'coolwarm')
s.boxplot (x= df['diagnosis'], y = df['area_worst'], ax = ax4,palette = 'coolwarm')
s.boxplot (x= df['diagnosis'], y = df['smoothness_worst'], ax = ax5,palette = 'coolwarm')
f .tight_layout()

f, (ax1,ax2,ax3,ax4,ax5) = plt.subplots (1,5)
s.boxplot (x= df['diagnosis'], y = df['compactness_worst'], ax = ax1,palette = 'coolwarm')
s.boxplot (x= df['diagnosis'], y = df['concavity_worst'] , ax = ax2,palette = 'coolwarm')
s.boxplot (x= df['diagnosis'], y = df['concave points_worst'], ax = ax3,palette = 'coolwarm')
s.boxplot (x= df['diagnosis'], y = df['symmetry_worst'], ax = ax4,palette = 'coolwarm')
s.boxplot (x= df['diagnosis'], y = df['fractal_dimension_worst'], ax = ax5,palette = 'coolwarm')
f .tight_layout()
plt.show()

"""Function for Model fitting and best parameter values"""

def FitModel(X, Y, algo_name, algorithm, gridSearchParams, cv):
    np.random.seed(10)
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    grid = GridSearchCV(estimator=algorithm, param_grid=gridSearchParams,
                        cv=cv, scoring='accuracy', verbose=1, n_jobs=-1)

    grid_result = grid.fit(x_train, y_train)
    best_params = grid_result.best_params_
    pred = grid_result.predict(x_test)
    cm = confusion_matrix(y_test, pred)

    print(pred)
    pickle.dump(grid_result, open(algo_name, 'wb'))

    print('Best Params :', best_params)
    print('Classification Report:', classification_report(y_test, pred))
    print('Accuracy Score', accuracy_score(y_test, pred))
    print('Confusion Matrix :\n', cm)

"""**Train models using fitmodel**
SVC model
"""

param = {
    'C': [0.1, 1, 100, 1000],
    'gamma': [0.0001, 0.001, 0.005, 0.1, 1, 3, 5, 10, 100]
}
FitModel(x, y, 'SVC', SVC(), param, cv=10)

"""Random forest model"""

param = { 'n_estimators': [100, 500, 1000, 2000] }
FitModel(x, y, 'Random Forest', RandomForestClassifier(), param, cv=10)

"""XG boost model"""

param = { 'n_estimators': [100, 500, 1000, 2000] }
FitModel(x, y, 'XGBoost', XGBClassifier(), param, cv=10)

"""Balancing the Data"""

pip install imblearn

"""Over sampling algorithm"""

from imblearn.over_sampling import SMOTE

"""Data split"""

display (df['diagnosis'].value_counts())

"""Over Sampling"""

sm = SMOTE(random_state =42)
X_res, Y_res = sm.fit_resample (x, y)

"""Print count"""

display (Y_res.value_counts())

"""Create model with resample data"""

# Random Forest Classifier
rf_param = { 'n_estimators': [100, 500, 1000, 2000] }
FitModel(X_res, Y_res, 'Random Forest', RandomForestClassifier(), rf_param, cv=10)

# Support Vector Machine
svc_param = {
    'C': [0.1, 1, 100, 1000],
    'gamma': [0.0001, 0.001, 0.005, 0.1, 1, 3, 5, 10, 100]
}
FitModel(X_res, Y_res, 'SVC', SVC(), svc_param, cv=10)

# XGBoost Classifier
xgb_param = { 'n_estimators': [100, 500, 1000, 2000] }
FitModel(X_res, Y_res, 'XGBoost', XGBClassifier(), xgb_param, cv=10)

"""Load pickle file XG boost"""

load_model =pickle.load(open("XGBoost","rb"))

"""Prediction"""

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(X_res, Y_res, test_size=0.2, random_state=10)

pred1 = load_model.predict (x_test)
print (pred1)

"""Best parameters"""

load_model.best_params_

"""Accuracy score"""

print (accuracy_score (pred1,y_test))

"""Load Pickle file Support Vector Machine"""

load_model =pickle.load(open("SVC","rb"))
pred1 = load_model.predict (x_test)
print (load_model.best_params_)
print (accuracy_score (pred1,y_test))
display (pred1)

"""Load Pickle file Random Forest"""

load_model =pickle.load(open("Random Forest","rb"))
pred1 = load_model.predict (x_test)
print (load_model.best_params_)
print (accuracy_score (pred1,y_test))
display (pred1)

"""#Conclusion

This project demonstrated how to build and evaluate multiple machine learning classifiers for cancer detection. After tuning hyperparameters and comparing results, the trained models are saved for future use.
"""