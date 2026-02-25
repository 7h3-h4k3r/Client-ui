import curses
from curses import panel
from libs.grid import Grid
from libs.sidebar import Side
import time
from libs.mainpanel import MainPanel

clients = {
    'Home' : [],
    'Group' : [],
}

class UI:
#'Alice','Ben','Lexa','Robi','Konan','Panzy','aureGen',
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.keypad(True)
        self.h, self.w = self.stdscr.getmaxyx()
        self.side_bar = Side(self.h,self.w,['Home','Group'])
        self.getPanel()
        self.loop()
    
   
    def setScreen(self):
        top = self.h * 5 // 100
        right = self.w * 5 // 100
        self.stdscr.addstr(top,right,'Hi Welcome to The Chat')

    def getPanel(self):
        j = 0
        for name in clients:
            if j == 0:
                main = MainPanel(self.h, self.w, 'Welcome to The Main Chat')
            else:
                main = MainPanel(self.h, self.w, 'Welcome To The Group')

            win = main.getmain()
            pnl = panel.new_panel(win)

            clients[name] = [main, pnl]
            j += 1 
    
    

    def _draw(self):
        self.stdscr.noutrefresh()

        self.side_bar.side_bar().noutrefresh()

        for name in clients:
            clients[name][0].getmain().noutrefresh()

        self.setScreen()
        self.stdscr.addstr(
            self.h - 1,
            Grid.getx(self.w) + 1,
            'F1:Help F2:Del F3:Hist F4:Quit'
        )

        panel.update_panels()
        curses.doupdate()

    def loop(self):
        
        self._draw()
        while True:
             
            key = self.stdscr.getch()

            if key == curses.KEY_RESIZE:
                curses.update_lines_cols()
                self.h, self.w = self.stdscr.getmaxyx()

                self.sideY , self.sideX  = Grid.getSqt(self.h,self.w)
   
                self.side_bar.resize(self.h, self.w)
                for i in clients:
                    clients[i][0].resize(self.h,self.w)
                # self.main_bar.resize(self.h, self.w)
                self.stdscr.clear()
                self._draw()
            elif key in (curses.KEY_DOWN, curses.KEY_UP):

                if key == curses.KEY_DOWN:
                    self.side_bar.Down()
                else:
                    self.side_bar.Up()

                self.side_bar.resize(self.h, self.w)

                name = self.side_bar.selected_name()

                # bring selected panel to top
                clients[name][1].top()

                panel.update_panels()
                curses.doupdate()
            elif key == ord('q'):
                break


def main(stdscr):
    UI(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)