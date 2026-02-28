import sys
import shutil
import os
import winreg
from pathlib import Path

# Script and Backup Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
BACKUP_DIR = SCRIPT_DIR / "ModBackup"

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

def find_game_directory():
    try:
        # Get Steam root path from Windows Registry
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        steam_path_str, _ = winreg.QueryValueEx(key, "SteamPath")
        winreg.CloseKey(key)
        
        steam_path = Path(steam_path_str)
        vdf_path = steam_path / "steamapps" / "libraryfolders.vdf"
        
        # Check default Steam library first
        default_game_path = steam_path / "steamapps" / "common" / "BloonsTD6"
        if default_game_path.exists():
            return default_game_path
            
        # Parse libraryfolders.vdf for other drives
        if vdf_path.exists():
            with open(vdf_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if '"path"' in line.lower():
                        parts = line.split('"')
                        if len(parts) >= 4:
                            # Fix double backslashes from VDF formatting
                            lib_path_str = parts[3].replace('\\\\', '\\')
                            game_path = Path(lib_path_str) / "steamapps" / "common" / "BloonsTD6"
                            if game_path.exists():
                                return game_path
    except Exception as e:
        print(f"Warning: Failed to auto-detect Steam directory: {e}")
        
    return None

def get_shortcut_dir():
    appdata_path = os.getenv('APPDATA')
    if not appdata_path:
        return None
    return Path(appdata_path) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Steam"

def is_currently_modded(game_dir):
    indicators = ["Mods", "MelonLoader", "version.dll"]
    return any((game_dir / item).exists() for item in indicators)

def update_shortcut(target_state):
    shortcut_dir = get_shortcut_dir()
    if not shortcut_dir or not shortcut_dir.exists():
        return

    shortcut_vanilla = shortcut_dir / "Bloons TD 6.url"
    shortcut_modded = shortcut_dir / "Bloons TD 6 Modded.url"

    if target_state == "clean":
        if shortcut_modded.exists():
            shortcut_modded.rename(shortcut_vanilla)
    elif target_state == "modded":
        if shortcut_vanilla.exists():
            shortcut_vanilla.rename(shortcut_modded)

def set_state(target_state, game_dir):
    BACKUP_DIR.mkdir(exist_ok=True)
    current_state = "modded" if is_currently_modded(game_dir) else "clean"
    
    if target_state == current_state:
        print(f"Status: Game is already {target_state.upper()}. No changes required.")
        update_shortcut(target_state)
        return

    print(f"Action: Switching to {target_state.upper()} state...")
    for item in MOD_ITEMS:
        if target_state == "clean":
            src = game_dir / item
            dst = BACKUP_DIR / item
        else: # modded
            src = BACKUP_DIR / item
            dst = game_dir / item
            
        if src.exists():
            shutil.move(str(src), str(dst))
            
    update_shortcut(target_state)

def launch_game():
    print("Action: Launching Bloons TD 6 via Steam...")
    os.system(f"start steam://rungameid/{APP_ID}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["clean", "modded"]:
        print("Error: Invalid or missing argument. Use 'clean' or 'modded'.")
        sys.exit(1)
        
    target = sys.argv[1]
    
    game_dir = find_game_directory()
    if not game_dir:
        print("Error: Could not locate Bloons TD 6 installation directory automatically.")
        input("Press Enter to exit...")
        sys.exit(1)
        
    print(f"Info: Found game directory at '{game_dir}'")
    
    try:
        set_state(target, game_dir)
        launch_game()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")