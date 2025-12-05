import tkinter


class Label:
    def make(self, window, text):
        self.__label = tkinter.Label(window, textvariable=text, relief="solid")
        self.__label.pack()

    def update(self, str):
        self.__label.config(text=str)
