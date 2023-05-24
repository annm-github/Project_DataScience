
from flask import Flask,render_template,request
import pickle
import numpy as np

model = pickle.load(open('Cboost.pkl','rb'))

Sc = pickle.load(open('scaler.pkl','rb'))#min max scaler 

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict_mag():
    Latitude = float(request.form.get("LT"))
    Longitude = float(request.form.get("LG"))
    Depth = float(request.form.get("DH"))
    Nst = int(request.form.get("NT"))
    Gap = float(request.form.get("GP"))
    MagNst = int(request.form.get("MN"))



    result = model.predict(np.array(Sc.transform([[Latitude,Longitude, Depth, Nst, Gap, MagNst]])).reshape(1, 6))
    result = result.item()

    if result <= 3.9:
        magnitude_category = "Minor-Earthquake"
    elif result <= 4.9:
        magnitude_category = "Light-Earthquake"    
    elif result <= 5.9:
        magnitude_category = "Moderate-Earthquake"
    elif result <= 6.9:
        magnitude_category = "Strong-Damage-Expected"
    elif result >= 7:
        magnitude_category = "Major-Damage-Expected"

    return render_template('result.html', result="The Earthquake Magnitude is {:.2f}".format(result), category=magnitude_category)

if __name__=='__main__':
    app.run(debug=True)