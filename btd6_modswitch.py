import sys
import shutil
import os
from pathlib import Path

# Paths
GAME_DIR = Path(r"D:\Steam\steamapps\common\BloonsTD6")
# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.resolve()
# Backup directory will be created next to the script
BACKUP_DIR = SCRIPT_DIR / "ModsBackup"

# Official Steam App ID for Bloons TD 6
APP_ID = "960090"

# Files and folders related to modding
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
    # Presence of version.dll indicates the game is modded
    return (GAME_DIR / "version.dll").exists()

def set_state(target_state):
    # Ensure backup directory exists
    BACKUP_DIR.mkdir(exist_ok=True)
    current_state = "modded" if is_currently_modded() else "clean"
    
    if target_state == current_state:
        print(f"Status: Game is already {target_state.upper()}. No changes required.")
        return

    if target_state == "clean":
        print("Action: Switching to CLEAN (Vanilla) state...")
        for item in MOD_ITEMS:
            src = GAME_DIR / item
            dst = BACKUP_DIR / item
            if src.exists():
                shutil.move(str(src), str(dst))
                
    elif target_state == "modded":
        print("Action: Switching to MODDED state...")
        for item in MOD_ITEMS:
            src = BACKUP_DIR / item
            dst = GAME_DIR / item
            if src.exists():
                shutil.move(str(src), str(dst))

def launch_game():
    print("Action: Launching Bloons TD 6 via Steam...")
    # Call Steam protocol to launch the game
    os.system(f"start steam://rungameid/{APP_ID}")

if __name__ == "__main__":
    # Argument validation
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