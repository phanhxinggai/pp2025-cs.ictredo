import math
import numpy as np
import _curses

class Student:
    def __init__(self, student_id, name, dob):
        self.student_id = student_id
        self.name = name
        self.dob = dob
        self.gpa = 0  # GPA will be calculated later

    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, DoB: {self.dob}, GPA: {self.gpa:.2f}"


class Course:
    def __init__(self, course_id, course_name, credits):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits

    def __str__(self):
        return f"ID: {self.course_id}, Name: {self.course_name}, Credits: {self.credits}"


class Marks:
    def __init__(self):
        self.marks = {}

    def input_marks(self, course, students):
        print(f"Enter marks for course: {course.course_name} (ID: {course.course_id})")
        self.marks[course.course_id] = {}
        for student in students:
            mark = float(input(f"Enter mark for {student.name} (ID: {student.student_id}): "))
            rounded_mark = math.floor(mark * 10) / 10  # Round down to 1 decimal place
            self.marks[course.course_id][student.student_id] = rounded_mark

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
            credits = int(input("Enter course credits: "))
            self.courses.append(Course(course_id, course_name, credits))

    def list_students(self, stdscr):
        stdscr.clear()
        stdscr.addstr("List of students:\n")
        for student in self.students:
            stdscr.addstr(str(student) + "\n")
        stdscr.addstr("\nPress any key to return to the menu.")
        stdscr.getch()

    def list_courses(self, stdscr):
        stdscr.clear()
        stdscr.addstr("List of courses:\n")
        for course in self.courses:
            stdscr.addstr(str(course) + "\n")
        stdscr.addstr("\nPress any key to return to the menu.")
        stdscr.getch()

    def input_marks(self):
        self.list_courses()
        course_id = input("Enter the course ID to input marks: ")
        selected_course = next((course for course in self.courses if course.course_id == course_id), None)
        if selected_course:
            self.marks.input_marks(selected_course, self.students)
        else:
            print("Invalid course ID!")

    def show_student_marks(self, stdscr):
        stdscr.clear()
        self.list_courses(stdscr)
        course_id = input("Enter the course ID to view marks: ")
        selected_course = next((course for course in self.courses if course.course_id == course_id), None)
        if selected_course:
            self.marks.show_marks(selected_course, self.students)
        else:
            stdscr.addstr("Invalid course ID!\n")

    def calculate_gpa(self):
        for student in self.students:
            total_weighted_score = 0
            total_credits = 0
            for course in self.courses:
                course_marks = self.marks.marks.get(course.course_id, {}).get(student.student_id, 0)
                total_weighted_score += course_marks * course.credits
                total_credits += course.credits
            student.gpa = total_weighted_score / total_credits if total_credits > 0 else 0

    def sort_students_by_gpa(self):
        self.students.sort(key=lambda s: s.gpa, reverse=True)

    def leaderboard(self, stdscr):
        stdscr.clear()
        stdscr.addstr("Leaderboard:\n")
        for idx, student in enumerate(sorted(self.students, key=lambda s: s.gpa, reverse=True), start=1):
            stdscr.addstr(f"{idx}. {student.name} (GPA: {student.gpa:.2f})\n")
        stdscr.addstr("\nPress any key to return to the menu.")
        stdscr.getch()

    def performance_groups(self, stdscr):
        stdscr.clear()
        groups = {"Top Performers": [], "Average": [], "Needs Improvement": []}
        for student in self.students:
            if student.gpa >= 3.5:
                groups["Top Performers"].append(student)
            elif 2.0 <= student.gpa < 3.5:
                groups["Average"].append(student)
            else:
                groups["Needs Improvement"].append(student)

        for group, members in groups.items():
            stdscr.addstr(f"\n{group}:\n")
            for member in members:
                stdscr.addstr(f"- {member.name} (GPA: {member.gpa:.2f})\n")

        stdscr.addstr("\nPress any key to return to the menu.")
        stdscr.getch()

    def decorated_ui(self):
        def curses_app(stdscr):
            while True:
                stdscr.clear()
                stdscr.addstr("Options:\n")
                stdscr.addstr("1. List students\n")
                stdscr.addstr("2. List courses\n")
                stdscr.addstr("3. Input marks for a course\n")
                stdscr.addstr("4. Show student marks for a course\n")
                stdscr.addstr("5. Calculate and display GPA\n")
                stdscr.addstr("6. Sort students by GPA\n")
                stdscr.addstr("7. Show leaderboard\n")
                stdscr.addstr("8. Group students by performance\n")
                stdscr.addstr("9. Exit\n")
                stdscr.addstr("Select an option: ")
                choice = stdscr.getstr().decode("utf-8")

                if choice == "1":
                    self.list_students(stdscr)
                elif choice == "2":
                    self.list_courses(stdscr)
                elif choice == "3":
                    self.input_marks()
                elif choice == "4":
                    self.show_student_marks(stdscr)
                elif choice == "5":
                    self.calculate_gpa()
                    stdscr.addstr("GPA calculated for all students.\nPress any key to return to the menu.")
                    stdscr.getch()
                elif choice == "6":
                    self.sort_students_by_gpa()
                    stdscr.addstr("Students sorted by GPA!\nPress any key to return to the menu.")
                    stdscr.getch()
                elif choice == "7":
                    self.leaderboard(stdscr)
                elif choice == "8":
                    self.performance_groups(stdscr)
                elif choice == "9":
                    break
                else:
                    stdscr.addstr("Invalid option! Press any key to try again.")
                    stdscr.getch()

        curses.wrapper(curses_app)

# Main program
if __name__ == "__main__":
    sm = StudentManagement()
    sm.input_students()
    sm.input_courses()
    sm.decorated_ui()
