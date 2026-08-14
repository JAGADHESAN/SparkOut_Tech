import pandas as pd
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("student_pass_fail.csv")

print("Student Dataset:")
print(df)

X = df[["Hours", "Attendance"]]

y = df["Pass"]

model = DecisionTreeClassifier(random_state=42)

model.fit(X, y)

print("\nDecision Tree Classifier trained successfully!")

new_student = [[6, 80]]

prediction = model.predict(new_student)

print("\nPrediction:")

if prediction[0] == 1:
    print("Student is likely to PASS")
else:
    print("Student is likely to FAIL")