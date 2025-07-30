# Kitchen Dashboard

A fullscreen kitchen assistant built with Python and Tkinter for Raspberry Pi. The dashboard includes multiple timers, a live clock, a recipe viewer, and a shopping list system. It’s designed to run on a 10.1” touchscreen with a clean interface and easy access to essential tools while cooking.

## Features

- Real-time 12-hour clock
- Multiple adjustable cooking timers
- Recipe viewer with the ability to add and delete entries
- Shopping list with both keyboard and touchscreen input
- Email notifications for shopping list updates and timer alerts
- Idle background/screensaver feature in progress
- Voice input planned for future updates

## Built With

- Python 3
- Tkinter for the GUI
- smtplib for sending email alerts
- Raspberry Pi 5 with touchscreen
- Linux (Raspberry Pi OS)

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/dloganwilli/kitchen-dashboard.git
   cd kitchen-dashboard
   ```

2. (Optional) Set up environment variables or config files for email alerts.

3. Run the dashboard:
   ```bash
   python3 main.py
   ```

## Project Structure

```
kitchen-dashboard/
├── ui/
│   ├── clock.py
│   ├── dashboard.py
│   ├── keyboard.py
│   └── ...
├── data/
│   └── recipes.db
├── setup_db.py
├── main.py
├── .gitignore
└── README.md
```

## To-Do / Future Improvements

- Finalize voice input functionality
- Improve touchscreen interface design and usability
- Add cloud syncing or export for recipes and shopping list
- Add a screensaver-style animated idle screen

## Author

Logan Williamson  
[GitHub](https://github.com/dloganwilli)
