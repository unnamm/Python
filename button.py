import tkinter


class Button:
    __button = 0

    def make(self, window, cmd):
        self.__button = tkinter.Button(
            window,
            text="run",
            overrelief="solid",
            command=cmd,
            repeatdelay=200,
            repeatinterval=100,
        )
        self.__button.pack()
