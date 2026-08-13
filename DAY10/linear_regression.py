import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("student_marks.csv")

print("Student Dataset:")
print(df)

X = df[["Hours"]]
y = df["Marks"]

model = LinearRegression()

model.fit(X, y)

hours = [[7]]
prediction = model.predict(hours)

print("\nPredicted Marks for 7 Hours of Study:", prediction[0])

print("Slope:", model.coef_[0])
print("Intercept:", model.intercept_)