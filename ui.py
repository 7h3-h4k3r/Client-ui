import curses
from libs.grid import Grid
from libs.sidebar import Side
import time
class UI:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.keypad(True)
        self.h, self.w = self.stdscr.getmaxyx()
        self.side_bar = Side(self.h,Grid.gety(self.h),Grid.getx(self.w))
        self.loop()
    def _gety(self,y,ops=False):
        if ops:
            return y * 70 // 100 
        return y * 30 // 100
    def _getx(self,x,ops=False):
        if ops:
            return x  * 70 // 100
        return x * 30 // 100
    def setScreen(self):
        top = self.h * 5 // 100
        right = self.w * 5 // 100
        self.stdscr.addstr(top,right,'Hi Welcome to The Chat')

    def _create_windows(self,sideY,sideX):

        win = curses.newwin(
            self.h - sideY,
            sideX,
            sideY,
            0
        )
        return win
   


    def _resize_windows(self,win):
        curses.update_lines_cols()
        self.h, self.w = self.stdscr.getmaxyx()

        self.sideY = self._gety(self.h)
        self.sideX = self._getx(self.w)

        win.resize(self.h - self.sideY, self.sideX)
        win.mvwin(self.sideY, 0)
        self.stdscr.clearok(True)


    
        
    def _draw(self):

        win = self.side_bar.side_bar()
        self.stdscr.noutrefresh()
        win2 = curses.newwin(self._gety(self.h,1),self._getx(self.w,1),self._gety(self.h),self._getx(self.w))
        self.stdscr.erase()
        self.stdscr.noutrefresh()
        win2.erase()
        win2.box()
        win2.addstr(1, 1, "Menu Bar")
        win.noutrefresh()
        win2.noutrefresh()
        self.setScreen()
        self.stdscr.addstr(self.h-1,self._getx(self.w)+1,'F1:Help F2:Del F3:Hist F4:Quit')
        curses.doupdate()

        return (win,win2)

    def loop(self):
        
        
        side_bar ,main_bar = self._draw()
        while True:
             
            key = self.stdscr.getch()

            if key == curses.KEY_RESIZE:
                curses.update_lines_cols()
                self.h, self.w = self.stdscr.getmaxyx()

                self.sideY = self._gety(self.h)
                self.sideX = self._getx(self.w)

                self.side_bar.resize(self.h, self.w)

                # self.main_bar.resize(self.h - self.sideY, self.sideX)
                # self.main_bar.mvwin(self.sideY, self.sideX)

                self.stdscr.clear()
                self._draw()
            elif key == curses.KEY_DOWN:
                self.side_bar.Down()
                self.side_bar.resize(self.h,self.w)
                self._draw()
            
            elif key == curses.KEY_UP:
                self.side_bar.Up()
                self.side_bar.resize(self.h,self.w)
                self._draw()
            elif key == ord('q'):
                break


def main(stdscr):
    UI(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)