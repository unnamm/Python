import label
import data
import window
import button

main = window.Window()
w = main.make()

d = data.Data()
l = label.Label()
b = button.Button()

d.create(w)
l.make(w, d.toString())
b.make(w, d.up)

main.loop()
