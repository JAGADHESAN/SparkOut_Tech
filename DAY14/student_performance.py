import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

df = pd.read_csv("student_performance.csv")

print("===== STUDENT PERFORMANCE DATASET =====")
print(df)

X = df[["StudyHours", "Attendance", "AssignmentScore"]]

y = df["Performance"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

model = DecisionTreeClassifier(random_state=42)

model.fit(X_train, y_train)

print("\nModel trained successfully!")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n===== MODEL EVALUATION =====")
print("Actual Values:", y_test.values)
print("Predicted Values:", y_pred)
print("Accuracy:", accuracy)
print("Accuracy Percentage:", accuracy * 100, "%")

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

new_student = [[6, 85, 80]]

prediction = model.predict(new_student)

print("\n===== NEW STUDENT PREDICTION =====")

if prediction[0] == 1:
    print("Prediction: Good Performance")
else:
    print("Prediction: Needs Improvement")