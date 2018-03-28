import tkinter
import win32gui
import win32con
import re

UPDATE_INTERVAL = 5000

class AppControlPanel(tkinter.Frame):
    def __init__(self, master, on_close=None, on_minimize=None):
        super(AppControlPanel, self).__init__(master)

        self.minimize_label = self.init_minimize_label(on_minimize)
        self.minimize_label.pack(side=tkinter.LEFT)

        self.close_label = self.init_close_label(on_close)
        self.close_label.pack(side=tkinter.RIGHT)
    
    def init_close_label(self, on_close=None):
        close_label = tkinter.Label(self)
        close_label.config(text='x')
        if on_close is not None:
            close_label.bind('<Button-1>', on_close)
        return close_label

    def init_minimize_label(self, on_minimize=None):
        minimize_label = tkinter.Label(self)
        minimize_label.config(text='-')
        if on_minimize is not None:
            minimize_label,bind('<Button-1>', on_minimize)
        return minimize_label

    def set_on_close(self, on_close):
        self.close_label.bind('<Button-1>', on_close)

    def set_on_minimize(self, on_minimize):
        self.minimize_label.bind('<Button-1>', on_minimize)


class App():
    def __init__(self):
        self.root = tkinter.Tk('now playing')
        self.root.call('wm', 'attributes', '.', '-topmost', '1')
        self.root.overrideredirect(True)
        self.root.geometry('+0+0')

        self.frame = tkinter.Frame(self.root)
        self.frame.pack()

        self.label = self.init_label()
        self.label.pack(side=tkinter.LEFT)

        self.control_panel = AppControlPanel(self.frame, on_close=lambda e: self.root.destroy())
        self.control_panel.pack(side=tkinter.RIGHT)
        
        tkinter.mainloop()
    
    def init_label(self):
        label = tkinter.Label(self.frame)
        label.config(text='select window to track')
        label.bind('<Button-1>', self.find_window)
        label.bind('<B1-Motion>', self.on_drag)
        return label

    def on_drag(self, event):
        self.root.geometry('+0+{}'.format(event.y_root))
    
    def update_label(self):
        wintext = win32gui.GetWindowText(self.window)
        wintext = self.translate_window_text(wintext)

        self.label.config(text=wintext)
        self.root.lift()
        self.update_loop = self.root.after(UPDATE_INTERVAL, self.update_label)

    def translate_window_text(self, text):
        text = text.rsplit('-', 1)[0]
        match = re.match(r'^\(\d*\)(.*)', text)
        if match is not None:
            return match.groups()[0]
        return text

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
        self.label.bind('<Button-3>', self.untrack_window)
        self.update_label()

    def untrack_window(self, event):
        if self.window is not None:
            self.window = None
            self.root.after_cancel(self.update_loop)
            self.label.destroy()
            self.init_label()


if __name__ == '__main__':
    App()
