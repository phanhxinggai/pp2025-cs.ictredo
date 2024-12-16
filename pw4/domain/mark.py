import math

class Marks:
    def __init__(self):
        self.marks = {}

    def input_marks(self, course, students):
        print(f"Enter marks for course: {course.course_name} (ID: {course.course_id})")
        self.marks[course.course_id] = {}
        for student in students:
            mark = float(input(f"Enter mark for {student.name} (ID: {student.student_id}): "))
            rounded_mark = math.floor(mark * 10) / 10
            self.marks[course.course_id][student.student_id] = rounded_mark

    def show_marks(self, course, students):
        if course.course_id not in self.marks:
            print(f"No marks available for course {course.course_name}.")
            return
        print(f"Marks for course {course.course_name}:")
        for student in students:
            mark = self.marks[course.course_id].get(student.student_id, "N/A")
            print(f"{student.name} (ID: {student.student_id}): {mark}")