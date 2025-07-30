import tkinter as tk

root = tk.Tk()
root.title("Test Window")
root.geometry("600x400")
tk.Label(root, text="If you see this, your GUI is working!", font=("Arial", 16)).pack(pady=20)
root.mainloop()