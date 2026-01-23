import tkinter as tk
from tkinter import colorchooser, filedialog, simpledialog, messagebox
import winsound
import sys
import os
import time
import secrets
import smtplib
from email.message import EmailMessage

# ================= FONTS =================
FONT_MAIN = ("Arial", 520, "bold")
FONT_CTRL = ("Arial", 90, "bold")
FONT_LABEL = ("Arial", 11)
FONT_BTN = ("Arial", 11, "bold")

# ================= EMAIL CONFIG =================
ADMIN_EMAIL = "cartercarig@gmail.com"     
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "cartercarig@gmail.com"      
EMAIL_PASS = "scfm nzrn gbef bisy"       

# ================= RESOURCE PATH =================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ================= SHOT CLOCK CLASS =================
class ShotClock:
    # ---- OTP FUNCTIONS ----
    def generate_otp(self, length=6):
        return ''.join(secrets.choice("0123456789") for _ in range(length))

    def send_otp_email(self, otp):
        msg = EmailMessage()
        msg['Subject'] = "Your ShotClock OTP"
        msg['From'] = EMAIL_USER
        msg['To'] = ADMIN_EMAIL
        msg.set_content(f"Your ShotClock OTP is: {otp}")
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print("Error sending OTP email:", e)
            return False

    def request_otp(self):
        otp = self.generate_otp()
        if self.send_otp_email(otp):
            user_input = simpledialog.askstring("OTP Verification", "Enter the OTP sent to admin email:")
            if user_input != otp:
                messagebox.showerror("Access Denied", "Incorrect OTP! Exiting...")
                return False
            else:
                messagebox.showinfo("Access Granted", "OTP verified successfully!")
                return True
        else:
            messagebox.showerror("Error", "Failed to send OTP. Check email settings. Exiting...")
            return False

    # ---- INIT ----
    def __init__(self):
        temp_root = tk.Tk()
        temp_root.withdraw()
        if not self.request_otp():
            temp_root.destroy()
            return
        temp_root.destroy()

        self.root = tk.Tk()
        self.root.iconbitmap(resource_path("sba_shotclock.ico"))
        self.root.title("Shot Clock Controller")
        self.root.state("zoomed")
        self.root.configure(bg="black")

        self.running = False
        self.time_left = 40
        self.alert_file_path = None
        self.timer_id = None
        self.last_alert_played = None

        self.vcmd_number = (self.root.register(self.validate_number), "%P")

        # ---- DISPLAY WINDOW ----
        self.display_window = tk.Toplevel(self.root)
        self.display_window.iconbitmap(resource_path("sba_shotclock.ico"))
        self.display_window.title("Shot Clock Display")
        self.display_window.state("zoomed")
        self.display_window.configure(bg="black")
        self.display_window.deiconify()

        self.display_label = tk.Label(
            self.display_window,
            text="40",
            font=FONT_MAIN,
            fg="white",
            bg="black"
        )
        self.display_label.pack(expand=True, fill="both")

        # ---- CONTROLLER DISPLAY ----
        self.controller_display = tk.Label(
            self.root,
            text="40",
            font=FONT_CTRL,
            fg="white",
            bg="black"
        )
        self.controller_display.pack(pady=10)

        self.mode_label = tk.Label(
            self.root,
            text="EDIT MODE",
            fg="yellow",
            bg="black",
            font=("Arial", 14, "bold")
        )
        self.mode_label.pack(pady=5)

        # ---- SETTINGS PANEL ----
        panel = tk.Frame(self.root, bg="#111", bd=2, relief="ridge")
        panel.pack(pady=20, padx=20)

        self.start_game_value = self.create_entry(panel, "Start Game At", "40", 0, numeric=True)
        self.shot_duration   = self.create_entry(panel, "Shot Duration", "30", 1, numeric=True)
        self.extension       = self.create_entry(panel, "Extension", "15", 2, numeric=True)
        self.alert_time      = self.create_entry(panel, "Alert At", "10", 3, numeric=True)
        self.normal_color    = self.create_entry(panel, "Normal Color", "white", 4)
        self.alert_color     = self.create_entry(panel, "Alert Color", "red", 5)

        self.btn_pick_normal = tk.Button(panel, text="Pick Normal Color", command=self.choose_normal_color)
        self.btn_pick_normal.grid(row=4, column=2, padx=10)

        self.btn_pick_alert = tk.Button(panel, text="Pick Alert Color", command=self.choose_alert_color)
        self.btn_pick_alert.grid(row=5, column=2, padx=10)

        self.btn_sound = tk.Button(panel, text="Select Alert Sound", command=self.select_alert_file)
        self.btn_sound.grid(row=6, column=2, pady=5)

        self.buzzer_enabled = tk.BooleanVar(value=True)
        tk.Checkbutton(
            panel,
            text="Enable Alerts",
            variable=self.buzzer_enabled,
            fg="white",
            bg="#111",
            selectcolor="#111",
            font=FONT_LABEL
        ).grid(row=6, column=0, columnspan=2, pady=10)

        # ---- CONTROLS ----
        controls = tk.Frame(self.root, bg="black")
        controls.pack(pady=30)

        self.create_button(controls, "START GAME (G)", self.start_game, 0)
        self.create_button(controls, "START (S)", self.start, 1)
        self.create_button(controls, "PAUSE (P)", self.pause, 2)
        self.create_button(controls, "RESET (X)", self.reset, 3)
        self.create_button(controls, "EXTEND (SPACE)", self.add_extension, 4)

        self.edit_widgets = [
            self.start_game_value,
            self.shot_duration,
            self.extension,
            self.alert_time,
            self.normal_color,
            self.alert_color,
            self.btn_pick_normal,
            self.btn_pick_alert,
            self.btn_sound
        ]

        # ---- HOTKEYS ----
        self.root.bind_all("<s>", lambda e: self.start())
        self.root.bind_all("<p>", lambda e: self.pause())
        self.root.bind_all("<x>", lambda e: self.reset())
        self.root.bind_all("<space>", lambda e: self.add_extension())
        self.root.bind_all("<g>", lambda e: self.start_game())
        self.root.bind_all("<Escape>", lambda e: self.root.destroy())

        self.start_game_value.focus_set()
        self.root.mainloop()

    # ---- VALIDATION ----
    def validate_number(self, value):
        return value.isdigit() or value == ""

    # ---- HELPERS ----
    def create_entry(self, parent, label, default, row, numeric=False):
        tk.Label(parent, text=label, fg="white", bg="#111", font=FONT_LABEL)\
            .grid(row=row, column=0, sticky="e", padx=10, pady=6)
        entry = tk.Entry(
            parent,
            font=FONT_LABEL,
            width=8,
            justify="center",
            validate="key" if numeric else "none",
            validatecommand=self.vcmd_number if numeric else None
        )
        entry.insert(0, default)
        entry.grid(row=row, column=1)
        entry.bind("<FocusIn>", lambda e: self.mode_label.config(text="EDIT MODE", fg="yellow"))
        entry.bind("<Return>", self.exit_entry_mode)
        entry.bind("<Escape>", self.exit_entry_mode)
        return entry

    def create_button(self, parent, text, cmd, col):
        tk.Button(parent, text=text, font=FONT_BTN, width=16, command=cmd)\
            .grid(row=0, column=col, padx=8)

    # ---- COLORS ----
    def choose_normal_color(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.normal_color.delete(0, tk.END)
            self.normal_color.insert(0, c)

    def choose_alert_color(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.alert_color.delete(0, tk.END)
            self.alert_color.insert(0, c)

    # ---- SOUND ----
    def select_alert_file(self):
        self.alert_file_path = filedialog.askopenfilename(
            filetypes=(("WAV files", "*.wav"),)
        )

    def play_alert_sound(self):
        if not self.buzzer_enabled.get():
            return
        if self.alert_file_path:
            winsound.PlaySound(self.alert_file_path, winsound.SND_ASYNC)
        else:
            winsound.Beep(1200, 150)

    # ---- TIMER ----
    def update_timer(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1  # Countdown per second

            # Play alert if below alert time
            alert = int(self.alert_time.get())
            if self.time_left <= alert and self.last_alert_played != self.time_left:
                self.play_alert_sound()
                self.last_alert_played = self.time_left

            self.update_display()

            if self.time_left > 0:
                self.timer_id = self.root.after(1000, self.update_timer)
            else:
                self.running = False
                self.unlock_editing()
                self.play_alert_sound()  # Ensure buzzer at 0

    def update_display(self):
        val = str(self.time_left)
        alert = int(self.alert_time.get())
        color = self.alert_color.get() if self.time_left <= alert else self.normal_color.get()
        self.controller_display.config(text=val, fg=color)
        self.display_label.config(text=val, fg=color)

    # ---- ACTIONS ----
    def start_game(self):
        self.running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.time_left = int(self.start_game_value.get())
        self.last_alert_played = None
        self.update_display()
        self.unlock_editing()

    def start(self):
        if not self.running:
            self.running = True
            self.lock_editing()
            self.mode_label.config(text="HOTKEY MODE", fg="lime")
            self.last_alert_played = None
            self.update_display()  # Show exact start value immediately
            self.timer_id = self.root.after(1000, self.update_timer)  # Start countdown after 1 second

    def pause(self):
        self.running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.unlock_editing()

    def reset(self):
        self.running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.time_left = int(self.shot_duration.get())
        self.last_alert_played = None
        self.update_display()
        self.unlock_editing()

    def add_extension(self):
        self.time_left += int(self.extension.get())
        self.update_display()

    def lock_editing(self):
        for w in self.edit_widgets:
            w.config(state="disabled")
        self.mode_label.config(text="LOCKED (RUNNING)", fg="red")

    def unlock_editing(self):
        for w in self.edit_widgets:
            w.config(state="normal")
        self.mode_label.config(text="EDIT MODE", fg="yellow")

    def exit_entry_mode(self, event=None):
        self.root.focus_set()
        self.mode_label.config(text="HOTKEY MODE", fg="lime")

# ---- RUN APP ----
ShotClock()
