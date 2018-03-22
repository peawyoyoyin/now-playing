import tkinter
import win32gui
import win32con
import re

class App():
    def __init__(self):
        self.root = tkinter.Tk('test')
        self.root.call('wm', 'attributes', '.', '-topmost', '1')
        self.root.overrideredirect(True)
        self.init_frame()
        self.init_label()
        self.init_close_label()
        self.root.geometry('+0+150')
        tkinter.mainloop()
    
    def init_frame(self):
        self.frame = tkinter.Frame(self.root)
        self.frame.pack()

    def init_label(self):
        if self.frame is None:
            self.init_frame()
        self.label = tkinter.Label(self.frame)
        self.label.config(text='select window to track')
        self.label.bind('<Button-1>', self.find_window)
        self.label.pack(side=tkinter.LEFT)
    
    def init_close_label(self):
        if self.frame is None:
            self.init_frame()
        self.close_label = tkinter.Label(self.frame)
        self.close_label.config(text='x')
        self.close_label.bind('<Button-1>', lambda e: self.root.destroy())
        self.close_label.pack(side=tkinter.RIGHT)
    
    def update_label(self):
        wintext = win32gui.GetWindowText(self.window)

        # translate chrome text into prettier format
        wintext = wintext.rsplit('-', 2)[0]
        match = re.match(r'^\(\d*\)(.*)', wintext)
        if match is not None:
            wintext = match.groups()[0]

        self.label.config(text=wintext)
        self.root.lift()
        self.root.after(5000, self.update_label)

    def find_window(self, event):
        top_window = win32gui.GetActiveWindow()
        next_window = win32gui.GetWindow(top_window, 2)
        while(True):
            if(win32gui.IsWindowVisible(next_window) and win32gui.IsWindow(next_window) and win32gui.IsWindow(next_window)):
                if(win32gui.GetWindowText(next_window)):
                    break
            next_window = win32gui.GetWindow(next_window, 2)
        self.window = next_window
        self.label.unbind('<Button-1>')
        self.update_label()
        

if __name__ == '__main__':
    App()
