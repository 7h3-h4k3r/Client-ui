import curses
from curses import panel
from libs.grid import Grid
from libs.sidebar import Side
import time
from libs.mainpanel import MainPanel

session = {
    'Home' : [],
    'Group' : [],
}

class UI:
#'Alice','Ben','Lexa','Robi','Konan','Panzy','aureGen',
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.active = 1
        curses.curs_set(0)
        self.stdscr.keypad(True)
        self.h, self.w = self.stdscr.getmaxyx()
        self.side_bar = Side(self.h,self.w,['Home','Group'])
        self.main_bar = MainPanel(self.h,self.w)
        self.loop()
    
    def brand(self):
        top = self.h * 5 // 100
        right = self.w * 5 // 100
        self.stdscr.addstr(top,right,'Hi Welcome to The Chat')



    def footer(self):
        self.stdscr.addstr(
            self.h - 1,
            Grid.getx(self.w) + 1,
            'F1:Help F2:Del F3:Hist F4:Quit'
        )
   
    def updatewindow(self):
        try:
            curses.update_lines_cols()
            self.h, self.w = self.stdscr.getmaxyx()
            self.stdscr.erase()
            self.sideY , self.sideX  = Grid.getSqt(self.h,self.w)
            self.side_bar.resize(self.h, self.w)
            self.main_bar.resize(self.h,self.w)
        except Exception as e:
            raise(str(e))
        
    def _draw(self):
        try:
            self.stdscr.noutrefresh()

            self.side_bar.side_bar().noutrefresh()
            self.main_bar.getmain().noutrefresh()
            self.brand()
            self.footer()
            curses.doupdate()
        except:
            raise(' window size is too short')
    def loop(self):
        active = 1
        self._draw()
       
        self.side_bar.setBox(True)
        
        while True:
            
            
            key = self.stdscr.getch()

            if key == curses.KEY_RESIZE:
                try:
                    self.updatewindow()
                    self._draw()
                except Exception as e:
                    pass
            elif key == 9:
                if active:
                    self.main_bar.setBox()
                    self.side_bar.setBox(True)
                    active = 0
                else:
                    self.side_bar.setBox()
                    self.main_bar.setBox(True)
                    active  = 1
            elif key == curses.KEY_DOWN:
                if active:
                    self.side_bar.Down()
                else:
                    self.main_bar.Down()
                self._draw()
            elif key == curses.KEY_UP:
                if active:
                    self.side_bar.Up()
                else:
                    self.main_bar.Up()
                self._draw()


            elif key == ord('q'):
                break


def main(stdscr):
    UI(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)