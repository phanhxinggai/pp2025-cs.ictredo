# 1.student.mark.oop.py

class Student:
    def __init__(self, student_id, name, dob):
        self.student_id = student_id
        self.name = name
        self.dob = dob

    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, DoB: {self.dob}"


class Course:
    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name

    def __str__(self):
        return f"ID: {self.course_id}, Name: {self.course_name}"


class Marks:
    def __init__(self):
        self.marks = {}

    def input_marks(self, course, students):
        print(f"Enter marks for course: {course.course_name} (ID: {course.course_id})")
        self.marks[course.course_id] = {}
        for student in students:
            mark = float(input(f"Enter mark for {student.name} (ID: {student.student_id}): "))
            self.marks[course.course_id][student.student_id] = mark

    def show_marks(self, course, students):
        if course.course_id not in self.marks:
            print(f"No marks available for course {course.course_name}.")
            return
        print(f"Marks for course {course.course_name}:")
        for student in students:
            mark = self.marks[course.course_id].get(student.student_id, "N/A")
            print(f"{student.name} (ID: {student.student_id}): {mark}")


class StudentManagement:
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = Marks()

    def input_students(self):
        num_students = int(input("Enter the number of students: "))
        for _ in range(num_students):
            student_id = input("Enter student ID: ")
            name = input("Enter student name: ")
            dob = input("Enter student DoB (YYYY-MM-DD): ")
            self.students.append(Student(student_id, name, dob))

    def input_courses(self):
        num_courses = int(input("Enter the number of courses: "))
        for _ in range(num_courses):
            course_id = input("Enter course ID: ")
            course_name = input("Enter course name: ")
            self.courses.append(Course(course_id, course_name))

    def list_students(self):
        print("List of students:")
        for student in self.students:
            print(student)

    def list_courses(self):
        print("List of courses:")
        for course in self.courses:
            print(course)

    def input_marks(self):
        self.list_courses()
        course_id = input("Enter the course ID to input marks: ")
        selected_course = next((course for course in self.courses if course.course_id == course_id), None)
        if selected_course:
            self.marks.input_marks(selected_course, self.students)
        else:
            print("Invalid course ID!")

    def show_student_marks(self):
        self.list_courses()
        course_id = input("Enter the course ID to view marks: ")
        selected_course = next((course for course in self.courses if course.course_id == course_id), None)
        if selected_course:
            self.marks.show_marks(selected_course, self.students)
        else:
            print("Invalid course ID!")


# Main program
if __name__ == "__main__":
    sm = StudentManagement()

    while True:
        print("\nOptions:")
        print("1. List students")
        print("2. List courses")
        print("3. Input marks for a course")
        print("4. Show student marks for a course")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            sm.list_students()
        elif choice == "2":
            sm.list_courses()
        elif choice == "3":
            sm.input_marks()
        elif choice == "4":
            sm.show_student_marks()
        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")
