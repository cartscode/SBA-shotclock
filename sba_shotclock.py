import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser, filedialog, simpledialog, messagebox
import winsound
import sys
import os
import time
import secrets
root = tk.Tk()
root.title("Scoreboard Software")

root.geometry("1000x600")
root.minsize(950, 780)
# root.maxsize(1100, 700)

root.configure(bg="#000000")
root.resizable(True, True)

# ❌ REMOVE this line:
# root.attributes("-toolwindow", True)


root.configure(bg="#000000")

# Optional: disable maximize button (Windows)
root.resizable(True, True)
# root.attributes("-toolwindow", True)  # makes it feel like a control panel

# ================== STYLES ==================
style = ttk.Style()
style.theme_use("default")

style.configure("Card.TFrame", background="#121212")
style.configure("Title.TLabel", background="#121212", foreground="white", font=("Arial", 16, "bold"))
style.configure("Label.TLabel", background="#121212", foreground="white", font=("Arial", 12))
style.configure("Entry.TEntry", font=("Arial", 11))

# ================== MAIN CONTAINER ==================
main = tk.Frame(root, bg="black")
main.pack(fill="both", expand=True, padx=8, pady=8)

# ================== TOP SECTION ==================
top = tk.Frame(main, bg="black")
top.pack(fill="x")

# ---------- LEFT TEAM ----------
left_team = ttk.Frame(top, style="Card.TFrame", padding=10)
left_team.pack(side="left", fill="y", padx=10)
    

ttk.Label(left_team, text="Team", style="Title.TLabel").pack(anchor="center")
ttk.Entry(left_team, width=25).pack(pady=5)

ttk.Label(left_team, text="Player's Name", style="Label.TLabel").pack(anchor="center", pady=(10, 5))

for _ in range(5):
    row = tk.Frame(left_team, bg="#121212")
    row.pack(fill="x", pady=4)
    tk.Button(row, text="Select", width=8).pack(side="left")
    ttk.Entry(row).pack(side="left", padx=5, fill="x", expand=True)

#---------------Need to be fix add function ---------------

# ---------- CENTER TIMER ----------
center = ttk.Frame(top, style="Card.TFrame", padding=10)
center.pack(side="left", expand=True, fill="both", padx=10)

# ----------------- TIMER LABEL -----------------
timer_value = tk.IntVar(value=40)

start_game_at = tk.IntVar(value=40)
shot_duration = tk.IntVar(value=30)
extension_seconds = tk.IntVar(value=10)
alert_time = tk.IntVar(value=5)

alert_enabled = tk.BooleanVar(value=True)

running = False
timer_job = None

# ✅ MOVED HERE (FIXED ORDER)
normal_color_value = tk.StringVar(value="white")
alert_color_value = tk.StringVar(value="red")
alert_sound_path = None


timer_label = ttk.Label(
    center,
    textvariable=timer_value,
    foreground="#FFFFFF",
    background="#121212",
    font=("Arial", 48, "bold")
)
timer_label.pack()

ttk.Label(center, text="EDIT MODE", foreground="#FFD700",
          background="#121212", font=("Arial", 14, "bold")).pack(pady=5)

def config_row(parent, label):
    row = tk.Frame(parent, bg="#121212")
    row.pack(pady=4)
    ttk.Label(row, text=label, style="Label.TLabel", width=15).pack(side="left")
    ttk.Entry(row, width=10).pack(side="left")

config_row(center, "Start game at:")
config_row(center, "Shot Duration:")
config_row(center, "Extention:")
config_row(center, "Alert At:")

# ----------------- COLOR ROW -----------------
color_row = tk.Frame(center, bg="#121212")
color_row.pack(pady=5)

ttk.Label(color_row, text="Normal Color:", style="Label.TLabel").pack(side="left")

normal_color_entry = ttk.Entry(color_row, width=10, textvariable=normal_color_value)
normal_color_entry.pack(side="left", padx=5)

tk.Button(color_row, text="Select", command=lambda: choose_normal_color()).pack(side="left")

# ----------------- ALERT COLOR ROW -----------------
color_row2 = tk.Frame(center, bg="#121212")
color_row2.pack(pady=5)

ttk.Label(color_row2, text="Alert Color:", style="Label.TLabel").pack(side="left")

alert_color_entry = ttk.Entry(color_row2, width=10, textvariable=alert_color_value)
alert_color_entry.pack(side="left", padx=5)

tk.Button(color_row2, text="Select", command=lambda: choose_alert_color()).pack(side="left")

# ----------------- ALERT ROW -----------------
alert_row = tk.Frame(center, bg="#121212")
alert_row.pack(pady=10)

