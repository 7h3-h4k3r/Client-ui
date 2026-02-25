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

    def getmain(self):
        self.win.addstr(1,1,self.whois)
        return self.win
        