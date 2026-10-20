import os
import sys

import requests

CHECK_URL = "https://www.playstation.com/de-at/ps5/ps5-pro/buy-now/"
BUY_URL = "https://direct.playstation.com/de-at/buy-consoles/playstation5-pro-console-2-tb"
TOPIC = os.environ["NTFY_TOPIC"]

UNAVAILABLE_MARKERS = ["XXXTEST"]
PAGE_OK_MARKER = "PlayStation®5 Pro Konsole"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "de-AT,de;q=0.9",
}


def notify(title, message):
    requests.post(
        f"https://ntfy.sh/{TOPIC}",
        data=message.encode("utf-8"),
        headers={
            "Title": title,
            "Priority": "urgent",
            "Tags": "video_game,tada",
            "Click": BUY_URL,
        },
        timeout=15,
    )


r = requests.get(CHECK_URL, headers=HEADERS, timeout=20)
print("HTTP", r.status_code)
if r.status_code != 200 or PAGE_OK_MARKER not in r.text:
    print("Seite nicht auswertbar, überspringe.")
    sys.exit(0)

if any(m in r.text for m in UNAVAILABLE_MARKERS):
    print("Noch nicht verfügbar.")
else:
    print("VERFÜGBAR!")
    notify(
        "PS5 Pro ist verfügbar!",
        "Die PS5 Pro 2 TB wird im PlayStation Direct Shop (AT) nicht mehr als "
        "nicht erhältlich angezeigt. Schnell zuschlagen!",
    )
