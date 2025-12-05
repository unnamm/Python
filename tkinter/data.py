import tkinter


class Data:
    def create(self, window):
        self.s = tkinter.StringVar(window)
        self.value = 0
        self.s.set(self.value)

    def up(self):
        self.value += 1
        self.s.set(self.value)

    def toString(self):
        return self.s
