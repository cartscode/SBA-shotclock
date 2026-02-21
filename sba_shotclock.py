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

SELECT_COLOR = "#4FC3F7"   # Light Blue
DEFAULT_BTN_COLOR = "#F0F0F0"  # Default system color
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

left_team_name_var = tk.StringVar()
left_team_entry = ttk.Entry(left_team, width=25, textvariable=left_team_name_var)
left_team_entry.pack(pady=5)

ttk.Label(left_team, text="Player's Name",
          style="Label.TLabel").pack(anchor="center", pady=(10, 5))

left_player_vars = []
left_player_entries = []

left_select_buttons = []

for i in range(6):
    row = tk.Frame(left_team, bg="#121212")
    row.pack(fill="x", pady=4)

    var = tk.StringVar()

    select_btn = tk.Button(
        row,
        text="Select",
        width=8
    )
    select_btn.pack(side="left")

    def make_select(v, btn):
        def select_action():
            player1_name_var.set(v.get())
            update_obs_player_names()

            # Reset all buttons color
            for b in left_select_buttons:
                b.config(bg=DEFAULT_BTN_COLOR)

            # Highlight selected
            btn.config(bg=SELECT_COLOR)

        return select_action

    select_btn.config(command=make_select(var, select_btn))

    entry = ttk.Entry(row, textvariable=var)
    entry.pack(side="left", padx=5, fill="x", expand=True)

    left_player_vars.append(var)
    left_player_entries.append(entry)
    left_select_buttons.append(select_btn)


def save_left_team_data():
    with open("left_team.txt", "w", encoding="utf-8") as file:
        file.write(f"Team:{left_team_name_var.get()}\n")

        for i, var in enumerate(left_player_vars):
            file.write(f"Player{i+1}:{var.get()}\n")
