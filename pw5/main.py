import os
import json
import zipfile
from domain.student import Student
from domain.course import Course
from domain.mark import Marks
from input import write_students_to_file, write_courses_to_file, write_marks_to_file
from output import list_students, list_courses
import curses

class StudentManagement:
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = Marks()
        self.data_file = "students.dat"
        self.decompress_and_load_data()

    def decompress_and_load_data(self):
        if os.path.exists(self.data_file):
            with zipfile.ZipFile(self.data_file, "r") as zip_ref:
                zip_ref.extractall()
            self.load_data_from_files()

    def compress_data(self):
        with zipfile.ZipFile(self.data_file, "w") as zip_ref:
            zip_ref.write("students.txt")
            zip_ref.write("courses.txt")
            zip_ref.write("marks.txt")
        print(f"Data compressed into {self.data_file}.")

    def load_data_from_files(self):
        try:
            with open("students.txt", "r") as f:
                self.students = [Student(**data) for data in json.load(f)]
            with open("courses.txt", "r") as f:
                self.courses = [Course(**data) for data in json.load(f)]
            with open("marks.txt", "r") as f:
                self.marks.marks = json.load(f)
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("Data files not found. Starting with empty data.")

    def input_students(self):
        num_students = int(input("Enter the number of students: "))
        for _ in range(num_students):
            student_id = input("Enter student ID: ")
            name = input("Enter student name: ")
            dob = input("Enter student DoB (YYYY-MM-DD): ")
            self.students.append(Student(student_id, name, dob))
        write_students_to_file(self.students)

    def input_courses(self):
        num_courses = int(input("Enter the number of courses: "))
        for _ in range(num_courses):
            course_id = input("Enter course ID: ")
            course_name = input("Enter course name: ")
            credits = int(input("Enter course credits: "))
            self.courses.append(Course(course_id, course_name, credits))
        write_courses_to_file(self.courses)

    def input_marks(self):
        course_id = input("Enter the course ID to input marks: ")
        selected_course = next((course for course in self.courses if course.course_id == course_id), None)
        if selected_course:
            self.marks.input_marks(selected_course, self.students)
            write_marks_to_file(self.marks)
        else:
            print("Invalid course ID!")

    def decorated_ui(self):
        def curses_app(stdscr):
            while True:
                stdscr.clear()
                stdscr.addstr("Options:\n")
                stdscr.addstr("1. List students\n")
                stdscr.addstr("2. List courses\n")
                stdscr.addstr("3. Input marks\n")
                stdscr.addstr("4. Exit\n")
                stdscr.addstr("Select an option: ")
                choice = stdscr.getstr().decode("utf-8")

                if choice == "1":
                    list_students(stdscr, self.students)
                elif choice == "2":
                    list_courses(stdscr, self.courses)
                elif choice == "3":
                    self.input_marks()
                elif choice == "4":
                    self.compress_data()
                    break
                else:
                    stdscr.addstr("Invalid option! Press any key to try again.")
                    stdscr.getch()

        curses.wrapper(curses_app)

if __name__ == "__main__":
    sm = StudentManagement()
    sm.decorated_ui()
