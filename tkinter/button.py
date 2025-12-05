import tkinter


class Button:
    def make(self, window, click):
        self.__button = tkinter.Button(
            window,
            text="run",
            overrelief="solid",
            command=click,
            repeatdelay=200,
            repeatinterval=100,
        )
        self.__button.pack(side='top', anchor='w', padx=10, pady=10)
