import os
import pickle
import zipfile
import curses
from domain.student import Student
from domain.course import Course
from domain.mark import Marks

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
            self.load_data_from_pickle()

    def compress_and_save_data(self):
        self.save_data_to_pickle()
        with zipfile.ZipFile(self.data_file, "w") as zip_ref:
            zip_ref.write("students.pkl")
        print(f"Data compressed into {self.data_file}.")

    def save_data_to_pickle(self):
        data = {
            "students": self.students,
            "courses": self.courses,
            "marks": self.marks.marks
        }
        with open("students.pkl", "wb") as f:
            pickle.dump(data, f)

    def load_data_from_pickle(self):
        try:
            with open("students.pkl", "rb") as f:
                data = pickle.load(f)
            self.students = data["students"]
            self.courses = data["courses"]
            self.marks.marks = data["marks"]
            print("Data loaded successfully from pickle.")
        except FileNotFoundError:
            print("No pickle file found. Starting with empty data.")

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

    def input_marks(self):
        course_id = input("Enter the course ID to input marks: ")
        selected_course = next((course for course in self.courses if course.course_id == course_id), None)
        if selected_course:
            self.marks.input_marks(selected_course, self.students)
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
                    self.list_students(stdscr)
                elif choice == "2":
                    self.list_courses(stdscr)
                elif choice == "3":
                    self.input_marks()
                elif choice == "4":
                    self.compress_and_save_data()
                    break
                else:
                    stdscr.addstr("Invalid option! Press any key to try again.")
                    stdscr.getch()

        curses.wrapper(curses_app)

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

if __name__ == "__main__":
    sm = StudentManagement()
    sm.decorated_ui()