tk.Checkbutton(alert_row, text="Enable Alert", fg="white",
               bg="#121212", selectcolor="#121212",
               variable=alert_enabled).pack(side="left")

# ✅ FIXED BUTTON
tk.Button(alert_row, text="Select", command=lambda: select_alert_file()).pack(side="left", padx=5)


# =====================================================
# 🔥 ADDED 3 FUNCTIONS
# =====================================================

def choose_normal_color():
    color = colorchooser.askcolor()[1]
    if color:
        normal_color_value.set(color)
        timer_label.config(foreground=color)


def choose_alert_color():
    color = colorchooser.askcolor()[1]
    if color:
        alert_color_value.set(color)


def select_alert_file():
    global alert_sound_path
    path = filedialog.askopenfilename(
        filetypes=[("WAV files", "*.wav")]
    )
    if path:
        alert_sound_path = path


# ----------------- TIMER FUNCTIONS -----------------
def update_timer():
    global running, timer_job

    if not running:
        return

    current = timer_value.get()

    if current > 0:
        timer_value.set(current - 1)

        if alert_enabled.get() and current - 1 <= alert_time.get():
            timer_label.config(foreground=alert_color_value.get())

            if alert_sound_path:
                winsound.PlaySound(alert_sound_path, winsound.SND_ASYNC)
            else:
                winsound.Beep(1200, 60)
        else:
            timer_label.config(foreground=normal_color_value.get())

        timer_job = root.after(1000, update_timer)

    else:
        running = False
        timer_label.config(foreground=alert_color_value.get())

        if alert_sound_path:
            winsound.PlaySound(alert_sound_path, winsound.SND_ASYNC)
        else:
            winsound.Beep(1500, 300)


def start_game():
    stop_timer()
    timer_value.set(start_game_at.get())
    timer_label.config(foreground=normal_color_value.get())


def start_timer():
    global running
    if running:
        return
    running = True
    update_timer()


def pause_timer():
    stop_timer()


def stop_timer():
    global running, timer_job
    running = False
    if timer_job:
        root.after_cancel(timer_job)
        timer_job = None


def reset_timer():
    stop_timer()
    timer_value.set(shot_duration.get())
    timer_label.config(foreground=normal_color_value.get())


def add_extension():
    if timer_value.get() > 0:
        timer_value.set(timer_value.get() + extension_seconds.get())


# ----------------- CONTROLS -----------------
controls = tk.Frame(center, bg="#121212")
controls.pack(pady=10)

buttons_text = ["Start Game(G)", "Start(S)", "Pause(P)", "Reset(X)", "Extention(Space)"]
buttons_command = [
    start_game,
    start_timer,
    pause_timer,
    reset_timer,
    add_extension
]

for text, cmd in zip(buttons_text, buttons_command):
    tk.Button(controls, text=text, command=cmd).pack(side="left", padx=5)

# ----------------- KEYBINDINGS -----------------
root.bind("g", lambda e: start_game())
root.bind("s", lambda e: start_timer())
root.bind("p", lambda e: pause_timer())
root.bind("x", lambda e: reset_timer())
root.bind("<space>", lambda e: add_extension())
#------fix(adding function)----
# ---------- RIGHT TEAM ----------
right_team = ttk.Frame(top, style="Card.TFrame", padding=10)
right_team.pack(side="left", fill="y", padx=10)

ttk.Label(right_team, text="Team", style="Title.TLabel").pack(anchor="center")
ttk.Entry(right_team, width=25).pack(pady=5)

ttk.Label(right_team, text="Player's Name", style="Label.TLabel").pack(anchor="center", pady=(10, 5))

for _ in range(5):
    row = tk.Frame(right_team, bg="#121212")
    row.pack(fill="x", pady=4)
    tk.Button(row, text="Select", width=8).pack(side="left")
    ttk.Entry(row).pack(side="left", padx=5, fill="x", expand=True)

# ================== BOTTOM SECTION ==================
bottom = tk.Frame(main, bg="black")
bottom.pack(fill="x", pady=20)

# ---------- PLAYER 1 ----------
p1 = ttk.Frame(bottom, style="Card.TFrame", padding=10)
p1.pack(side="left", fill="x", expand=True, padx=10)

ttk.Label(
    p1,
    text="Player 1",
    style="Title.TLabel"
).pack(anchor="center")

name_row1 = tk.Frame(p1, bg="#121212")
name_row1.pack(pady=5)

# STOP auto expansion
name_row1.columnconfigure(0, weight=0)
name_row1.columnconfigure(1, weight=0)

