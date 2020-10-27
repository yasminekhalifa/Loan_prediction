import pickle
import flask
import json
from flask import request, render_template, redirect, url_for
import pandas as pd 
app = flask.Flask(__name__)

#loading my model
model = pickle.load(open("model.pkl","rb"))
cluster_model = pickle.load(open("cluster.pkl","rb"))
high_risk = {'pred':'1','risk':'High','banks':[{"name": "NAB", "loan": "unsecured personal loan fixed", "fixed rate": "12.69%", "image": "https://upload.wikimedia.org/wikipedia/en/thumb/f/fa/National_Australia_Bank.svg/1200px-National_Australia_Bank.svg.png" },
            {"name": "ANZ", "loan": "personal loan fixed", "fixed rate": "10.5%", "image": "https://anz.brandkit.io/a/49963"}]}

low_risk = {'pred':'1','risk':'Low','banks':[{"name": "Latitude", "loan": "secured fixed low rate", "fixed rate": "6.49%", "image": "https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F57793044%2F68388708205%2F1%2Foriginal.20190304-070337?auto=compress&s=70c45f2e99f7bc7d286c4626773ea1f0"},
            {"name": "SocietyOne", "loan": "low rate personal loan", "fixed rate": "6.99%", "image": "https://www.bestfind.com.au/wp-content/uploads/2017/07/logo-societyone.gif"}]}

#defining a route for rendering home page
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html',show=False)
    else:
        # getting an array of features from the post request's body
        feature_dict = request.get_json()
        #creating a response object
        #storing the model's prediction in the object
        feature_df = pd.DataFrame([list(map(lambda x:int(x),feature_dict.values()))],columns=feature_dict.keys())
        prediction = model.predict(feature_df)[0]
        print("**********************")
        print(feature_df)
        print(prediction)
        print("**********************")

        #returning the response object as json
        loan_amount = feature_dict["LoanAmount"]
        income = feature_dict["ApplicantIncome"]
        if prediction == 0:
            pred = get_recommendation(feature_df,income,loan_amount)
        else:
            pred = get_risk_level(feature_df)
        return flask.jsonify(pred)

def get_risk_level(feature_df):
    prediction = cluster_model.predict(feature_df)[0]
    print(prediction)
    if prediction == 0:
        return high_risk
    else:
       return low_risk

def get_recommendation(feature_df,income,loan_amount):
    prediction = model.predict(feature_df)[0]
    my_df = feature_df.copy()
    while prediction == 0 and int(my_df["ApplicantIncome"]) > 0 and int(my_df["LoanAmount"]) > 0:
        my_df["ApplicantIncome"] = int(my_df["ApplicantIncome"]) + 500
        my_df["LoanAmount"] = int(my_df["LoanAmount"]) - 5
        prediction = model.predict(my_df)[0]
    income_linked = my_df["ApplicantIncome"][0]
    loan_amount_linked = my_df["LoanAmount"][0]

    my_df1 = feature_df.copy()
    prediction = 0
    while prediction == 0 and int(my_df1["ApplicantIncome"]) > 0 and int(my_df1["LoanAmount"]) > 0:
        my_df1["LoanAmount"] = int(my_df1["LoanAmount"]) - 5
        prediction = model.predict(my_df1)[0]
    loan_amount_updated = my_df1["LoanAmount"][0]

    my_df2 = feature_df.copy()
    prediction = 0
    while prediction == 0 and int(my_df2["LoanAmount"]) > 0:
        my_df2["ApplicantIncome"] = int(my_df2["ApplicantIncome"]) + 500
        prediction = model.predict(my_df2)[0]
    income_updated = my_df2["ApplicantIncome"][0]

    print(income_updated)
    print(loan_amount_updated)
    print(income_linked)
    print(loan_amount_linked)
    return {'pred':'0',
            "income_updated":str(income_updated),
            "loan_amount_updated":str(loan_amount_updated),
            "income_linked":str(income_linked),
            "loan_amount_linked":str(loan_amount_linked)}


if __name__ == "__main__":
    app.run(debug=True)