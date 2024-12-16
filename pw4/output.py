import curses

def show_message(stdscr, message):
    stdscr.clear()
    stdscr.addstr(message)
    stdscr.getch()
