import curses

def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    # Create two windows
    win1 = curses.newwin(height//2, width, 0, 0)
    win2 = curses.newwin(height//2, width, height//2, 0)

    win1.box()
    win2.box()

    input1 = ""
    input2 = ""

    active = 1  # 1 = win1, 2 = win2

    while True:
        # Highlight active window
        if active == 1:
            win1.attron(curses.A_BOLD)
            win2.attroff(curses.A_BOLD)
        else:
            win2.attron(curses.A_BOLD)
            win1.attroff(curses.A_BOLD)

        win1.clear()
        win2.clear()
        win1.box()
        win2.box()

        win1.addstr(1, 2, "Window 1: " + input1)
        win2.addstr(1, 2, "Window 2: " + input2)

        win1.refresh()
        win2.refresh()

        key = stdscr.getch()

        if key == 9:  # TAB to switch window
            active = 2 if active == 1 else 1

        elif key in (27,):  # ESC to exit
            break

        elif key in (curses.KEY_BACKSPACE, 127):
            if active == 1 and len(input1) > 0:
                input1 = input1[:-1]
            elif active == 2 and len(input2) > 0:
                input2 = input2[:-1]

        elif 32 <= key <= 126:  # printable chars
            if active == 1:
                input1 += chr(key)
            else:
                input2 += chr(key)

curses.wrapper(main)