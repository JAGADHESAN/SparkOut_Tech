import pandas as pd
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("student_pass_fail.csv")

print("Student Dataset:")
print(df)

X = df[["Hours", "Attendance"]]

y = df["Pass"]

model = LogisticRegression()

model.fit(X, y)

new_student = [[6, 80]]

prediction = model.predict(new_student)

print("\nPrediction:")

if prediction[0] == 1:
    print("Student is likely to PASS")
else:
    print("Student is likely to FAIL")