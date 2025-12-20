import tkinter as tk
from tkinter import colorchooser, filedialog
import winsound

class ShotClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shot Clock Controller")
        self.root.state("zoomed")
        self.root.configure(bg="black")

        self.running = False
        self.time_left = 40
        self.alert_file_path = None  # Custom alert sound path

        # ================= DISPLAY WINDOW =================
        self.display_window = tk.Toplevel(self.root)
        self.display_window.title("Shot Clock Display")
        self.display_window.state("zoomed")
        self.display_window.configure(bg="black")

        self.display_label = tk.Label(
            self.display_window,
            text=str(self.time_left),
            font=("Arial", 250, "bold"),
            fg="white",
            bg="black"
        )
        self.display_label.pack(expand=True)

        # ================= CONTROLLER DISPLAY =================
        self.controller_display = tk.Label(
            self.root,
            text=str(self.time_left),
            font=("Arial", 140, "bold"),
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

        # Entries
        self.start_game_value = self.create_entry(settings, "Start Game At", "40", 0)  # NEW textbox for Start Game
        self.shot_duration = self.create_entry(settings, "Shot Duration", "30", 1)
        self.extension = self.create_entry(settings, "Extension", "15", 2)
        self.alert_time = self.create_entry(settings, "Alert At", "10", 3)
        self.normal_color = self.create_entry(settings, "Normal Color", "white", 4)
        self.alert_color = self.create_entry(settings, "Alert Color", "red", 5)

        # Color picker buttons
        tk.Button(settings, text="Pick Normal Color", command=self.choose_normal_color, width=18).grid(row=4, column=2, padx=10)
        tk.Button(settings, text="Pick Alert Color", command=self.choose_alert_color, width=18).grid(row=5, column=2, padx=10)

        # Custom alert sound
        tk.Button(settings, text="Select Alert Sound File", command=self.select_alert_file, width=22).grid(row=6, column=2, padx=10)

        # ================= CONTROLS =================
        controls = tk.Frame(self.root, bg="black")
        controls.pack(pady=30)

        self.create_button(controls, "Start Game(G)", self.start_game, 0)
        self.create_button(controls, "START (S)", self.start, 1)
        self.create_button(controls, "PAUSE (P)", self.pause, 2)
        self.create_button(controls, "RESET (X)", self.reset, 3)
        self.create_button(controls, "EXTENSION (SPACE)", self.add_extension, 4)

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
        self.root.bind_all("<g>", lambda e: self.start_game()) 
        self.root.bind_all("<Escape>", lambda e: self.exit_all())

        self.start_game_value.focus_set()
        self.mode_label.config(text="EDIT MODE", fg="yellow")

        self.root.mainloop()

    # ================= UI HELPERS =================
    def create_entry(self, parent, label, default, row):
        tk.Label(parent, text=label, fg="white", bg="black", font=("Arial", 18)).grid(row=row, column=0, padx=10, pady=5)
        entry = tk.Entry(parent, font=("Arial", 18), width=8, justify="center")
        entry.insert(0, default)
        entry.grid(row=row, column=1)
        entry.bind("<FocusIn>", self.entry_focus_on)
        entry.bind("<Return>", self.exit_entry_mode)
        entry.bind("<Escape>", self.exit_entry_mode)
        return entry

    def create_button(self, parent, text, command, col):
        tk.Button(parent, text=text, font=("Arial", 18, "bold"), width=14, command=command).grid(row=0, column=col, padx=10)

    # ================= COLOR PICKERS =================
    def choose_normal_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.normal_color.delete(0, tk.END)
            self.normal_color.insert(0, color)

    def choose_alert_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.alert_color.delete(0, tk.END)
            self.alert_color.insert(0, color)

    # ================= ALERT SOUND =================
    def select_alert_file(self):
        file_path = filedialog.askopenfilename(title="Select Alert Sound",
                                               filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))
        if file_path:
            self.alert_file_path = file_path

    def play_alert_sound(self, duration=150):
        if not self.buzzer_enabled.get():
            return
        if self.alert_file_path:
            winsound.PlaySound(self.alert_file_path, winsound.SND_ASYNC)
        else:
            winsound.Beep(1200, duration)

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
            if 0 < self.time_left <= alert:
                self.play_alert_sound()
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0 and self.running:
            self.running = False
            self.update_display()
            self.play_alert_sound(duration=500)

    def update_display(self):
        value = str(self.time_left)
        self.controller_display.config(text=value)
        self.display_label.config(text=value)
        alert = int(self.alert_time.get())
        color = self.alert_color.get() if self.time_left <= alert else self.normal_color.get()
        self.controller_display.config(fg=color)
        self.display_label.config(fg=color)

    # ================= ACTIONS =================
    def start_game(self):
        """Set timer to the value in Start Game At textbox without starting countdown."""
        self.running = False
        self.time_left = int(self.start_game_value.get())
        self.update_display()
        self.start_game_value.focus_set()
        self.mode_label.config(text="EDIT MODE", fg="yellow")

    def start(self):
        if not self.running:
            self.exit_entry_mode()
            self.running = True
            self.update_timer()

    def pause(self):
        self.running = False

    def reset(self):
        """Reset timer to the current Shot Duration value."""
        self.running = False
        self.time_left = int(self.shot_duration.get())
        self.update_display()

    def add_extension(self):
        self.time_left += int(self.extension.get())
        self.update_display()

    def exit_all(self):
        self.root.destroy()


ShotClock()
