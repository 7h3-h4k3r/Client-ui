import curses
from libs.grid import Grid
class Side:

    def __init__(self,h,w,menu):
        self.Menu = menu 
        self.h = h
        self.w = w
        self.offset = 0 
        self.selected = 0 
        self.win = None
        self.sqfeet = self.setSqt()
        self._create_windows()

    def selected_name(self):
        return self.Menu[self.selected]
    def setSqt(self):
        return (Grid.gety(self.h),Grid.getx(self.w))
    def _create_windows(self):
        
        self.win = curses.newwin(
            self.h - self.sqfeet[0],
            self.sqfeet[-1],
            self.sqfeet[0],
            0
        )
        self.win.erase()
        self.win.box()
    
    def resize(self, h, w):
        sideY = Grid.gety(h)
        sideX = Grid.getx(w)

        self.win.resize(h - sideY, sideX)
        self.win.mvwin(sideY, 0)
        self.win.erase()
        self.win.box()
        
    
    
    def side_bar(self):
        h , w = self.win.getmaxyx()
        for i in range(h-2):
            menu_index = self.offset + i

            if menu_index >= len(self.Menu):
                break
            y = i + 1 
            item = self.Menu[menu_index]

            if menu_index == self.selected:
                self.win.attron(curses.A_REVERSE)
                self.win.addstr(y, 1, " " * (w - 2))
                self.win.addstr(y, 2, item[:w-4])
                self.win.attroff(curses.A_REVERSE)
            else:
                self.win.addstr(y, 2, item[:w-4])
        
        return self.win
    
    def Up(self):
        if self.selected > 0:
            self.selected -= 1
            if self.selected < self.offset:
                self.offset -= 1
    def Down(self):
        h, w = self.win.getmaxyx()
        visible_height = h - 2
        if self.selected < len(self.Menu) - 1:
            self.selected += 1
            if self.selected >= self.offset + visible_height:
                self.offset += 1
       

            
