import tkinter

class AppControlPanel(tkinter.Frame):
    def __init__(self, master):
        super(AppControlPanel, self).__init__(master)

        self.minimize_label = self.init_minimize_label()
        self.minimize_label.pack(side=tkinter.LEFT)

        self.close_label = self.init_close_label()
        self.close_label.pack(side=tkinter.RIGHT)
    
    def init_close_label(self):
        close_label = tkinter.Label(self)
        close_label.config(text='x')
        return close_label

    def init_minimize_label(self):
        minimize_label = tkinter.Label(self)
        minimize_label.config(text='-')
        return minimize_label

    def set_on_close(self, on_close):
        self.close_label.bind('<Button-1>', on_close)

    def set_on_minimize(self, on_minimize):
        self.minimize_label.bind('<Button-1>', on_minimize)
