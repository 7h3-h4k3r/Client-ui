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
        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_BLUE, -1)   # selected
        curses.init_pair(2, curses.COLOR_CYAN,curses.COLOR_WHITE) 
        self.sqfeet = self.setSqt()
        self._create_windows()

    def selected_name(self):
        return self.Menu[self.selected]
    
    def setSqt(self):
        return (Grid.gety(self.h),Grid.getx(self.w))
    
    def setBox(self,state=False):
        if state:
            self.win.attron(curses.color_pair(1))
            self.win.box()
            self.win.attroff(curses.color_pair(1))
        else:
            self.win.box()
        self.win.refresh()
        
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
        
    def side_bar_content(self):
        self.win.erase()
        self.win.box()

        h, w = self.win.getmaxyx()

        for i in range(h - 2):
            menu_index = self.offset + i

            if menu_index >= len(self.Menu):
                break

            y = i + 1
            item = self.Menu[menu_index]

            if menu_index == self.selected:
                self.win.attron(curses.color_pair(2))
                self.win.addstr(y, 1, " " * (w - 2))
                self.win.addstr(y, 2, item[:w-4])
                self.win.attroff(curses.color_pair(2))
            else:
                self.win.addstr(y, 2, item[:w-4])
    
    def side_bar(self):
        self.side_bar_content()
        return self.win
    
    def Up(self):
        if self.selected >0:
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
       

            
