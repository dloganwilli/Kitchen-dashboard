import tkinter as tk

class Timer:
    def __init__(self, parent, name="New Timer"):
        self.parent = parent
        self.running = False
        self.time_left = 0

        self.frame = tk.Frame(parent, bg="black")
        self.frame.pack(pady=10)

        self.name_label = tk.Label(self.frame, text=name, font=('Helvetica', 18), fg="white", bg="black")
        self.name_label.grid(row=0, column=0, columnspan=3, pady=5)

        self.time_label = tk.Label(self.frame, text="00:00", font=('Helvetica', 36), fg="white", bg="black")
        self.time_label.grid(row=1, column=0, columnspan=3)

        # Time adjustment buttons
        tk.Button(self.frame, text="+1 min", command=self.add_minute).grid(row=2, column=0)
        tk.Button(self.frame, text="-1 min", command=self.remove_minute).grid(row=2, column=1)
        tk.Button(self.frame, text="Reset", command=self.reset_timer).grid(row=2, column=2)

        # Control buttons
        tk.Button(self.frame, text="Start", command=self.start_timer).grid(row=3, column=0)
        tk.Button(self.frame, text="Pause", command=self.pause_timer).grid(row=3, column=1)
        tk.Button(self.frame, text="Delete", command=self.delete_timer).grid(row=3, column=2)

    def update_display(self):
        mins = self.time_left // 60
        secs = self.time_left % 60
        self.time_label.config(text=f"{mins:02}:{secs:02}")

    def tick(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.update_display()
            self.parent.after(1000, self.tick)
        elif self.time_left == 0 and self.running:
            self.running = False
            self.time_label.config(text="Time's up!")

    def add_minute(self):
        self.time_left += 60
        self.update_display()

    def remove_minute(self):
        if self.time_left >= 60:
            self.time_left -= 60
        else:
            self.time_left = 0
        self.update_display()

    def start_timer(self):
        if not self.running:
            self.running = True
            self.tick()

    def pause_timer(self):
        self.running = False

    def reset_timer(self):
        self.time_left = 0
        self.update_display()
        self.running = False

    def delete_timer(self):
        self.frame.destroy()


class TimerWidget:
    def __init__(self, parent):
        self.parent = parent
        self.timer_container = tk.Frame(parent, bg="black")
        self.timer_container.pack()

        self.add_button = tk.Button(parent, text="Add Timer", command=self.add_timer, font=('Helvetica', 14))
        self.add_button.pack(pady=10)

    def add_timer(self):
        Timer(self.timer_container, name="Timer")
