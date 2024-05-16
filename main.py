import tkinter as tk
from tkinter import messagebox, colorchooser
import calendar

class InteractiveCalendar:
    def __init__(self, root, year, month):
        self.root = root
        self.year = year
        self.month = month
        self.create_widgets()

    def create_widgets(self):
        self.create_header()
        self.create_days_frame()
        self.create_calendar()

    def create_header(self):
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(fill=tk.X)

        # Previous month button
        prev_button = tk.Button(self.header_frame, text="<", command=self.prev_month)
        prev_button.pack(side=tk.LEFT)

        # Month label
        self.month_label = tk.Label(self.header_frame, text=self.get_month_year(), font=("Helvetica", 16))
        self.month_label.pack(side=tk.LEFT, expand=True)

        # Next month button
        next_button = tk.Button(self.header_frame, text=">", command=self.next_month)
        next_button.pack(side=tk.RIGHT)

    def create_days_frame(self):
        self.days_frame = tk.Frame(self.root)
        self.days_frame.pack(fill=tk.BOTH, expand=True)

    def create_calendar(self):
        # Clear previous calendar if it exists
        for widget in self.days_frame.winfo_children():
            widget.destroy()

        # Create the header for days of the week
        days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for day in days_of_week:
            label = tk.Label(self.days_frame, text=day, borderwidth=1, relief="solid")
            label.grid(row=0, column=days_of_week.index(day), sticky="nsew")

        # Configure grid weights for days of the week
        for i in range(7):
            self.days_frame.columnconfigure(i, weight=1)

        # Get the days of the month
        month_days = calendar.monthcalendar(self.year, self.month)

        # Create buttons for each day in the calendar
        for week_num, week in enumerate(month_days, start=1):
            for day_num, day in enumerate(week):
                if day != 0:
                    day_button = tk.Button(self.days_frame, text=str(day), command=lambda d=day: self.on_date_click(d))
                    day_button.grid(row=week_num, column=day_num, sticky="nsew")

            # Configure grid weights for each row
            self.days_frame.rowconfigure(week_num, weight=1)

    def on_date_click(self, day):
        selected_date = f"{self.year}-{self.month:02d}-{day:02d}"
        self.show_day_schedule(selected_date)

    def show_day_schedule(self, date):
        # Create a new window for the day schedule
        day_window = tk.Toplevel(self.root)
        day_window.title(f"Schedule for {date}")
        day_window.geometry("400x800")  # Set a fixed size for the day schedule window

        # Create a canvas for scrolling
        canvas = tk.Canvas(day_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(day_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Configure grid weights for each row in the frame
        for hour in range(24):
            frame.rowconfigure(hour, weight=1)

        frame.columnconfigure(0, weight=1)

        # Create blocks for each hour in the day
        for hour in range(24):
            hour_frame = tk.Frame(frame, borderwidth=1, relief="solid", height=50)
            hour_frame.grid(row=hour, column=0, sticky="nsew")

            hour_label = tk.Label(hour_frame, text=f"{hour:02d}:00 - {hour+1:02d}:00")
            hour_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Add a canvas to draw tasks on
            hour_tasks_canvas = tk.Canvas(hour_frame, bg="white", relief="sunken")
            hour_tasks_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

            # Store the canvas in a dictionary with the hour as the key
            hour_frame.tasks_canvas = hour_tasks_canvas

            # Example: Double-click to add/edit a task
            hour_tasks_canvas.bind("<Double-1>", lambda e, h=hour: self.add_edit_task(hour_frame, h, date))

        # Update the scroll region
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def add_edit_task(self, hour_frame, hour, date):
        def save_task():
            task = task_entry.get()
            duration = int(duration_entry.get())
            color = color_chooser.cget("bg")

            # Remove previous tasks in the same time slot
            hour_frame.tasks_canvas.delete("all")

            # Draw the task as a colored rectangle on the canvas
            hour_frame.tasks_canvas.create_rectangle(0, 0, 200, 50 * duration, fill=color, tags="task")
            hour_frame.tasks_canvas.create_text(100, 25 * duration, text=task, tags="task")

            task_window.destroy()

        task_window = tk.Toplevel(self.root)
        task_window.title(f"Add/Edit Task for {date} {hour:02d}:00")

        tk.Label(task_window, text="Task:").pack(side=tk.LEFT)
        task_entry = tk.Entry(task_window)
        task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(task_window, text="Duration (hours):").pack(side=tk.LEFT)
        duration_entry = tk.Entry(task_window)
        duration_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(task_window, text="Color:").pack(side=tk.LEFT)
        color_chooser = tk.Button(task_window, text="Choose Color", bg="white", command=lambda: self.choose_color(color_chooser))
        color_chooser.pack(side=tk.LEFT)

        save_button = tk.Button(task_window, text="Save", command=save_task)
        save_button.pack(side=tk.RIGHT)

    def choose_color(self, button):
        color = colorchooser.askcolor()[1]
        if color:
            button.config(bg=color)

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.update_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.update_calendar()

    def update_calendar(self):
        self.month_label.config(text=self.get_month_year())
        self.create_calendar()

    def get_month_year(self):
        return f"{calendar.month_name[self.month]} {self.year}"

if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()
    root.title("Interactive Calendar")

    # Set the window size to half the screen size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = screen_width // 2
    window_height = screen_height // 2
    root.geometry(f"{window_width}x{window_height}")

    # Create an instance of the calendar for May 2024
    cal = InteractiveCalendar(root, 2024, 5)

    # Run the application
    root.mainloop()
