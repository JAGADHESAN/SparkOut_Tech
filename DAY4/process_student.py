marks = []

for i in range(5):
    mark = int(input("Enter Mark: "))
    marks.append(mark)

print("\nMarks:", marks)
print("Highest Mark:", max(marks))
print("Lowest Mark:", min(marks))
print("Average:", sum(marks) / len(marks))