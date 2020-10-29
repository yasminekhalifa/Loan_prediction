from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import pickle
train_df = pd.read_csv('/Users/yasminekhalifa/Desktop/Loan_prediction/Data/train.csv')
train_df = train_df.drop(columns=['Loan_ID', 'Credit_History']) ## Dropping Loan ID
categorical_columns = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area','Loan_Amount_Term']
numerical_columns = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']
train_df_encoded = pd.get_dummies(train_df,drop_first=True)
cleaned_data = train_df_encoded.copy()
for column in numerical_columns:
    q1 = cleaned_data[column].quantile(0.25)
    q3 = cleaned_data[column].quantile(0.75)
    iqr = q3 - q1
    fence_low = q1 - 1.5 * iqr
    fence_high = q3 + 1.5 * iqr
    cleaned_data = cleaned_data.loc[(cleaned_data[column] > fence_low) & (cleaned_data[column] < fence_high)]

# Split Features and Target Varible
X = cleaned_data.drop(columns='Loan_Status_Y')
y = cleaned_data['Loan_Status_Y']

# Splitting into Train -Test Data
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,stratify =y,random_state =42)
# Handling/Imputing Missing values
from sklearn.impute import SimpleImputer
imp = SimpleImputer(strategy='mean')
imp_train = imp.fit(X_train)
X_train = imp_train.transform(X_train)
X_test_imp = imp_train.transform(X_test)

# create kmeans object
kmeans = KMeans(n_clusters=2)
# fit kmeans object to data
kmeans.fit(X_train)

#exporting my model
pickle.dump(kmeans,open("cluster.pkl","wb"))