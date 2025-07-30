import tkinter as tk
from tkinter import simpledialog, messagebox
from ui.styles import COLORS, FONTS, WIDGET_STYLE

# Import Twilio configuration and module. Ensure you've installed 'twilio' via pip.
try:
    from twilio.rest import Client
    import twilio_config  # This file should contain your Twilio credentials.
except ImportError:
    Client = None  # If the module isn't installed, we warn later.

class ShoppingListWidget:
    def __init__(self, parent):
        self.parent = parent

        # Shopping list display
        self.listbox = tk.Listbox(
            parent,
            font=FONTS["body"],
            bg=COLORS["entry_bg"],
            fg=COLORS["fg"],
            selectbackground=COLORS["highlight"]
        )
        self.listbox.pack(padx=10, pady=10, fill="both", expand=True)

        # Button frame
        button_frame = tk.Frame(parent, bg=COLORS["bg"])
        button_frame.pack(pady=10)

        add_btn = tk.Button(button_frame, text="Add Item", command=self.add_item,
                            font=FONTS["button"], bg=COLORS["button"], fg=COLORS["fg"], **WIDGET_STYLE["button"])
        add_btn.grid(row=0, column=0, padx=5)

        remove_btn = tk.Button(button_frame, text="Remove Selected", command=self.remove_item,
                               font=FONTS["button"], bg=COLORS["button"], fg=COLORS["fg"], **WIDGET_STYLE["button"])
        remove_btn.grid(row=0, column=1, padx=5)

        clear_btn = tk.Button(button_frame, text="Clear All", command=self.clear_items,
                              font=FONTS["button"], bg=COLORS["button"], fg=COLORS["fg"], **WIDGET_STYLE["button"])
        clear_btn.grid(row=0, column=2, padx=5)

        send_btn = tk.Button(button_frame, text="Send to Phone", command=self.send_to_phone,
                             font=FONTS["button"], bg=COLORS["button"], fg=COLORS["fg"], **WIDGET_STYLE["button"])
        send_btn.grid(row=0, column=3, padx=5)

    def add_item(self):
        item = simpledialog.askstring("Add Item", "Enter item name:")
        if item:
            self.listbox.insert(tk.END, item)

    def remove_item(self):
        selected = self.listbox.curselection()
        for index in reversed(selected):
            self.listbox.delete(index)

    def clear_items(self):
        confirm = messagebox.askyesno("Clear List", "Are you sure you want to clear the entire list?")
        if confirm:
            self.listbox.delete(0, tk.END)

    def send_to_phone(self):
        # Check if Twilio client is available.
        if Client is None:
            messagebox.showerror("Twilio Error", "Twilio module not installed. Run 'pip3 install twilio' to enable SMS sending.")
            return

        # Get the phone number from the user.
        phone_num = simpledialog.askstring("Send Shopping List", "Enter phone number with country code (e.g., +15551234567):")
        if not phone_num:
            return

        # Retrieve shopping list items.
        items = self.listbox.get(0, tk.END)
        if not items:
            messagebox.showinfo("Empty List", "Your shopping list is empty.")
            return

        message_body = "Shopping List:\n" + "\n".join(items)

        try:
            # Initialize Twilio Client using credentials from twilio_config.py.
            client = Client(twilio_config.TWILIO_ACCOUNT_SID, twilio_config.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=message_body,
                from_=twilio_config.TWILIO_PHONE_NUMBER,
                to=phone_num
            )
            messagebox.showinfo("Success", "Shopping list sent to your phone!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")
