import tkinter as tk
from tkinter import ttk

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
    
ttk.Label(left_team, text="Team", style="Title.TLabel").pack(anchor="w")
ttk.Entry(left_team, width=25).pack(pady=5)

ttk.Label(left_team, text="Player's Name", style="Label.TLabel").pack(anchor="w", pady=(10, 5))

for _ in range(5):
    row = tk.Frame(left_team, bg="#121212")
    row.pack(fill="x", pady=4)
    tk.Button(row, text="Select", width=8).pack(side="left")
    ttk.Entry(row).pack(side="left", padx=5, fill="x", expand=True)

# ---------- CENTER TIMER ----------
center = ttk.Frame(top, style="Card.TFrame", padding=10)
center.pack(side="left", expand=True, fill="both", padx=10)

ttk.Label(center, text="40", foreground="#FFFFFF", background="#121212",
          font=("Arial", 48, "bold")).pack()

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

color_row = tk.Frame(center, bg="#121212")
color_row.pack(pady=5)
ttk.Label(color_row, text="Normal Color:", style="Label.TLabel").pack(side="left")
ttk.Entry(color_row, width=10).pack(side="left", padx=5)
tk.Button(color_row, text="Select").pack(side="left")

color_row2 = tk.Frame(center, bg="#121212")
color_row2.pack(pady=5)
ttk.Label(color_row2, text="Alert Color:", style="Label.TLabel").pack(side="left")
ttk.Entry(color_row2, width=10).pack(side="left", padx=5)
tk.Button(color_row2, text="Select").pack(side="left")

alert_row = tk.Frame(center, bg="#121212")
alert_row.pack(pady=10)
tk.Checkbutton(alert_row, text="Enable Alert", fg="white",
               bg="#121212", selectcolor="#121212").pack(side="left")
tk.Button(alert_row, text="Select").pack(side="left", padx=5)

controls = tk.Frame(center, bg="#121212")
controls.pack(pady=10)
for text in ["Start Game(G)", "Start(S)", "Pause(P)", "Reset(S)", "Extention(Space)"]:
    tk.Button(controls, text=text).pack(side="left", padx=5)

# ---------- RIGHT TEAM ----------
right_team = ttk.Frame(top, style="Card.TFrame", padding=10)
right_team.pack(side="left", fill="y", padx=10)

ttk.Label(right_team, text="Team", style="Title.TLabel").pack(anchor="w")
ttk.Entry(right_team, width=25).pack(pady=5)

ttk.Label(right_team, text="Player's Name", style="Label.TLabel").pack(anchor="w", pady=(10, 5))

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

ttk.Label(p1, text="Player 1", style="Title.TLabel").pack(anchor="w")

name_row1 = tk.Frame(p1, bg="#121212")
name_row1.pack(anchor="w", pady=5)

ttk.Label(name_row1, text="Name:", style="Label.TLabel", width=6).pack(side="left", padx=(0, 5))
nick1 = ttk.Entry(name_row1, width=18)
nick1.pack(side="left")


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
p2 = ttk.Frame(bottom, style="Card.TFrame", padding=10)
p2.pack(side="left", fill="x", expand=True, padx=10)

ttk.Label(p2, text="Player 2", style="Title.TLabel").pack(anchor="w")
name_row2 = tk.Frame(p2, bg="#121212")
name_row2.pack(anchor="w", pady=5)

ttk.Label(name_row2, text="Name:", style="Label.TLabel", width=6).pack(side="left", padx=(0, 5))
nick2 = ttk.Entry(name_row2, width=18)
nick2.pack(side="left")



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
