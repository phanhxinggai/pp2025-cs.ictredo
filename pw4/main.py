import curses
from input import get_input
from output import show_message
from domain.student import Student
from domain.course import Course
from domain.mark import Marks

class StudentManagement:
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = Marks()

    def input_students(self):
        num_students = int(get_input("Enter the number of students: "))
        for _ in range(num_students):
            student_id = get_input("Enter student ID: ")
            name = get_input("Enter student name: ")
            dob = get_input("Enter student DoB (YYYY-MM-DD): ")
            self.students.append(Student(student_id, name, dob))

    def input_courses(self):
        num_courses = int(get_input("Enter the number of courses: "))
        for _ in range(num_courses):
            course_id = get_input("Enter course ID: ")
            course_name = get_input("Enter course name: ")
            credits = int(get_input("Enter course credits: "))
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
        course_id = get_input("Enter the course ID to input marks: ")
        selected_course = next((course for course in self.courses if course.course_id == course_id), None)
        if selected_course:
            self.marks.input_marks(selected_course, self.students)
        else:
            print("Invalid course ID!")

    def show_student_marks(self, stdscr):
        stdscr.clear()
        self.list_courses(stdscr)
        course_id = get_input("Enter the course ID to view marks: ")
        selected_course = next((course for course in self.courses if course.course_id == course_id), None)
        if selected_course:
            self.marks.show_marks(selected_course, self.students)
        else:
            show_message(stdscr, "Invalid course ID!")

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
                    show_message(stdscr, "GPA calculated for all students.")
                elif choice == "6":
                    self.sort_students_by_gpa()
                    show_message(stdscr, "Students sorted by GPA!")
                elif choice == "7":
                    self.leaderboard(stdscr)
                elif choice == "8":
                    self.performance_groups(stdscr)
                elif choice == "9":
                    break
                else:
                    show_message(stdscr, "Invalid option! Press any key to try again.")

        curses.wrapper(curses_app)

# Main program
if __name__ == "__main__":
    sm = StudentManagement()
    sm.input_students()
    sm.input_courses()
    sm.decorated_ui()
