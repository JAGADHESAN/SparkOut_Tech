student = {}

student["Name"] = input("Enter Name: ")
student["Age"] = int(input("Enter Age: "))
student["Department"] = input("Enter Department: ")
student["Marks"] = int(input("Enter Marks: "))

print("\nStudent Details")

for key, value in student.items():
    print(key, ":", value)