-------------- Overview------------------------

This Scoreboard Software is a complete basketball game management tool designed for professional and semi-professional use.
It provides a clean, intuitive GUI for controlling game timers, player scores, fouls, and team management. It integrates 
seamlessly with OBS for live broadcasting, allowing real-time updates of scores, player information, and center labels.

Perfect for sports broadcasters, coaches, and tournament organizers who want a reliable digital scoreboard solution.

-----------Key Features--------------------
Team Management

Add Team Names and Player Names for both left and right teams.

Supports 7 players per team with a "Select" button to assign the active player.

Auto-save player data to left_team.txt and right_team.txt.

Switch sides with a single click (<– Switch ->) to handle team rotations.

Timer & Shot Clock

Customizable start game time, shot duration, extension seconds, and alert times.

Dual display:

Main control panel

Fullscreen Shot Clock Display Window for OBS or large screens.

Color-coded alerts:

Normal color and Alert color can be customized.

Sound alerts configurable with .wav files.

Full start/pause/reset/extension controls.

Hotkeys

Fully customizable hotkeys for:

Start Game

Start Timer

Pause Timer

Reset Timer

Add Extension

Special key support (space, enter, escape, arrow keys, function keys).

Hotkey mode locks editing for safe gameplay control.

Score, Foul & Extension Management

Adjust Player 1 and Player 2 scores (+/- buttons).

Track fouls and extensions for each player.

Auto-save to OBS-compatible text files:

obs_player1_score.txt, obs_player2_score.txt

obs_player1_foul.txt, obs_player2_foul.txt

obs_player1_ext.txt, obs_player2_ext.txt

Display fouls as black dots (●) for visual clarity.

Center Label Control

Editable center label for game announcements or scores.

Updates OBS in real-time (obs_center_label.txt).

Auto-update functionality with a single click or checkbox toggle.


GUI & Usability

Dark-themed Tkinter interface with clean, professional layout.

Editable fields and buttons grouped logically for intuitive use.

Full lock/unlock editing mode for game operation or setup.

-----------------System Requirements-----------------------------

Windows 10/11 recommended

Python 3.10+

Tkinter, winsound (standard Python library)

Resolution: 1920x1080 or higher recommended for display window

____________Installation_______________________________________

Download the software files.

Ensure Python 3.10+ is installed.

Run main.py (or your main script).

Optional: Place .wav files for alerts in a dedicated folder.


___________________________How to Use_____________________________

Enter team names and player names for both teams.

Configure timer settings (start time, shot duration, extension, alert).

Customize normal and alert colors and alert sound if needed.

Use hotkeys or GUI buttons to control the timer during gameplay.

Update scores, fouls, and extensions live.

Enable Auto Update to push data directly to OBS files.

Use Switch Sides for halftime or team rotation.

_____________________________Files Generated / Used______________________________

left_team.txt, right_team.txt → Stores team and player info

obs_player1.txt, obs_player2.txt → Active player names for OBS

obs_player1_score.txt, obs_player2_score.txt → Player scores

obs_player1_foul.txt, obs_player2_foul.txt → Fouls as dots

obs_player1_ext.txt, obs_player2_ext.txt → Player extensions

obs_center_label.txt → Center label for OBS


Shotclock 1.1 version

## 🔄 Update – Foul & Extension Display Customization

### ✨ New Feature

Added customizable display options for **Fouls** and **Extensions** in the settings panel.

### ⚙️ What’s New

Users can now choose how values are displayed in OBS:

* **Foul Display Mode**

  * `Dots (●●●)` – visual indicator style
  * `Number (1, 2, 3...)` – standard numeric format

* **Extension Display Mode**

  * `Number (1, 2, 3...)`
  * `Dots (●●●)`

### 🎮 How to Use

1. Open the software
2. Click the ⚙ (Settings) button
3. Select your preferred display mode
4. Click **Save**

### 📺 OBS Integration

The selected format will automatically update the following files:

* `obs_player1_foul.txt`
* `obs_player2_foul.txt`
* `obs_player1_ext.txt`
* `obs_player2_ext.txt`

### 🚀 Benefits

* Flexible display for different leagues (FIBA, streetball, etc.)
* Better visual clarity for livestreams
* Customizable scoreboard style

---

📞 Support

For setup or usage assistance, contact: Carter Carig
Email: cartercarig@gmail.com
