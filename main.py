import tkinter as tk
import traceback

print("Importing KitchenDashboard...")  # Confirm import attempt

try:
    from ui.dashboard import KitchenDashboard
    print("KitchenDashboard import successful.")  # Confirm import success
except Exception as e:
    print("Failed to import KitchenDashboard.")
    traceback.print_exc()

def main():
    try:
        print("Starting GUI root...")
        root = tk.Tk()

        try:
            app = KitchenDashboard(root)
            print("KitchenDashboard initialized.")
        except Exception as inner:
            print("KitchenDashboard failed, showing fallback window.")
            tk.Label(root, text="Fallback window loaded.", font=("Helvetica", 20)).pack(pady=40)
            traceback.print_exc()

        root.mainloop()
    except Exception as e:
        traceback.print_exc()
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()