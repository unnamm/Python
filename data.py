import tkinter


class Data:
    value = 0

    def create(self, window):
        self.s = tkinter.StringVar(window)
        self.up()

    def up(self):
        self.value += 1
        self.s.set(self.value)

    def toString(self):
        return self.s
