import curses
from libs.grid import Grid
# from ui import session

class MainPanel:


    def __init__(self,h,w,whois=''):
        self.win = None 
        self.whois = whois
        self.h = h 
        self.input_buffer = ''
        self.w = w 
        self.scroll_offset = 0
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
        h , w = self.win.getmaxyx()
        message = 'MESSAGE\'s'
        x = (w - len(message)) // 2
        # self.win.addstr(1, 1, self.whois[:self.w - 4])
        self.win.addstr(1, x, message)
        self.win.addstr(h- 2, 1, "> " + self.input_buffer)
    def redraw_content(self):
        self.win.erase()
        self.win.box()

        h, w = self.win.getmaxyx()

        message = "MESSAGE's"
        x = (w - len(message)) // 2
        self.win.addstr(1, x, message)

        prompt = "> "
        max_input_width = w - len(prompt) - 3

        if len(self.input_buffer) > max_input_width:
            visible_input = self.input_buffer[-max_input_width:]
        else:
            visible_input = self.input_buffer

        self.win.move(h - 2, 0)
        self.win.clrtoeol()
        self.win.addstr(h - 2, 1, prompt + visible_input)
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
        self.redraw_content()
       
        curses.doupdate()
        return self.win
    def send(self,session):
        session.append('Me:'+self.input_buffer)
        self.input_buffer = ''
    def pop(self):
        self.input_buffer = self.input_buffer[:-1]
    def push(self,key):
        self.input_buffer += chr(key)
    def Up(self):
        self.win.addstr(1,2,'Up is working Well')
    
    def Down(self):
        self.win.addstr(1,2,'Down is working Well')
        