def load_left_team_data():
    try:
        with open("left_team.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith("Team:"):
                left_team_name_var.set(line.strip().split(":", 1)[1])

            elif line.startswith("Player"):
                parts = line.strip().split(":", 1)
                index = int(parts[0].replace("Player", "")) - 1
                if 0 <= index < len(left_player_vars):
                    left_player_vars[index].set(parts[1])

    except FileNotFoundError:
        pass
def auto_save_left(*args):
    save_left_team_data()

left_team_name_var.trace_add("write", auto_save_left)

for var in left_player_vars:
    var.trace_add("write", auto_save_left)


# ---------- CENTER TIMER ----------
center = ttk.Frame(top, style="Card.TFrame", padding=10)
center.pack(side="left", expand=True, fill="both", padx=10)

# ----------------- TIMER VARIABLES -----------------
timer_value = tk.IntVar(value=40)

start_game_at = tk.IntVar(value=40)
shot_duration = tk.IntVar(value=30)
extension_seconds = tk.IntVar(value=15)
alert_time = tk.IntVar(value=0)

alert_enabled = tk.BooleanVar(value=True)

running = False
timer_job = None
last_alert_played = None  # 🔥 prevent alert spam

normal_color_value = tk.StringVar(value="white")
alert_color_value = tk.StringVar(value="red")
alert_sound_path = None

# 🔥 LIST TO STORE EDITABLE WIDGETS
edit_widgets = []

# ----------------- TIMER LABEL -----------------
timer_label = ttk.Label(
    center,
    textvariable=timer_value,
    foreground="#FFFFFF",
    background="#121212",
    font=("Arial", 48, "bold")
)
timer_label.pack()

mode_label = tk.Label(
    center,
    text="EDIT MODE",
    fg="#FFD700",
    bg="#121212",
    font=("Arial", 14, "bold")
)
mode_label.pack(pady=5)


# ----------------- DISPLAY WINDOW -----------------
display_window = tk.Toplevel(root)
display_window.title("Shot Clock Display")
display_window.configure(bg="black")
display_window.state("zoomed")

display_label = tk.Label(
    display_window,
    textvariable=timer_value,
    font=("Arial", 600, "bold"),
    fg="white",
    bg="black"
)
display_label.pack(expand=True)

# ----------------- VALIDATION FUNCTION -----------------
def only_numbers(P):
    return P.isdigit() or P == ""

# ----------------- CONFIG ROW -----------------
shotclock_entries = []

def config_row(parent, label, variable):
    row = tk.Frame(parent, bg="#121212")
    row.pack(pady=4)

    ttk.Label(row, text=label, style="Label.TLabel", width=15).pack(side="left")

    vcmd = (parent.register(only_numbers), "%P")

    entry = ttk.Entry(row, width=10, textvariable=variable,
                      validate="key", validatecommand=vcmd)
    entry.pack(side="left")

    # 🔥 MUST BE INSIDE FUNCTION
    edit_widgets.append(entry)
    shotclock_entries.append(entry)


# ----------------- CONFIG ROWS -----------------
config_row(center, "Start game at:", start_game_at)
config_row(center, "Shot Duration:", shot_duration)
config_row(center, "Extension:", extension_seconds)
config_row(center, "Alert At:", alert_time)

# ----------------- COLOR ROW -----------------
color_row = tk.Frame(center, bg="#121212")
color_row.pack(pady=5)

ttk.Label(color_row, text="Normal Color:",
          style="Label.TLabel").pack(side="left")

normal_color_entry = ttk.Entry(color_row, width=10,
                               textvariable=normal_color_value)
normal_color_entry.pack(side="left", padx=5)
edit_widgets.append(normal_color_entry)

normal_color_btn = tk.Button(
    color_row, text="Select",
    command=lambda: choose_normal_color())
normal_color_btn.pack(side="left")
edit_widgets.append(normal_color_btn)

# ----------------- ALERT COLOR ROW -----------------
color_row2 = tk.Frame(center, bg="#121212")
color_row2.pack(pady=5)

ttk.Label(color_row2, text="Alert Color:",
          style="Label.TLabel").pack(side="left")

alert_color_entry = ttk.Entry(color_row2, width=10,
                              textvariable=alert_color_value)
alert_color_entry.pack(side="left", padx=5)
edit_widgets.append(alert_color_entry)

alert_color_btn = tk.Button(
    color_row2, text="Select",
    command=lambda: choose_alert_color())
alert_color_btn.pack(side="left")
edit_widgets.append(alert_color_btn)

# ----------------- ALERT ROW -----------------
alert_row = tk.Frame(center, bg="#121212")
alert_row.pack(pady=10)

alert_checkbox = tk.Checkbutton(
    alert_row, text="Enable Alert",
    fg="white", bg="#121212",
    selectcolor="#121212",
    variable=alert_enabled)
alert_checkbox.pack(side="left")
edit_widgets.append(alert_checkbox)

alert_sound_btn = tk.Button(
    alert_row, text="Select",
    command=lambda: select_alert_file())
alert_sound_btn.pack(side="left", padx=5)
edit_widgets.append(alert_sound_btn)

# =====================================================
# COLOR + SOUND FUNCTIONS
# =====================================================
def choose_normal_color():
    color = colorchooser.askcolor()[1]
    if color:
        normal_color_value.set(color)
        timer_label.config(foreground=color)
        display_label.config(fg=color)

def choose_alert_color():
    color = colorchooser.askcolor()[1]
    if color:
        alert_color_value.set(color)

def select_alert_file():
    global alert_sound_path
    path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if path:
        alert_sound_path = path

def play_alert_sound(final=False):
    if not alert_enabled.get():
        return

    if alert_sound_path:
        winsound.PlaySound(alert_sound_path, winsound.SND_ASYNC)
    else:
        if final:
            winsound.Beep(1500, 300)
        else:
            winsound.Beep(1200, 60)

# =====================================================
# LOCK / UNLOCK
# =====================================================
def lock_editing():
    for widget in edit_widgets:
        widget.config(state="disabled")

    mode_label.config(text="HOTKEY MODE", fg="#00FF00")


def unlock_editing():
    for widget in edit_widgets:
        widget.config(state="normal")

    mode_label.config(text="EDIT MODE", fg="#FFD700")


# =====================================================
# TIMER LOGIC
# =====================================================
def update_timer():
    global running, timer_job, last_alert_played

    if not running:
        return

    current = timer_value.get()

    if current <= 0:
        running = False
        timer_label.config(foreground=alert_color_value.get())
        display_label.config(fg=alert_color_value.get())
        play_alert_sound(final=True)
        unlock_editing()
        return

    # 🔥 Handle alert color BEFORE decrement
    if alert_enabled.get() and current <= alert_time.get():
        timer_label.config(foreground=alert_color_value.get())
        display_label.config(fg=alert_color_value.get())

        if last_alert_played != current:
            play_alert_sound()
            last_alert_played = current
    else:
        timer_label.config(foreground=normal_color_value.get())
        display_label.config(fg=normal_color_value.get())

    # 🔥 Wait 1 second THEN decrease
    timer_job = root.after(1000, decrement_timer)
def decrement_timer():
    if running:
        timer_value.set(timer_value.get() - 1)
        update_timer()


def start_game():
    global last_alert_played
    stop_timer()
    last_alert_played = None
    timer_value.set(start_game_at.get())
    timer_label.config(foreground=normal_color_value.get())
    display_label.config(fg=normal_color_value.get())
    unlock_editing()

def start_timer():
    global running, last_alert_played
    if running:
        return

    last_alert_played = None
    running = True
    lock_editing()
    update_timer()

def pause_timer():
    stop_timer()
    unlock_editing()

def stop_timer():
    global running, timer_job
    running = False
    if timer_job:
        root.after_cancel(timer_job)
        timer_job = None

def reset_timer():
    global last_alert_played
    stop_timer()
    last_alert_played = None
    timer_value.set(shot_duration.get())
    timer_label.config(foreground=normal_color_value.get())
    display_label.config(fg=normal_color_value.get())
    unlock_editing()

def add_extension():
    if timer_value.get() > 0:
        timer_value.set(timer_value.get() + extension_seconds.get())



# ----------------- KEYBINDINGS -----------------
def allow_hotkeys():
    focused = root.focus_get()
    return focused in shotclock_entries

# ----------------- SAFE HOTKEY SYSTEM -----------------

def safe_start_game(event=None):
    if allow_hotkeys():
        start_game()

def safe_start_timer(event=None):
    if allow_hotkeys():
        start_timer()

def safe_pause(event=None):
    if allow_hotkeys():
        pause_timer()

def safe_reset(event=None):
    if allow_hotkeys():
        reset_timer()

def safe_extension(event=None):
    if allow_hotkeys():
        add_extension()


# ----------------- KEYBINDINGS -----------------
root.bind("g", safe_start_game)
root.bind("s", safe_start_timer)
root.bind("p", safe_pause)
root.bind("x", safe_reset)
root.bind("<space>", safe_extension)

# ---------------- RIGHT TEAM ----------------
right_team = ttk.Frame(top, style="Card.TFrame", padding=10)
right_team.pack(side="left", fill="y", padx=10)

ttk.Label(right_team, text="Team", style="Title.TLabel").pack(anchor="center")

team_name_var = tk.StringVar()
team_entry = ttk.Entry(right_team, width=25, textvariable=team_name_var)
team_entry.pack(pady=5)

ttk.Label(right_team, text="Player's Name",
          style="Label.TLabel").pack(anchor="center", pady=(10, 5))

player_vars = []
player_entries = []

right_select_buttons = []

for i in range(6):
    row = tk.Frame(right_team, bg="#121212")
    row.pack(fill="x", pady=4)

    var = tk.StringVar()

    select_btn = tk.Button(
        row,
        text="Select",
        width=8
    )
    select_btn.pack(side="left")

    def make_select(v, btn):
        def select_action():
            player2_name_var.set(v.get())
            update_obs_player_names()

            # Reset all buttons
            for b in right_select_buttons:
                b.config(bg=DEFAULT_BTN_COLOR)

            # Highlight selected
            btn.config(bg=SELECT_COLOR)

        return select_action

    select_btn.config(command=make_select(var, select_btn))

    entry = ttk.Entry(row, textvariable=var)
    entry.pack(side="left", padx=5, fill="x", expand=True)

    player_vars.append(var)
    player_entries.append(entry)
    right_select_buttons.append(select_btn)


def save_team_data():
    with open("right_team.txt", "w", encoding="utf-8") as file:
        file.write(f"Team:{team_name_var.get()}\n")

        for i, var in enumerate(player_vars):
            file.write(f"Player{i+1}:{var.get()}\n")
def load_team_data():
    try:
        with open("right_team.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith("Team:"):
                team_name_var.set(line.strip().split(":", 1)[1])

            elif line.startswith("Player"):
                parts = line.strip().split(":", 1)
                index = int(parts[0].replace("Player", "")) - 1
                if 0 <= index < len(player_vars):
                    player_vars[index].set(parts[1])

    except FileNotFoundError:
        pass
def auto_save(*args):
    save_team_data()

team_name_var.trace_add("write", auto_save)

for var in player_vars:
    var.trace_add("write", auto_save)


# ================= SCORE VARIABLES =================
player1_score = tk.IntVar(value=0)
player2_score = tk.IntVar(value=0)
# ================= FOUL & EXT VARIABLES =================
player1_foul = tk.IntVar(value=0)
player1_ext = tk.IntVar(value=1)

player2_foul = tk.IntVar(value=0)
player2_ext = tk.IntVar(value=1)

# ================= SCORE AUTO SAVE =================
def save_scores_to_obs(*args):
    # Player 1 score
    with open("obs_player1_score.txt", "w", encoding="utf-8") as f:
        f.write(str(player1_score.get()))

    # Player 2 score
    with open("obs_player2_score.txt", "w", encoding="utf-8") as f:
        f.write(str(player2_score.get()))
        
player1_score.trace_add("write", save_scores_to_obs)
player2_score.trace_add("write", save_scores_to_obs)

# ================= FOUL & EXT AUTO SAVE =================
def save_foul_ext_to_obs(*args):

    # Convert number to black dots
    p1_dots = "●" * player1_foul.get()
    p2_dots = "●" * player2_foul.get()

    with open("obs_player1_foul.txt", "w", encoding="utf-8") as f:
        f.write(p1_dots.strip())

    with open("obs_player2_foul.txt", "w", encoding="utf-8") as f:
        f.write(p2_dots.strip())

    # Extension stays number
    with open("obs_player1_ext.txt", "w", encoding="utf-8") as f:
        f.write(str(player1_ext.get()))

    with open("obs_player2_ext.txt", "w", encoding="utf-8") as f:
        f.write(str(player2_ext.get()))

player1_foul.trace_add("write", save_foul_ext_to_obs)
player2_foul.trace_add("write", save_foul_ext_to_obs)
player1_ext.trace_add("write", save_foul_ext_to_obs)
player2_ext.trace_add("write", save_foul_ext_to_obs)

# ================ SCORE FUNCTION =================
def change_score(score_var, amount):
    new_value = score_var.get() + amount
    if new_value < 0:
        new_value = 0
    score_var.set(new_value)

def reset_all_scores():
    player1_score.set(0)
    player2_score.set(0)

# ================= FOUL & EXT FUNCTIONS =================
def change_stat(stat_var, amount, minimum=0):
    new_value = stat_var.get() + amount
    if new_value < minimum:
        new_value = minimum
    stat_var.set(new_value)

def reset_stat(stat_var, value=0):
    stat_var.set(value)
#---obs center label update---
def save_center_label(*args):
    with open("obs_center_label.txt", "w", encoding="utf-8") as f:
        f.write(center_label_var.get())
    
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

name_row1.columnconfigure(0, weight=0)
name_row1.columnconfigure(1, weight=0)

ttk.Label(
    name_row1,
    text="Name:",
    style="Label.TLabel"
).grid(row=0, column=0, sticky="e", padx=(0, 8))

player1_name_var = tk.StringVar()

nick1 = ttk.Entry(
    name_row1,
    width=24,
    textvariable=player1_name_var
)
nick1.grid(row=0, column=1, sticky="w")


# SCORE
score_row = tk.Frame(p1, bg="#121212")
score_row.pack(pady=10)

tk.Button(score_row, text="-", width=4,
      command=lambda: change_score(player1_score, -1)).pack(side="left")

ttk.Label(score_row,
      textvariable=player1_score,
      font=("Arial", 32, "bold"),
      background="#121212",
      foreground="white").pack(side="left", padx=10)

tk.Button(score_row, text="+", width=4,
      command=lambda: change_score(player1_score, 1)).pack(side="left")

# FOUL & EXT
fe_row = tk.Frame(p1, bg="#121212")
fe_row.pack(pady=10)

tk.Label(fe_row, text="Foul:", fg="white", bg="#121212").grid(row=0, column=0, padx=5)

ttk.Label(
    fe_row,
    textvariable=player1_foul,
    width=3,
    anchor="center"
).grid(row=0, column=1)
tk.Button(fe_row, text="+", width=3,
          command=lambda: change_stat(player1_ext, 1)).grid(row=1, column=3)


tk.Button(fe_row, text="+", width=3,
          command=lambda: change_stat(player1_foul, 1)).grid(row=0, column=2)

tk.Button(fe_row, text="Reset", width=6,
          command=lambda: reset_stat(player1_foul, 0)).grid(row=0, column=3, padx=5)


tk.Label(fe_row, text="Ext:", fg="white", bg="#121212").grid(row=1, column=0, padx=5, pady=5)

ttk.Label(fe_row, textvariable=player1_ext, width=3, anchor="center").grid(row=1, column=1)

tk.Button(fe_row, text="-", width=3,
          command=lambda: change_stat(player1_ext, -1, minimum=0)).grid(row=1, column=2)



# ---------- CENTER CONTROL ----------
mid = ttk.Frame(bottom, style="Card.TFrame", padding=10)
mid.pack(side="left", padx=10)

center_label_var = tk.StringVar()

label_entry = ttk.Entry(
    mid,
    justify="center",
    width=30,
    textvariable=center_label_var
)
label_entry.pack(fill="x", pady=5)
ttk.Label(mid, text="Label", style="Label.TLabel").pack()
def switch_sides():
    # Swap team names
    temp_team = left_team_name_var.get()
    left_team_name_var.set(team_name_var.get())
    team_name_var.set(temp_team)

    # Swap player list names
    for i in range(6):
        temp = left_player_vars[i].get()
        left_player_vars[i].set(player_vars[i].get())
        player_vars[i].set(temp)

    # Swap selected player names
    p1 = player1_name_var.get()
    p2 = player2_name_var.get()
    player1_name_var.set(p2)
    player2_name_var.set(p1)

    # Swap scores
    s1 = player1_score.get()
    s2 = player2_score.get()
    player1_score.set(s2)
    player2_score.set(s1)

    # Swap fouls
    f1 = player1_foul.get()
    f2 = player2_foul.get()
    player1_foul.set(f2)
    player2_foul.set(f1)

    # Swap extension
    e1 = player1_ext.get()
    e2 = player2_ext.get()
    player1_ext.set(e2)
    player2_ext.set(e1)

    manual_update()

switch_btn = tk.Button(mid, text="<- Switch ->", command=switch_sides)
switch_btn.pack(pady=5)
tk.Button(mid, text="Reset Score",
      command=reset_all_scores).pack(pady=5)
auto_update_var = tk.BooleanVar(value=False)

def auto_update_trigger(*args):
    if auto_update_var.get():
        manual_update()

tk.Checkbutton(
    mid,
    text="Auto Update",
    fg="white",
    bg="#121212",
    selectcolor="#121212",
    variable=auto_update_var
).pack(pady=5)
def manual_update():
    update_obs_player_names()
    save_scores_to_obs()
    save_foul_ext_to_obs()
    save_center_label()

update_btn = tk.Button(
    mid,
    text="UPDATE",
    font=("Arial", 18, "bold"),
    bg="#BDBDBD",
    command=manual_update
)
update_btn.pack(pady=10, fill="x")


# ---------- PLAYER 2 ----------
p2 = ttk.Frame(bottom, style="Card.TFrame", padding=10)
p2.pack(side="left", fill="x", expand=True, padx=10)

ttk.Label(
    p2,
    text="Player 2",
    style="Title.TLabel"
).pack(anchor="center")

name_row2 = tk.Frame(p2, bg="#121212")
name_row2.pack(pady=5)

name_row2.columnconfigure(0, weight=0)
name_row2.columnconfigure(1, weight=0)

ttk.Label(
    name_row2,
    text="Name:",
    style="Label.TLabel"
).grid(row=0, column=0, sticky="e", padx=(0, 8))

player2_name_var = tk.StringVar()

nick2 = ttk.Entry(
    name_row2,
    width=24,
    textvariable=player2_name_var
)
nick2.grid(row=0, column=1, sticky="w")


score_row2 = tk.Frame(p2, bg="#121212")
score_row2.pack(pady=10)

tk.Button(score_row2, text="-", width=4,
      command=lambda: change_score(player2_score, -1)).pack(side="left")

ttk.Label(score_row2,
      textvariable=player2_score,
      font=("Arial", 32, "bold"),
      background="#121212",
      foreground="white").pack(side="left", padx=10)

tk.Button(score_row2, text="+", width=4,
      command=lambda: change_score(player2_score, 1)).pack(side="left")

#foul and ext player 2
fe_row2 = tk.Frame(p2, bg="#121212")
fe_row2.pack(pady=10)

tk.Label(fe_row2, text="Foul:", fg="white", bg="#121212").grid(row=0, column=0, padx=5)

ttk.Label(
    fe_row2,
    textvariable=player2_foul,
    width=3,
    anchor="center"
).grid(row=0, column=1)


tk.Button(fe_row2, text="+", width=3,
          command=lambda: change_stat(player2_foul, 1)).grid(row=0, column=2)

tk.Button(fe_row2, text="Reset", width=6,
          command=lambda: reset_stat(player2_foul, 0)).grid(row=0, column=3, padx=5)


tk.Label(fe_row2, text="Ext:", fg="white", bg="#121212").grid(row=1, column=0, padx=5, pady=5)

ttk.Label(fe_row2, textvariable=player2_ext, width=3, anchor="center").grid(row=1, column=1)

tk.Button(fe_row2, text="-", width=3,
          command=lambda: change_stat(player2_ext, -1, minimum=0)).grid(row=1, column=2)
tk.Button(fe_row2, text="+", width=3,
          command=lambda: change_stat(player2_ext, 1)).grid(row=1, column=3)

# player name update for obs.
def update_obs_player_names():
    with open("obs_player1.txt", "w", encoding="utf-8") as f:
        f.write(player1_name_var.get())

    with open("obs_player2.txt", "w", encoding="utf-8") as f:
        f.write(player2_name_var.get())
# ================= AUTO UPDATE BINDINGS =================

player1_name_var.trace_add("write", auto_update_trigger)
player2_name_var.trace_add("write", auto_update_trigger)
center_label_var.trace_add("write", auto_update_trigger)

player1_score.trace_add("write", auto_update_trigger)
player2_score.trace_add("write", auto_update_trigger)

player1_foul.trace_add("write", auto_update_trigger)
player2_foul.trace_add("write", auto_update_trigger)

player1_ext.trace_add("write", auto_update_trigger)
player2_ext.trace_add("write", auto_update_trigger)

# ================== RUN ==================
load_left_team_data()
load_team_data()
save_scores_to_obs()
save_foul_ext_to_obs()
save_center_label()
root.mainloop()
