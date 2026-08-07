students = []

n = int(input("Enter Number of Students: "))

for i in range(n):
    print("\nEnter Details of Student", i + 1)

    name = input("Name: ")
    age = int(input("Age: "))
    marks = int(input("Marks: "))

    student = {
        "Name": name,
        "Age": age,
        "Marks": marks
    }

    students.append(student)

print("\nStudent Records")

for student in students:
    print(student)