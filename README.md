# BTD6 ModSwitch

A lightweight utility for Bloons TD 6 that lets you seamlessly switch between vanilla and modded game states. This prevents your main account from being flagged while allowing you to easily manage MelonLoader and Btd6ModHelper installations.

## Features
* **Instant Toggling:** Moves mod files to an isolated backup folder instantly without heavy read/write operations.
* **1-Click Execution:** Includes `.bat` files for quick state switching and game launching.
* **Interactive CLI:** Run the Python script directly for an interactive terminal menu.
* **Auto-Path Detection:** Automatically locates your Steam installation of Bloons TD 6 via the Windows Registry.
* **Dynamic Shortcut Renaming:** Updates your Start Menu/Desktop shortcut name to reflect the current game state (e.g., "Bloons TD 6 Modded").
* **Drift Detection:** Scans the game directory upon launch and alerts you to any unknown files that are neither standard vanilla files nor recognized mod files.

## Prerequisites
* Windows OS
* Python 3.x installed
* Bloons TD 6 installed via Steam

## Installation
1.  Download or clone this repository to your local drive. It is recommended to place it on the same drive as your Steam installation for instant file moving.
2.  Install MelonLoader and your desired mods into your Bloons TD 6 directory as usual.
3.  Ensure the `.bat` files and `btd6_modswitch.py` are in the same folder.

## Usage
Use the provided batch files to manage your game state:

* **Manager_Menu.bat:** Opens the interactive command-line interface.
* **Play_Vanilla.bat:** Disables all mods and launches the clean version of the game.
* **Play_Modded.bat:** Restores all mods and launches the modded version of the game.
* **Enable_Mods.bat:** Restores mod files without launching the game.
* **Disable_Mods.bat:** Hides mod files without launching the game.

## How It Works
The script checks for indicators like `version.dll`, `MelonLoader`, and `Mods`. When switching to the vanilla state, it safely moves these mod-related files and folders into a local `ModBackup` directory located next to the script. When switching back, it restores them to the game folder.