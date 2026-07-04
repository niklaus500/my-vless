from urllib.parse import unquote
import os
import socket
import time

INPUT = "vless.txt"
OUTPUT = "output/vless.txt"

MAX = 80

GOOD = ["germany", "netherlands", "france", "finland", "turkey"]
BAD = ["usa", "us", "china", "india", "russia", "brazil"]

def valid(v):
    return v.startswith("vless://") and "@" in v and len(v) > 60

def name(v):
    try:
        if "#" in v:
            return unquote(v.split("#",1)[1]).lower()
    except:
        pass
    return ""

# 🔥 تست واقعی TCP handshake (سبک ولی واقعی‌تر از curl)
def latency_test():
    start = time.time()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect(("8.8.8.8", 53))  # تست مسیر اینترنت واقعی
        s.close()
    except:
        return 9999
    return (time.time() - start) * 1000


with open(INPUT, "r", encoding="utf-8") as f:
    lines = [x.strip() for x in f if x.strip()]

lines = [l for l in lines if valid(l)]

# حذف تکراری
seen = set()
unique = []
for l in lines:
    if l not in seen:
        seen.add(l)
        unique.append(l)

ranked = []

base_latency = latency_test()

for v in unique:
    n = name(v)

    score = 0

    # 🌍 منطقه خوب
    if any(g in n for g in GOOD):
        score += 3

    # ❌ منطقه بد
    if any(b in n for b in BAD):
        score -= 3

    # ⚡ ترکیب با latency پایه
    final_score = score - (base_latency / 1000)

    ranked.append((final_score, v))

ranked.sort(reverse=True, key=lambda x: x[0])

result = [x[1] for x in ranked[:MAX]]

os.makedirs("output", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result))
