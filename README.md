# Monitor-Refresh-Rate-Switcher
A lightweight Windows tray utility to quickly switch your monitor refresh rate between **60 Hz** and **144 Hz** (or more if you add them).  
The current refresh rate is shown directly on the tray icon, with different colors per rate.

<img width="329" height="60" alt="Immagine 2025-09-14 142839" src="https://github.com/user-attachments/assets/c5189678-f92e-4bc5-a210-fa6a3cd798a0" />

<img width="430" height="110" alt="Screenshot 2025-09-14 142905" src="https://github.com/user-attachments/assets/2cea7dd3-2194-4d14-8789-bc6b61da32ce" />


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
4. Taskbar behavior is limited by Windows 11 design: the icon may start in the overflow menu until you pin it visible manually. For this I highly recommend [ExplorerPatcher](https://github.com/valinet/ExplorerPatcher) so it's always visible.

---

## 🛠 Build from source
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

The refresh rate will change even if your monitor doesn't support it, without warning.

Only affects the primary monitor.
