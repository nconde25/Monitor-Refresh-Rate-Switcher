import win32api
import win32con
import pystray
from PIL import Image, ImageDraw, ImageFont
import threading
import ctypes

# Assign Windows AppID (important for Win11 tray recognition)
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.hellmiau.refresh_rate")

# ----------------- Monitor functions -----------------
REFRESH_RATES = [60, 75, 120, 144, 165, 240, 360]
COLOR_MAP = {
    60: "green",
    75: "lime",
    120: "cyan",
    144: "lightblue",
    165: "magenta",
    240: "orange",
    360: "red"
}

def get_refresh_rate():
    """Get current monitor refresh rate."""
    devmode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
    return round(devmode.DisplayFrequency, 1)

def normalize_rate(freq):
    """Normalize frequency to nearest standard value within 1 Hz."""
    for standard in REFRESH_RATES:
        if abs(freq - standard) <= 1:
            return standard
    return round(freq)

def set_refresh_rate(rate):
    """Set primary monitor refresh rate."""
    devmode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
    devmode.DisplayFrequency = rate
    devmode.Fields = win32con.DM_PELSHEIGHT | win32con.DM_PELSWIDTH | win32con.DM_DISPLAYFREQUENCY
    win32api.ChangeDisplaySettings(devmode, 0)

def is_rate_supported(rate):
    i = 0
    while True:
        try:
            devmode = win32api.EnumDisplaySettings(None, i)
        except:
            break
        if devmode.DisplayFrequency == rate:
            return True
        i += 1
    return False

# ----------------- Tray icon -----------------
def create_icon_text(text, color):
    img = Image.new("RGB", (32, 32), (0, 0, 0))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arialbd.ttf", 20)
    except:
        font = ImageFont.load_default()

    bbox = d.textbbox((0,0), text, font=font)
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]

    while (w>32 or h>32) and getattr(font, "size", 12) > 5:
        font = ImageFont.truetype("arialbd.ttf", getattr(font, "size", 20)-1)
        bbox = d.textbbox((0,0), text, font=font)
        w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]

    d.text(((32-w)/2, (32-h)/2), text, font=font, fill=color)
    return img

# ----------------- Tray menu -----------------
def run_tray():
    icon = pystray.Icon("refresh_rate")

    # Detect unsupported rates at startup
    supported_rates = {r: is_rate_supported(r) for r in REFRESH_RATES}

    # Update tray icon every second
    def update_icon():
        while True:
            rate = normalize_rate(get_refresh_rate())
            color = COLOR_MAP.get(rate, "white")
            icon.icon = create_icon_text(str(rate), color)
            threading.Event().wait(1)

    # Correctly create menu items with closure for each refresh rate
    def make_menu():
        def create_item(r):
            if supported_rates[r]:
                return pystray.MenuItem(
                    f"{r} Hz",
                    lambda _: set_refresh_rate(r),
                    checked=lambda item: normalize_rate(get_refresh_rate()) == r
                )
            else:
                # Greyed out / strikethrough for unsupported
                return pystray.MenuItem(
                    f"{r} Hz (unsupported)",
                    None,
                    enabled=False
                )

        items = [create_item(r) for r in REFRESH_RATES]
        items.append(pystray.MenuItem("Quit", lambda _: icon.stop()))
        return pystray.Menu(*items)

    icon.menu = make_menu()
    threading.Thread(target=update_icon, daemon=True).start()
    icon.run()

# ----------------- Main -----------------
if __name__ == "__main__":
    run_tray()
