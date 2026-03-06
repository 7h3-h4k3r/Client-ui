import curses
from curses import panel
from libs.grid import Grid
import textwrap
from libs.sidebar import Side
import time
from threading import Thread, Event
from libs.mainpanel import MainPanel
import socket
redraw_event = Event()
session = {
    'Home' : [],
    'Group' : [],
}
class connServer:
    
    def __init__(self,host='0.0.0.0',port=5656):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = host 
        self.port = port
            
    def setConf(self):
        self.socket.connect((self.host,self.port))
        
    def getMsg(self):
        while True:
            try:
                data = self.socket.recv(1024).decode()
                if not data:
                    continue
                session['Group'].append(data)
                redraw_event.set()
            except:
                self.socket.close()
                break

    def reciver(self):
        self.setConf()
        t = Thread(target=self.getMsg,daemon=True)
        t.start()
        
    def send(self,data):
        self.socket.sendall(data.encode())
         
class UI:
    
            
        
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.active = 1
        self.scroll_offset= 0
        self.server = connServer()
        self.server.reciver()
        curses.curs_set(0)
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)
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
        
    
     
        
    def _draw(self,state=False):
        try:
            self.stdscr.noutrefresh()
            self.side_bar.side_bar().noutrefresh()
            win = self.main_bar.getmain()
            if state:
                self.main_bar.home()
            else:
                self.main_bar.visible_message(session['Group'])
            win.noutrefresh()
            self.brand()
            
            self.footer()
            curses.doupdate()
        except:
            raise(' window size is too short')
        
        
    def loop(self):
        active = 1
        self._draw(True)
        
        self.side_bar.setBox(True)
        # self.main_bar.redraw_content()
        while True:
            if active:
                self.main_bar.setBox()
                self.side_bar.setBox(True)
            else:
                self.side_bar.setBox()
                self.main_bar.setBox(True)

            if redraw_event.is_set():
                self._draw()
                redraw_event.clear()
            
            key = self.stdscr.getch()
            
            if key == curses.KEY_RESIZE:
                try:
                    self.updatewindow()
                    self._draw()
                except Exception as e:
                    pass
            elif key == 9:
                if active:
                    active = 0
                else:
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

            elif 32 <= key and key <= 126:
                if self.side_bar.selected_name() == 'Home':
                    continue
                self.main_bar.push(key=key)
                self._draw()

            elif key == curses.KEY_BACKSPACE:
                self.main_bar.pop()
                self._draw()
     
            elif key in (10,13):
                state=False
                if self.side_bar.selected_name() =='Home':
                    state=True 
                else:
                    msg = self.main_bar.getData()
                    self.server.send(msg)
                    session['Group'].append(msg)
                self._draw(state)
            elif key == curses.KEY_F4:
                break


        
def main(stdscr):
    UI(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)