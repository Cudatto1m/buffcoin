import requests
import time
import re
from datetime import datetime

RAW_COOKIE = "cf_clearance=LXidC1oZTfrv5GXnwdWu7p57li5k0PQFMJdzAEMoNEI-1769866055-1.2.1.1-vMhJWdUfrK7e22_K8LW7qct3vYrMOaPJHz1DyxWZi9tL.POvmNphRFqp9GGALqQa79pDwsfMFVd1VftrQPmv40GRZefTtePFIN9cENTWdBrNPIEG7JSf6lW0Mpqm2kd1j94omdhySV9VDSpEoyfm4hbgYRDYfNgsZb51WQuaxu2xu.iYGnIwF85vJt2uwktNWIs.NN6mb4jttxTWNKne7hZnc8g.RY.ZaHjh4Cadlt6NZbO_zBkzXIoMuBmZbrk1; jexactyl_session=eyJpdiI6Iithd3QyblBYUUpkM0ZkWWdsNGFSWFE9PSIsInZhbHVlIjoidU5MZUNOVE9CV2cyNGd3QUZta2kvYlQ1STZCNDQ3MWtkS0FTWEVsWWdSQ1E0R1NISzJsTEZxSVlxR0FDdW02and6V3ptZ0NRSDVFY1RaWVkwaC9lSloxdVk4WlJ6WE8rQ3FwZXhaQkw1elhBRktZNzFWckc1Y25ibjZZWG5qMlMiLCJtYWMiOiJjMjc4NGZlMjUzN2UzMmE2YzBmMGNjOGU0NTE5MWE4ZmYxZDlkOWE0ODQ4MjgxZmRjZTMyYzQzZjNkNWY4ODI0IiwidGFnIjoiIn0%3D; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IjNQeXZWOGNZazB0TitQaDN0ZVhkdGc9PSIsInZhbHVlIjoiMGU4TlVPL3hnQm03MkpnMjRCeThQeHFFSWpMaE9TZVgrd2VGeGZGdGVTT0JzOGI3UGRMZ2JHTml6TFhBSzBXdTRzTDl2SlI5M3lsV0lyNlJJc2NHVWMzUzh0R2JUeWxIcm1wRmZEQ0kyQW85MkpjaldVUW96L3VRRXgzUjE4clQ5T1NuL1NVY0lZRnRSL0x5K1J5Q0VBUTNQSjNNdG5rVkZUVEhzUEJLMkozRmJhQVZ3aGJMbitBOHNqV0xXVHFuRHM0akVPZUhCWHI5THhRRXVuenl4VHo0YTczT3ZSZzNMNWJzcTVTUGFxVT0iLCJtYWMiOiJlYTEwODcxNTlkNzA0OTYzNDI3YWZjYzZlMGUwMDA5MzBiYmQyYmYxODQ2YWY0NTc5OTg1OGFlODlmMDAzZTdhIiwidGFnIjoiIn0%3D; XSRF-TOKEN=eyJpdiI6IkdzdjA2N2VpMWxEVHlCcDFlR2tQWVE9PSIsInZhbHVlIjoiYVRGeWZ6NG4ycE53b3Zkam45THgycExTNS81RS9kY2drc3F6cEdtY3ByL2Y1RE5EZGJXVVM4QzdOaVdxd1JnaG1XZFRhZVZHWjR6UHhUdlVTbGhaOTNsWEFtWWNCTVpUYWtvanR4WFZsYVM5Qysxc0JFU3p4M011dzhUYjBNbDMiLCJtYWMiOiI2ZDlhY2JiZWUxMTA0YmI2MGQ3ZjBhODg0NzI0NGExN2VjYmIwMmNjNmE3ZjM2YTc0NWE4ZWUxNmI2NGYwNWFmIiwidGFnIjoiIn0%3D"

URL = "https://panel.orihost.com/api/client/store/earn"

def extract_xsrf(cookie_str):
    """Tự động trích xuất XSRF-TOKEN từ chuỗi cookie"""
    match = re.search(r'XSRF-TOKEN=([^;]+)', cookie_str)
    if match:
        from urllib.parse import unquote
        return unquote(match.group(1))
    return None

def start_afk():
    xsrf_token = extract_xsrf(RAW_COOKIE)
    
    if not xsrf_token:
        print("❌ Lỗi: Không tìm thấy XSRF-TOKEN trong Cookie!")
        return

    session = requests.Session()
    
    headers = {
        "Accept": "application/json",
        "Content-Length": "0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "X-XSRF-TOKEN": xsrf_token,
        "Cookie": RAW_COOKIE,
        "Origin": "https://panel.orihost.com",
        "Referer": "https://panel.orihost.com/store"
    }

    total_earned = 0
    attempt = 1
    
    print(f"--- AFK ORIHOST BOT ---")
    print(f"[*] Đã nhận diện XSRF-TOKEN: {xsrf_token[:20]}...")

    while True:
        now = datetime.now().strftime("%H:%M:%S")
        try:
            response = session.post(URL, headers=headers, timeout=15)
            
            if response.status_code in [200, 204]:
                total_earned += 3
                print(f"[{now}] Lần {attempt}: +3 C thành công! (Tổng: {total_earned} C)")
            
            elif response.status_code == 419:
                print(f"[{now}] ❌ Lỗi 419: Token hết hạn. Hãy copy Cookie mới từ trình duyệt.")
                break
                
            elif response.status_code == 429:
                print(f"[{now}] ⚠️ Lỗi 429: Rate Limit (Quá nhanh). Nghỉ 60s...")
                time.sleep(60)
                continue
                
            else:
                print(f"[{now}] ❗ Lỗi {response.status_code}: {response.text[:50]}")

            attempt += 1
            time.sleep(61)

        except Exception as e:
            print(f"[{now}] 🌐 Lỗi kết nối: {e}")
            time.sleep(20)

if __name__ == "__main__":
    start_afk()