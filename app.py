from flask import Flask, render_template, request
import pickle
import numpy as np
from database import *
import serial
import time
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import warnings
warnings.filterwarnings('ignore')
app = Flask(__name__,static_url_path='/static')

# Load the machine learning model
 


@app.route('/p')
def p():
    

    # Define the serial port and baud rate.
    # Ensure 'COM3' (or '/dev/ttyUSB0' for Linux) is replaced with the correct port name.
    ser = serial.Serial('COM7', 9600, timeout=1)

    # Give some time for the serial connection to establish
    time.sleep(2)

    try:
        while True:
            # Read a line of data from the serial port
            line = ser.readline().decode('utf-8').rstrip()
            data=line
            if line:
                print(f"Received: {line}")
                

                # Split the string by commas
                values = data.split(',')

                # Assign each value to a variable
                var1 = int(values[0])
                var2 = int(values[1])
               

                # Print the variables to verify
                print(f"var1: {var1}")
                print(f"var2: {var2}")
                
                # Write the received data to a CSV file
                with open('received_data.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Received Data'])
                    writer.writerow([line])
                
                # Break the loop after writing the first received data
                break

    except KeyboardInterrupt:
        print("Program interrupted")

    finally:
        ser.close()
        print("Serial connection closed")
    return render_template('index.html',a=var1, b=var2 )

@app.route('/')
def m():
    return render_template('main.html')

@app.route('/l')
def l():
    return render_template('login.html')

@app.route('/h')
def h():
    return render_template('home.html')

@app.route('/r')
def r():
    return render_template('register.html')

@app.route('/m')
def menu():
    return render_template('menu.html')



@app.route("/register",methods=['POST','GET'])
def signup():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        status = user_reg(username,email,password)
        if status == 1:
            return render_template("/login.html")
        else:
            return render_template("/register.html",m1="failed")        
    

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        status = user_loginact(request.form['username'], request.form['password'])
        print(status)
        if status == 1:                                      
            return render_template("/home.html", m1="sucess")
        else:
            return render_template("/login.html", m1="Login Failed")

@app.route('/predict', methods=['POST'])
def predict():
    # Get the user input
    ui=""
    prediction_class = ""
    prediction_message = ""
    colour = int(request.form.get("1"))
    chemical = int(request.form.get("2"))
   
    # Load the data
    df = pd.read_csv("ripening_data.csv")

    # Preprocess labels
    le = LabelEncoder()
    df['Ripen'] = le.fit_transform(df['Ripen'])  # Encode 'Ripen' column

    # Separate features and labels
    X = df[['Color', 'Chemical']]
    y = df['Ripen']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Initialize the Random Forest model
    model = RandomForestClassifier()

    # Train and evaluate the Random Forest model
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Random Forest Accuracy: {accuracy:.2f}")

    # Predict on new input
    new_data = [[colour, chemical]]
    prediction = model.predict(new_data)
    result = le.inverse_transform(prediction)
    print(f"Random Forest Prediction for {new_data}: {result[0]}")
    print(result)
 
 

    

    return render_template("result.html", prediction_message=result)


if __name__ == "__main__":
    app.run(debug=True, port=5112)