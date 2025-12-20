import tkinter as tk
from tkinter import colorchooser
import winsound

class ShotClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shot Clock Controller")
        self.root.state("zoomed")
        self.root.configure(bg="black")

        self.time_left = 40
        self.running = False

        # ================= DISPLAY WINDOW =================
        self.display_window = tk.Toplevel(self.root)
        self.display_window.title("Shot Clock Display")
        self.display_window.state("zoomed")
        self.display_window.configure(bg="black")

        self.display_label = tk.Label(
            self.display_window,
            text="40",
            font=("Arial", 250, "bold"),
            fg="white",
            bg="black"
        )
        self.display_label.pack(expand=True)

        # ================= CONTROLLER DISPLAY =================
        self.controller_display = tk.Label(
            self.root,
            text="40",
            font=("Arial", 150, "bold"),
            fg="white",
            bg="black"
        )
        self.controller_display.pack(pady=20)

        # ================= CURSOR / MODE INDICATOR =================
        self.mode_label = tk.Label(
            self.root,
            text="HOTKEY MODE",
            fg="lime",
            bg="black",
            font=("Arial", 16, "bold")
        )
        self.mode_label.pack(pady=5)

        # ================= SETTINGS =================
        settings = tk.Frame(self.root, bg="black")
        settings.pack()

        self.shot_duration = self.create_entry(settings, "Shot Duration", "40", 0)
        self.extension = self.create_entry(settings, "Extension", "15", 1)
        self.alert_time = self.create_entry(settings, "Alert At", "10", 2)
        self.normal_color = self.create_entry(settings, "Normal Color", "white", 3)
        self.alert_color = self.create_entry(settings, "Alert Color", "red", 4)

        # Color picker buttons
        tk.Button(settings, text="Pick Normal Color", command=self.choose_normal_color, width=18).grid(row=3, column=2, padx=10)
        tk.Button(settings, text="Pick Alert Color", command=self.choose_alert_color, width=18).grid(row=4, column=2, padx=10)

        # ================= CONTROLS =================
        controls = tk.Frame(self.root, bg="black")
        controls.pack(pady=30)

        self.create_button(controls, "START (S)", self.start, 0)
        self.create_button(controls, "PAUSE (P)", self.pause, 1)
        self.create_button(controls, "RESET (X)", self.reset, 2)
        self.create_button(controls, "EXTENSION (SPACE)", self.add_extension, 3)

        # ================= BUZZER =================
        self.buzzer_enabled = tk.BooleanVar(value=True)
        tk.Checkbutton(
            self.root,
            text="Enable Alerts",
            variable=self.buzzer_enabled,
            fg="white",
            bg="black",
            font=("Arial", 18),
            selectcolor="black"
        ).pack()

        # ================= GLOBAL HOTKEYS =================
        self.root.bind_all("<s>", lambda e: self.start())
        self.root.bind_all("<p>", lambda e: self.pause())
        self.root.bind_all("<x>", lambda e: self.reset())
        self.root.bind_all("<space>", lambda e: self.add_extension())
        self.root.bind_all("<Escape>", lambda e: self.exit_all())

        self.root.mainloop()

    # ================= UI HELPERS =================
    def create_entry(self, parent, label, default, row):
        tk.Label(
            parent, text=label, fg="white", bg="black", font=("Arial", 18)
        ).grid(row=row, column=0, padx=10, pady=5)

        entry = tk.Entry(parent, font=("Arial", 18), width=8, justify="center")
        entry.insert(0, default)
        entry.grid(row=row, column=1)

        # ENTER / ESC exits typing mode
        entry.bind("<FocusIn>", self.entry_focus_on)
        entry.bind("<Return>", self.exit_entry_mode)
        entry.bind("<Escape>", self.exit_entry_mode)

        return entry

    def create_button(self, parent, text, command, col):
        tk.Button(
            parent,
            text=text,
            font=("Arial", 18, "bold"),
            width=14,
            command=command
        ).grid(row=0, column=col, padx=10)

    # ================= COLOR PICKERS =================
    def choose_normal_color(self):
        color = colorchooser.askcolor()[1]  # Returns (#RRGGBB)
        if color:
            self.normal_color.delete(0, tk.END)
            self.normal_color.insert(0, color)

    def choose_alert_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.alert_color.delete(0, tk.END)
            self.alert_color.insert(0, color)

    # ================= MODE CONTROL =================
    def entry_focus_on(self, event):
        self.mode_label.config(text="EDIT MODE", fg="yellow")

    def exit_entry_mode(self, event=None):
        self.root.focus_set()
        self.mode_label.config(text="HOTKEY MODE", fg="lime")

    # ================= TIMER LOGIC =================
    def update_timer(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.update_display()

            alert = int(self.alert_time.get())
            if self.buzzer_enabled.get() and 0 < self.time_left <= alert:
                winsound.Beep(1200, 150)

            self.root.after(1000, self.update_timer)

        elif self.time_left == 0 and self.buzzer_enabled.get():
            winsound.Beep(2000, 800)

    def update_display(self):
        value = str(self.time_left)
        self.controller_display.config(text=value)
        self.display_label.config(text=value)

        # Update colors based on alert threshold
        alert = int(self.alert_time.get())
        color = self.alert_color.get() if self.time_left <= alert else self.normal_color.get()
        self.controller_display.config(fg=color)
        self.display_label.config(fg=color)

    # ================= ACTIONS =================
    def start(self):
        if not self.running:
            self.exit_entry_mode()
            self.running = True
            self.update_timer()

    def pause(self):
        self.running = False

    def reset(self):
        self.running = False
        self.time_left = int(self.shot_duration.get())
        self.update_display()

    def add_extension(self):
        self.time_left += int(self.extension.get())
        self.update_display()

    def exit_all(self):
        self.root.destroy()

ShotClock()
