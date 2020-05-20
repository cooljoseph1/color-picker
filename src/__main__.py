#!/usr/bin/env python3

import tkinter as tk

from .application import Application
from .genetic import ConvergeAlgorithm

colors = ConvergeAlgorithm(255, 255, 255)

root = tk.Tk()
app = Application(root)
app.set_algorithm(colors)
root.mainloop()

window = Window()
while True:
    window.set_colors(colors[:3])
    colors.update_choice(window.get_choice())
    colors.new_generation()
