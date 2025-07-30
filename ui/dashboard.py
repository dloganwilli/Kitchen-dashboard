# ✅ Final `dashboard.py` with Idle Screensaver Overlay

import tkinter as tk
from tkinter import ttk
import time
import threading
from ui.clock import ClockWidget
from ui.timers import TimerWidget
from ui.recipes import RecipeWidget
from ui.shopping_list import ShoppingListWidget
from ui.styles import COLORS

class KitchenDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Kitchen Dashboard")
        self.root.geometry("1024x600")
        self.root.configure(bg=COLORS["bg"])

        self.idle_timeout = 60  # seconds until overlay
        self.last_interaction_time = time.time()
        self.idle_overlay = None

        self.root.bind_all("<Any-KeyPress>", self.reset_idle_timer)
        self.root.bind_all("<Any-Button>", self.reset_idle_timer)
        self.start_idle_check()

        # Escape key exits fullscreen
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=COLORS["bg"])
        style.configure('TNotebook.Tab', background=COLORS["highlight"], foreground=COLORS["fg"], padding=10)
        style.map('TNotebook.Tab', background=[('selected', COLORS["accent"])])

        # Tab setup
        self.tab_control = ttk.Notebook(self.root)

        self.tab_timers = tk.Frame(self.tab_control, bg=COLORS["bg"])
        self.tab_recipes = tk.Frame(self.tab_control, bg=COLORS["bg"])
        self.tab_shopping = tk.Frame(self.tab_control, bg=COLORS["bg"])

        self.tab_control.add(self.tab_timers, text="🕒 Timers")
        self.tab_control.add(self.tab_recipes, text="📖 Recipes")
        self.tab_control.add(self.tab_shopping, text="🛒 Shopping List")

        self.tab_control.pack(expand=1, fill="both")

        ClockWidget(self.tab_timers)
        TimerWidget(self.tab_timers)
        RecipeWidget(self.tab_recipes)
        ShoppingListWidget(self.tab_shopping)

    def reset_idle_timer(self, event=None):
        self.last_interaction_time = time.time()
        if self.idle_overlay:
            self.idle_overlay.destroy()
            self.idle_overlay = None

    def start_idle_check(self):
        def monitor():
            while True:
                if time.time() - self.last_interaction_time > self.idle_timeout and not self.idle_overlay:
                    self.show_idle_overlay()
                time.sleep(1)
        threading.Thread(target=monitor, daemon=True).start()

    def show_idle_overlay(self):
        self.idle_overlay = tk.Toplevel(self.root)
        self.idle_overlay.attributes('-fullscreen', True)
        self.idle_overlay.configure(bg="black")
        tk.Label(
            self.idle_overlay,
            text="",
            font=("Helvetica", 48),
            fg="teal",
            bg="black"
        ).pack(expand=True)
