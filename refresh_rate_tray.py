import win32api
import win32con
import pystray
from PIL import Image, ImageDraw, ImageFont
import threading
import ctypes

# Assign Windows AppID (important for Win11 tray recognition)
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.hellmiau.refresh_rate")


# ----------------- Monitor functions -----------------
def get_refresh_rate():
    """Get current monitor refresh rate, rounded to nearest standard value (60 or 144)."""
    devmode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
    freq = round(devmode.DisplayFrequency)
    if abs(freq - 60) <= 1:
        return 60
    elif abs(freq - 144) <= 1:
        return 144
    return freq

def set_refresh_rate(rate):
    """Set primary monitor refresh rate."""
    devmode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
    devmode.DisplayFrequency = rate
    devmode.Fields = win32con.DM_PELSHEIGHT | win32con.DM_PELSWIDTH | win32con.DM_DISPLAYFREQUENCY
    win32api.ChangeDisplaySettings(devmode, 0)

# ----------------- Tray icon -----------------
def create_icon_text(text, color):
    img = Image.new("RGB", (32, 32), (0, 0, 0))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arialbd.ttf", 20)  # bold font
    except:
        font = ImageFont.load_default()

    bbox = d.textbbox((0,0), text, font=font)
    w = bbox[2]-bbox[0]
    h = bbox[3]-bbox[1]

    while (w>32 or h>32) and getattr(font, "size", 12)>5:
        font = ImageFont.truetype("arialbd.ttf", getattr(font, "size", 20)-1)
        bbox = d.textbbox((0,0), text, font=font)
        w = bbox[2]-bbox[0]
        h = bbox[3]-bbox[1]

    d.text(((32-w)/2,(32-h)/2), text, font=font, fill=color)
    return img

# ----------------- Tray menu -----------------
def run_tray():
    icon = pystray.Icon("refresh_rate")

    def update_icon():
        while True:
            rate = get_refresh_rate()
            color = "green" if rate == 60 else "lightblue" if rate == 144 else "white"
            icon.icon = create_icon_text(str(rate), color)
            icon.title = f"{rate} Hz"
            threading.Event().wait(1)

    def make_menu():
        return pystray.Menu(
            pystray.MenuItem(
                "60 Hz",
                lambda _: set_refresh_rate(60),
                checked=lambda item: get_refresh_rate()==60
            ),
            pystray.MenuItem(
                "144 Hz",
                lambda _: set_refresh_rate(144),
                checked=lambda item: get_refresh_rate()==144
            ),
            pystray.MenuItem("Quit", lambda _: icon.stop())
        )

    icon.menu = make_menu()
    threading.Thread(target=update_icon, daemon=True).start()
    icon.run()

# ----------------- Main -----------------
if __name__ == "__main__":
    run_tray()
