import pandas as pd

df = pd.read_csv("students.csv")

print("===== STUDENT DATASET =====")
print(df)

print("\nTotal Students:", len(df))

print("Highest Marks:", df["Marks"].max())
print("Lowest Marks:", df["Marks"].min())
print("Average Marks:", df["Marks"].mean())

df["Result"] = df["Marks"].apply(
    lambda x: "Pass" if x >= 40 else "Fail"
)

def get_grade(mark):
    if mark >= 90:
        return "A+"
    elif mark >= 80:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 40:
        return "D"
    else:
        return "F"

df["Grade"] = df["Marks"].apply(get_grade)

print("\n===== STUDENT RESULTS =====")
print(df)

average = df["Marks"].mean()

print("\n===== ABOVE AVERAGE STUDENTS =====")
print(df[df["Marks"] > average][["Name", "Marks"]])

print("\n===== GRADE COUNT =====")
print(df["Grade"].value_counts())

df.to_csv("analyzed_students.csv", index=False)

print("\nAnalyzed dataset saved successfully!")