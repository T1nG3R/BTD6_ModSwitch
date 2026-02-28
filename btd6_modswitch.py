import sys
import shutil
import os
from pathlib import Path

# Paths
# You can change GAME_DIR if the game is installed on another drive
GAME_DIR = Path(r"D:\Steam\steamapps\common\BloonsTD6")
SCRIPT_DIR = Path(__file__).parent.resolve()
BACKUP_DIR = SCRIPT_DIR / "ModBackup"

# Dynamically get the AppData/Roaming path for any Windows user
APPDATA_PATH = os.getenv('APPDATA')
if not APPDATA_PATH:
    print("Error: Could not locate APPDATA environment variable.")
    sys.exit(1)

# Universal Shortcut Paths
SHORTCUT_DIR = Path(APPDATA_PATH) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Steam"
SHORTCUT_VANILLA = SHORTCUT_DIR / "Bloons TD 6.url"
SHORTCUT_MODDED = SHORTCUT_DIR / "Bloons TD 6 Modded.url"

# Official Steam App ID for Bloons TD 6
APP_ID = "960090"

MOD_ITEMS = [
    "Btd6ModHelper",
    "MelonLoader",
    "Mods",
    "Plugins",
    "UserData",
    "UserLibs",
    "version.dll"
]

def is_currently_modded():
    indicators = ["Mods", "MelonLoader", "version.dll"]
    return any((GAME_DIR / item).exists() for item in indicators)

def update_shortcut(target_state):
    # Failsafe: only try to rename if the shortcut directory actually exists
    if not SHORTCUT_DIR.exists():
        return

    if target_state == "clean":
        if SHORTCUT_MODDED.exists():
            SHORTCUT_MODDED.rename(SHORTCUT_VANILLA)
    elif target_state == "modded":
        if SHORTCUT_VANILLA.exists():
            SHORTCUT_VANILLA.rename(SHORTCUT_MODDED)

def set_state(target_state):
    BACKUP_DIR.mkdir(exist_ok=True)
    current_state = "modded" if is_currently_modded() else "clean"
    
    if target_state == current_state:
        print(f"Status: Game is already {target_state.upper()}. No changes required.")
        update_shortcut(target_state)
        return

    if target_state == "clean":
        print("Action: Switching to CLEAN (Vanilla) state...")
        for item in MOD_ITEMS:
            src = GAME_DIR / item
            dst = BACKUP_DIR / item
            if src.exists():
                shutil.move(str(src), str(dst))
        update_shortcut("clean")
                
    elif target_state == "modded":
        print("Action: Switching to MODDED state...")
        for item in MOD_ITEMS:
            src = BACKUP_DIR / item
            dst = GAME_DIR / item
            if src.exists():
                shutil.move(str(src), str(dst))
        update_shortcut("modded")

def launch_game():
    print("Action: Launching Bloons TD 6 via Steam...")
    os.system(f"start steam://rungameid/{APP_ID}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["clean", "modded"]:
        print("Error: Invalid or missing argument. Use 'clean' or 'modded'.")
        sys.exit(1)
        
    target = sys.argv[1]
    try:
        set_state(target)
        launch_game()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")