ttk.Label(
    name_row1,
    text="Name:",
    style="Label.TLabel"
).grid(row=0, column=0, sticky="e", padx=(0, 8))

# Custom width Entry
nick1 = ttk.Entry(
    name_row1,
    width=24   # 👈 adjust freely
)
nick1.grid(row=0, column=1, sticky="w")




# SCORE
score_row = tk.Frame(p1, bg="#121212")
score_row.pack(pady=10)

tk.Button(score_row, text="-", width=4).pack(side="left")
ttk.Label(score_row, text="0", font=("Arial", 32, "bold"),
          background="#121212", foreground="white").pack(side="left", padx=10)
tk.Button(score_row, text="+", width=4).pack(side="left")

# FOUL & EXT
fe_row = tk.Frame(p1, bg="#121212")
fe_row.pack(pady=10)

# FOUL
tk.Label(fe_row, text="Foul:", fg="white", bg="#121212").grid(row=0, column=0, padx=5)
ttk.Label(fe_row, text="0", width=3, anchor="center").grid(row=0, column=1)
tk.Button(fe_row, text="+", width=3).grid(row=0, column=2)
tk.Button(fe_row, text="Reset", width=6).grid(row=0, column=3, padx=5)

# EXT
tk.Label(fe_row, text="Ext:", fg="white", bg="#121212").grid(row=1, column=0, padx=5, pady=5)
ttk.Label(fe_row, text="1", width=3, anchor="center").grid(row=1, column=1)
tk.Button(fe_row, text="-", width=3).grid(row=1, column=2)

# ---------- CENTER CONTROL ----------
mid = ttk.Frame(bottom, style="Card.TFrame", padding=10)
mid.pack(side="left", padx=10)

ttk.Entry(mid, justify="center", width=30).pack(fill="x", pady=5)
ttk.Label(mid, text="Label", style="Label.TLabel").pack()
tk.Button(mid, text="<- Switch ->").pack(pady=5)
tk.Button(mid, text="Reset Score").pack(pady=5)
tk.Checkbutton(mid, text="Auto Update", fg="white",
               bg="#121212", selectcolor="#121212").pack(pady=5)
tk.Button(mid, text="UPDATE", font=("Arial", 18, "bold"),
          bg="#BDBDBD").pack(pady=10, fill="x")

# ---------- PLAYER 2 ----------
# Player 2 card
p2 = ttk.Frame(bottom, style="Card.TFrame", padding=10)
p2.pack(side="left", fill="x", expand=True, padx=10)

# Title
ttk.Label(
    p2,
    text="Player 2",
    style="Title.TLabel"
).pack(anchor="center")

# Name row
name_row2 = tk.Frame(p2, bg="#121212")
name_row2.pack(pady=5)

# DO NOT allow column expansion
name_row2.columnconfigure(0, weight=0)
name_row2.columnconfigure(1, weight=0)

# Label
ttk.Label(
    name_row2,
    text="Name:",
    style="Label.TLabel"
).grid(row=0, column=0, sticky="e", padx=(0, 8))

# Entry (custom width)
nick2 = ttk.Entry(
    name_row2,
    width=24 # 👈 adjust this number to control width
)

# IMPORTANT: no horizontal stretching
nick2.grid(row=0, column=1, sticky="w")




# SCORE
score_row2 = tk.Frame(p2, bg="#121212")
score_row2.pack(pady=10)

tk.Button(score_row2, text="-", width=4).pack(side="left")
ttk.Label(score_row2, text="0", font=("Arial", 32, "bold"),
          background="#121212", foreground="white").pack(side="left", padx=10)
tk.Button(score_row2, text="+", width=4).pack(side="left")

# FOUL & EXT
fe_row2 = tk.Frame(p2, bg="#121212")
fe_row2.pack(pady=10)

# FOUL
tk.Label(fe_row2, text="Foul:", fg="white", bg="#121212").grid(row=0, column=0, padx=5)
ttk.Label(fe_row2, text="0", width=3, anchor="center").grid(row=0, column=1)
tk.Button(fe_row2, text="+", width=3).grid(row=0, column=2)
tk.Button(fe_row2, text="Reset", width=6).grid(row=0, column=3, padx=5)

# EXT
tk.Label(fe_row2, text="Ext:", fg="white", bg="#121212").grid(row=1, column=0, padx=5, pady=5)
ttk.Label(fe_row2, text="1", width=3, anchor="center").grid(row=1, column=1)
tk.Button(fe_row2, text="-", width=3).grid(row=1, column=2)


# ================== RUN ==================
root.mainloop() 