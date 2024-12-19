import curses

def list_students(stdscr, students):
    stdscr.clear()
    stdscr.addstr("List of students:\n")
    for student in students:
        stdscr.addstr(str(student) + "\n")
    stdscr.addstr("\nPress any key to return to the menu.")
    stdscr.getch()

def list_courses(stdscr, courses):
    stdscr.clear()
    stdscr.addstr("List of courses:\n")
    for course in courses:
        stdscr.addstr(str(course) + "\n")
    stdscr.addstr("\nPress any key to return to the menu.")
    stdscr.getch()
