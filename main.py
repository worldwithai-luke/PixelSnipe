import os
import time
import keyboard
import pyautogui
from termcolor import colored
from pixelsnipe import Pixelsnipe

# Settings
TOGGLE_KEY = 'F1'  # Key to toggle aimbot on/off
XFOV = 280  # X-Axis Field of View
YFOV = 150  # Y-Axis Field of View
INGAME_SENSITIVITY = 1
FLICKSPEED = 1.07437623 * (INGAME_SENSITIVITY ** -0.9936827126)  # Calculate flick speed
MOVESPEED = 1 / (6 * INGAME_SENSITIVITY)  # Calculate move speed

monitor = pyautogui.size()
CENTER_X, CENTER_Y = monitor.width // 2, monitor.height // 2

def print_ui(pixelsnipe):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
    status = 'Enabled' if pixelsnipe.toggled else 'Disabled'
    status_color = 'green' if pixelsnipe.toggled else 'red'
    
    # Title with ASCII banner
    print(colored("╔══════════════════════════════════════╗", 'magenta'))
    print(colored("║           🌟 Pixel Snipe 🌟          ║", 'magenta'))
    print(colored("║                 v2.0                 ║", 'magenta'))
    print(colored("╚══════════════════════════════════════╝", 'magenta'))
    print()

    # Status Section
    print(colored("┌──[ 🎯 STATUS ]──────────────────────────────┐", 'cyan'))
    print(colored(f"│ Aimbot: {colored(status, status_color)}", 'white') + " " * (44 - len(f"Aimbot: {status}")) + "│")
    print(colored(f"│ FOV: {XFOV}x{YFOV} | Sensitivity: {INGAME_SENSITIVITY:.2f}", 'white') + " " * (44 - len(f"FOV: {XFOV}x{YFOV} | Sensitivity: {INGAME_SENSITIVITY:.2f}")) + "│")
    print(colored("└─────────────────────────────────────────────┘", 'cyan'))
    print()

    # Features & Controls Section
    print(colored("┌──[ ⚙️ FEATURES & CONTROLS ]─────────────────┐", 'cyan'))
    print(colored(f"│ {colored(TOGGLE_KEY, 'magenta')}  Toggle Aimbot (Track Purple enemies)", 'white') + " " * (21 - len(f"{TOGGLE_KEY}  Toggle Aimbot")) + "│")
    print(colored(f"│ {colored('F2', 'magenta')}  Show/Hide Detection Window", 'white') + " " * (44 - len("F2  Show/Hide Detection Window")) + "│")
    print(colored(f"│ {colored('RightMB', 'magenta')}  Aimbot (Aim at closest enemy)", 'white') + " " * (21 - len("RightMB  Aimbot")) + "│")
    print(colored(f"│ {colored('Alt', 'magenta')}  Triggerbot (Auto-click on target)", 'white') + " " * (21 - len("Alt  Triggerbot")) + "│")
    print(colored(f"│ {colored('LeftMB', 'magenta')}  Recoil Compensation", 'white') + " " * (44 - len("LeftMB  Recoil Compensation")) + "│")
    print(colored("└─────────────────────────────────────────────┘", 'cyan'))
    print()

    # Info Section
    print(colored("┌──[ ℹ️ INFO ]────────────────────────────────┐", 'cyan'))
    print(colored(f"│ GitHub: \033[4mhttps://github.com/pixelsnipe\033[0m", 'white') + " " * (44 - len("GitHub: https://github.com/pixelsnipe")) + "│")
    print(colored(f"│ Created by: {colored('Jiho Lee', 'magenta')}", 'white') + " " * (44 - len("Created by: Jiho Lee")) + "│")
    print(colored("└─────────────────────────────────────────────┘", 'cyan'))

def main():
    os.system('title Pixelsnipe')
    pixelsnipe = Pixelsnipe(CENTER_X - XFOV // 2, CENTER_Y - YFOV // 2, XFOV, YFOV, FLICKSPEED, MOVESPEED)
    
    try:
        while True:
            if keyboard.is_pressed(TOGGLE_KEY):
                pixelsnipe.toggle()
                print_ui(pixelsnipe)
                time.sleep(0.2)  # Debounce key press
            else:
                print_ui(pixelsnipe)
            time.sleep(0.1)  # Update UI less frequently to reduce flicker
    except (KeyboardInterrupt, SystemExit):
        print(colored('\n[Info]', 'green'), colored('Exiting...', 'white') + '\n')
    finally:
        pixelsnipe.close()

if __name__ == '__main__':
    main()