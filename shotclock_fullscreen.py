import tkinter as tk
import winsound  # Windows buzzer

class ShotClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shot Clock Controller")
        self.root.state("zoomed")
        self.root.configure(bg="black")

        self.time_left = 40
        self.running = False

        # ================= DISPLAY WINDOW =================
        self.display_window = tk.Tk()
        self.display_window.title("Shot Clock Display")
        self.display_window.state("zoomed")
        self.display_window.configure(bg="black")

        self.display_label = tk.Label(
            self.display_window,
            text="40",
            font=("Arial", 250, "bold"),
            fg="red",
            bg="black"
        )
        self.display_label.pack(expand=True)

        # ================= CONTROLLER DISPLAY =================
        self.controller_display = tk.Label(
            self.root,
            text="40",
            font=("Arial", 150, "bold"),
            fg="red",
            bg="black"
        )
        self.controller_display.pack(pady=20)

        # ================= SETTINGS =================
        settings = tk.Frame(self.root, bg="black")
        settings.pack()

        self.shot_duration = self.create_entry(settings, "Shot Duration", "40", 0)
        self.extension = self.create_entry(settings, "Extension", "15", 1)
        self.alert_time = self.create_entry(settings, "Alert At", "10", 2)

        # ================= CONTROLS =================
        controls = tk.Frame(self.root, bg="black")
        controls.pack(pady=30)

        self.create_button(controls, "START", self.start, 0)
        self.create_button(controls, "PAUSE", self.pause, 1)
        self.create_button(controls, "STOP", self.stop, 2)
        self.create_button(controls, "RESET", self.reset, 3)
        self.create_button(controls, "EXTENSION", self.add_extension, 4)

        # ================= BUZZER =================
        self.buzzer_enabled = tk.BooleanVar(value=True)
        buzzer_check = tk.Checkbutton(
            self.root,
            text="Enable Alerts",
            variable=self.buzzer_enabled,
            fg="white",
            bg="black",
            font=("Arial", 18),
            selectcolor="black"
        )
        buzzer_check.pack()

        # Exit shortcut
        self.root.bind("<Escape>", lambda e: self.exit_all())

        self.root.mainloop()

    # ================= UI HELPERS =================
    def create_entry(self, parent, label, default, row):
        tk.Label(
            parent, text=label, fg="white", bg="black", font=("Arial", 18)
        ).grid(row=row, column=0, padx=10, pady=5)

        entry = tk.Entry(parent, font=("Arial", 18), width=5)
        entry.insert(0, default)
        entry.grid(row=row, column=1)
        return entry

    def create_button(self, parent, text, command, col):
        tk.Button(
            parent,
            text=text,
            font=("Arial", 18, "bold"),
            width=10,
            command=command
        ).grid(row=0, column=col, padx=10)

    # ================= TIMER LOGIC =================
    def update_timer(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.update_display()

            alert = int(self.alert_time.get())
            if self.buzzer_enabled.get() and self.time_left <= alert and self.time_left > 0:
                winsound.Beep(1200, 150)

            self.root.after(1000, self.update_timer)

        elif self.time_left == 0 and self.buzzer_enabled.get():
            winsound.Beep(2000, 800)

    def update_display(self):
        self.controller_display.config(text=str(self.time_left))
        self.display_label.config(text=str(self.time_left))

    # ================= BUTTON ACTIONS =================
    def start(self):
        if not self.running:
            self.running = True
            self.update_timer()

    def pause(self):
        self.running = False

    def stop(self):
        self.running = False
        self.time_left = 0
        self.update_display()

    def reset(self):
        self.running = False
        self.time_left = int(self.shot_duration.get())
        self.update_display()

    def add_extension(self):
        self.time_left += int(self.extension.get())
        self.update_display()

    def exit_all(self):
        self.display_window.destroy()
        self.root.destroy()


ShotClock()
