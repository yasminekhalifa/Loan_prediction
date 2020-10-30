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
X = cleaned_data.drop(columns='Loan_Status_Y')
y = cleaned_data['Loan_Status_Y']

################# Splitting into Train -Test Data #######
from sklearn.model_selection import train_test_split
############### Handling/Imputing Missing values #############
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,stratify =y,random_state =42)
imp = SimpleImputer(strategy='mean')
imp_train = imp.fit(X_train)
X_train = imp_train.transform(X_train)
X_test_imp = imp_train.transform(X_test)

tree_clf = DecisionTreeClassifier(criterion='gini', max_depth = 3, min_samples_leaf = 2, splitter = 'random')
tree_clf.fit(X_train,y_train)

#exporting my model
pickle.dump(tree_clf,open("model.pkl","wb"))