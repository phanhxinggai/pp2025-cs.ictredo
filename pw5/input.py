import json
import math

def write_students_to_file(students):
    with open("students.txt", "w") as f:
        json.dump([student.__dict__ for student in students], f)

def write_courses_to_file(courses):
    with open("courses.txt", "w") as f:
        json.dump([course.__dict__ for course in courses], f)

def write_marks_to_file(marks):
    with open("marks.txt", "w") as f:
        json.dump(marks.marks, f)

def round_mark(mark):
    return math.floor(mark * 10) / 10
