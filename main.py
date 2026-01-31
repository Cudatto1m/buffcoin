import requests
import time
import re
import os
from datetime import datetime
from urllib.parse import unquote

RAW_COOKIE = os.getenv("RAW_COOKIE")  # lấy từ GitHub Secrets
URL = "https://panel.orihost.com/api/client/store/earn"

def extract_xsrf(cookie_str):
    match = re.search(r'XSRF-TOKEN=([^;]+)', cookie_str)
    return unquote(match.group(1)) if match else None

def start_afk():
    if not RAW_COOKIE:
        print("❌ Không có RAW_COOKIE")
        return

    xsrf_token = extract_xsrf(RAW_COOKIE)
    if not xsrf_token:
        print("❌ Không tìm thấy XSRF-TOKEN")
        return

    session = requests.Session()
    headers = {
        "Accept": "application/json",
        "Content-Length": "0",
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "X-XSRF-TOKEN": xsrf_token,
        "Cookie": RAW_COOKIE,
        "Origin": "https://panel.orihost.com",
        "Referer": "https://panel.orihost.com/store"
    }

    total_earned = 0
    attempt = 1

    START_TIME = time.time()
    MAX_RUNTIME = 5 * 60 * 60 - 60  # 4h59p

    print("=== AFK ORIHOST BOT START ===")
    print(f"XSRF-TOKEN: {xsrf_token[:20]}...")

    while True:
        if time.time() - START_TIME > MAX_RUNTIME:
            print(f"⏹️ Hết 5 tiếng | Tổng cộng: {total_earned} C")
            break

        now = datetime.now().strftime("%H:%M:%S")

        try:
            r = session.post(URL, headers=headers, timeout=15)

            if r.status_code in (200, 204):
                total_earned += 3
                print(f"[{now}] Lần {attempt}: +3 C ✅ | Tổng: {total_earned} C")

            elif r.status_code == 419:
                print(f"[{now}] ❌ 419 Cookie hết hạn → dừng")
                break

            elif r.status_code == 429:
                print(f"[{now}] ⚠️ 429 Rate limit → nghỉ 60s")
                time.sleep(60)
                continue

            else:
                print(f"[{now}] ❗ {r.status_code}: {r.text[:80]}")

            attempt += 1
            time.sleep(61)

        except Exception as e:
            print(f"[{now}] 🌐 Lỗi mạng: {e}")
            time.sleep(20)

if __name__ == "__main__":
    start_afk()
