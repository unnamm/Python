import tkinter

class Window:
    __window = 0

    def make(self):
        self.__window = tkinter.Tk()
        self.__window.title("window name")
        self.__window.geometry("1280x720")
        return self.__window

    def loop(self):
        self.__window.mainloop()