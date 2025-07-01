import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

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

# Initialize models
models = {
    "Random Forest": RandomForestClassifier(),
    "SVM": SVC(),
    "Logistic Regression": LogisticRegression()
}

# Train and evaluate each model
for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"{name} Accuracy: {accuracy:.2f}")

# Initialize the Random Forest model
model = RandomForestClassifier()

# Train and evaluate the Random Forest model
model.fit(X_train, y_train)
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Random Forest Accuracy: {accuracy:.2f}")

# Predict on new input
new_data = [[0, 1]]
prediction = model.predict(new_data)
result = le.inverse_transform(prediction)
print(f"Random Forest Prediction for {new_data}: {result[0]}")