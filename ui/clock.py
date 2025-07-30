# ui/clock.py
import tkinter as tk
import time
from ui.styles import COLORS, FONTS

class ClockWidget:
    def __init__(self, parent):
        self.label = tk.Label(
            parent,
            font=('Helvetica', 48),
            fg=COLORS["fg"],
            bg=COLORS["bg"]
        )
        self.label.pack(pady=20)
        self.update_clock()

    def update_clock(self):
        current_time = time.strftime('%I:%M:%S %p')
        self.label.config(text=current_time)
        self.label.after(1000, self.update_clock)
