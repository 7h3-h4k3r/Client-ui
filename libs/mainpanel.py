import curses
from libs.grid import Grid

class MainPanel:


    def __init__(self,h,w,whois='Hello Welcome To  homePage'):
        self.win = None 
        self.whois = whois
        self.h = h 
        self.w = w 
        self._create_mainwin()


    def _create_mainwin(self):
        self.win =  curses.newwin(
           Grid.gety(self.h,1),
           Grid.getx(self.w,1),
           Grid.gety(self.h),
           Grid.getx(self.w)
        ) 
        self.win.erase()
        self.win.box()
    def redraw_content(self):
        self.win.addstr(1, 1, self.whois[:self.w - 4])
        self.win.addstr(2, 1, 'Hello this From the chat server'[:self.w - 4])

    def setBox(self,state=False):
        if state:
            self.win.attron(curses.color_pair(1))
            self.win.box()
            self.win.attroff(curses.color_pair(1))
        else:
            self.win.box()
        self.win.refresh()

    def resize(self, h, w):
        self.h = h
        self.w = w

        sideY = Grid.gety(h)
        sideX = Grid.getx(w)

        self.win.resize(
            Grid.gety(self.h, 1),
            Grid.getx(self.w, 1)
        )
        self.win.mvwin(sideY, sideX)
        self.win.erase()
        self.win.box()
        self.redraw_content()

    def getmain(self):
        self.win.addstr(1,1,self.whois)
        self.win.addstr(2,1,'Hello this From the chat server')
        return self.win
        