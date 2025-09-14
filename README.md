# Monitor-Refresh-Rate-Switcher
A lightweight Windows tray utility to quickly switch your monitor refresh rate between **60 Hz** and **144 Hz** (or more if you add them).  
The current refresh rate is shown directly on the tray icon, with different colors per rate.

<img width="329" height="60" alt="Immagine 2025-09-14 142839" src="https://github.com/user-attachments/assets/c5189678-f92e-4bc5-a210-fa6a3cd798a0" />

<img width="447" height="247" alt="Screenshot 2025-09-14 155054" src="https://github.com/user-attachments/assets/9ea8a821-a4f5-4ac4-8713-6fae1681d8fd" />



---

## Features
- Small tray app (no console window)
- Detects your current refresh rate on startup
- One-click switching between refresh rates
- Tray icon dynamically updates (text and color)
- Works on Windows 10 and 11

---

## Installation
1. Download the latest release from [Releases](../../releases) (or build it yourself, see below).
2. Run the `.exe`. It will appear in your system tray (near the clock).
3. Right-click the tray icon to switch between available refresh rates.

## Anti-virus flag, whitelist.
The .exe is not signed by Micro$oft. It may be detected as evil. It's harmless, If you have doubts check the [refresh_rate_tray.py](https://github.com/nconde25/Monitor-Refresh-Rate-Switcher/blob/main/refresh_rate_tray.py) and compile your own (steps below) else simply add it as an exception on windows defender or your anti virus of choice. For windows Defender:

1. Open the Windows Defender Security Center
2. Click on "Virus & threat protection"
3. Click on "Virus & threat protection settings"
4. Scroll down and click on "Add or remove exclusions"
5. Click on "Add an exclusion"
6. Click on "File" and select the program or your start folder (see below).


## Run at Start Up
i recommend putting this on your start folder so it runs with when windows boot.
1. Win+R
2. search for > `shell:startup`
3. Copy the exe in that folder

# Windows 11, Always Visible fix.
- Taskbar behavior is limited by Windows 11 design: the icon may start in the overflow menu until you pin it visible manually. For this I highly recommend [ExplorerPatcher](https://github.com/valinet/ExplorerPatcher) so it's always visible.

---

## Build from source
You’ll need:
- [Python 3.12+](https://www.python.org/)
- [PyInstaller](https://pyinstaller.org/)
- Dependencies: `pip install pystray pillow pywin32`

Build with:

```powershell
pyinstaller --onefile --noconsole --icon="hz.ico" refresh_rate_tray.py
```
The final executable will be in the dist/ folder.

## Adding More Refresh Rates

By default the app supports 60 Hz and 144 Hz.
To add another refresh rate (e.g. 120 Hz):

Open refresh_rate_tray.py in a text editor.

Find the make_menu() function:

```Python
def make_menu():
    return pystray.Menu(
        pystray.MenuItem(
            "60 Hz",
            lambda _: switch_rate(60),
            checked=lambda _: get_refresh_rate() == 60
        ),
        pystray.MenuItem(
            "144 Hz",
            lambda _: switch_rate(144),
            checked=lambda _: get_refresh_rate() == 144
        ),
        pystray.MenuItem("Quit", lambda _: icon.stop())
    )

```
Add another block for 120 Hz:
```Python
pystray.MenuItem(
    "120 Hz",
    lambda _: switch_rate(120),
    checked=lambda _: get_refresh_rate() == 120
),
```

Save and rebuild with PyInstaller.

## Notes

The refresh rate will NOT change if your monitor doesn't support it or it couldn't do it.

Only affects the primary monitor.
