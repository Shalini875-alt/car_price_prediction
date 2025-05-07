# -*- coding: utf-8 -*-
"""
Vehicle Price Prediction Web App
"""

from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('rf_model.pkl', 'rb'))  # Make sure this file exists in the same directory

standard_to = StandardScaler()

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0

    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        Fuel_Type = request.form['Fuel_Type_Petrol']
        Seller_Type = request.form['Seller_Type_Individual']
        Transmission = request.form['Transmission_Manual']

        # Encoding Fuel Type
        if Fuel_Type == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif Fuel_Type == 'Diesel':
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0

        # Encoding Seller Type
        Seller_Type_Individual = 1 if Seller_Type == 'Individual' else 0

        # Encoding Transmission
        Transmission_Manual = 1 if Transmission == 'Manual' else 0

        # Calculate car age
        Num_Year = 2022 - Year

        features = [[
            Present_Price, Kms_Driven, Owner, Num_Year,
            Fuel_Type_Diesel, Fuel_Type_Petrol,
            Seller_Type_Individual, Transmission_Manual
        ]]
        prediction = model.predict(features)
        output = round(prediction[0], 2)

        if output < 0:
            return render_template('index.html', prediction_text='Sorry, you cannot sell this car.')
        else:
            return render_template('index.html', prediction_text=f'You can sell the car at ₹{output} lakhs')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
