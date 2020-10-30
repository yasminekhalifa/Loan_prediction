from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import pickle
train_df = pd.read_csv('/Users/yasminekhalifa/Desktop/Loan_prediction/Data/train.csv')
train_df = train_df.drop(columns=['Loan_ID', 'Credit_History']) ## Dropping Loan ID and credit history 
categorical_columns = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area','Loan_Amount_Term']
numerical_columns = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']
train_df_encoded = pd.get_dummies(train_df,drop_first=True)
class_df = train_df_encoded.copy()
for column in numerical_columns:
    q1 = class_df[column].quantile(0.25)
    q3 = class_df[column].quantile(0.75)
    iqr = q3 - q1
    fence_low = q1 - 1.5 * iqr
    fence_high = q3 + 1.5 * iqr
    class_df = class_df.loc[(class_df[column] > fence_low) & (class_df[column] < fence_high)]

class_df = class_df[class_df['Loan_Status_Y'] == 1]
class_df = class_df.drop(columns=['Loan_Status_Y'])

X = class_df
# Handling/Imputing Missing values
from sklearn.impute import SimpleImputer
imp = SimpleImputer(strategy='mean')
imp_train = imp.fit(X)
X_train = imp_train.transform(X)

from sklearn.cluster import KMeans
import numpy as np
# create kmeans object
kmeans = KMeans(n_clusters=2,algorithm='full')
labels = [0 , 1]
# fit kmeans object to data
kmeans.fit(X_train)

#exporting my model
pickle.dump(kmeans,open("cluster.pkl","wb"))