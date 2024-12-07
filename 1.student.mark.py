# 1.student.mark.py

# Functions to input data
def input_students():
    num_students = int(input("Enter the number of students: "))
    students = []
    for _ in range(num_students):
        student_id = input("Enter student ID: ")
        name = input("Enter student name: ")
        dob = input("Enter student DoB (YYYY-MM-DD): ")
        students.append((student_id, name, dob))
    return students

def input_courses():
    num_courses = int(input("Enter the number of courses: "))
    courses = []
    for _ in range(num_courses):
        course_id = input("Enter course ID: ")
        course_name = input("Enter course name: ")
        courses.append((course_id, course_name))
    return courses

def input_marks(students, courses):
    marks = {}
    print("Available courses:")
    for idx, course in enumerate(courses, start=1):
        print(f"{idx}. {course[1]} (ID: {course[0]})")
    selected_course = input("Enter the course ID to input marks: ")
    
    if selected_course not in [course[0] for course in courses]:
        print("Invalid course ID!")
        return marks
    
    marks[selected_course] = {}
    for student in students:
        mark = float(input(f"Enter mark for {student[1]} (ID: {student[0]}): "))
        marks[selected_course][student[0]] = mark
    return marks

# Listing functions
def list_courses(courses):
    print("List of courses:")
    for course_id, course_name in courses:
        print(f"ID: {course_id}, Name: {course_name}")

def list_students(students):
    print("List of students:")
    for student_id, name, dob in students:
        print(f"ID: {student_id}, Name: {name}, DoB: {dob}")

def show_student_marks(marks, students, courses):
    print("Available courses:")
    for idx, course in enumerate(courses, start=1):
        print(f"{idx}. {course[1]} (ID: {course[0]})")
    selected_course = input("Enter the course ID to view marks: ")

    if selected_course not in marks:
        print("No marks available for this course!")
        return

    print(f"Marks for course ID {selected_course}:")
    for student in students:
        student_id = student[0]
        mark = marks[selected_course].get(student_id, "N/A")
        print(f"{student[1]} (ID: {student_id}): {mark}")

# Main program
if __name__ == "__main__":
    students = input_students()
    courses = input_courses()
    marks = {}

    while True:
        print("\nOptions:")
        print("1. List students")
        print("2. List courses")
        print("3. Input marks for a course")
        print("4. Show student marks for a course")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            list_students(students)
        elif choice == "2":
            list_courses(courses)
        elif choice == "3":
            course_marks = input_marks(students, courses)
            if course_marks:
                marks.update(course_marks)
        elif choice == "4":
            show_student_marks(marks, students, courses)
        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")
