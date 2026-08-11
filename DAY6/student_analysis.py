import pandas as pd

df = pd.read_csv("students.csv")

print("Student Data")
print(df)

print("\nHighest Marks:", df["Marks"].max())
print("Lowest Marks:", df["Marks"].min())
print("Average Marks:", df["Marks"].mean())

print("\nStudents Scoring Above 90")
print(df[df["Marks"] > 90])