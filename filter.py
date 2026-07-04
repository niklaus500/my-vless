from urllib.parse import unquote
import os
import re

INPUT = "vless.txt"
OUTPUT = "output/vless.txt"

MAX = 80

# کشورهای خوب برای گیم
GOOD_REGIONS = [
    "germany", "de",
    "netherlands", "nl",
    "france", "fr",
    "finland", "fi",
    "turkey", "tr",
]

BAD_REGIONS = [
    "usa", "us", "china", "cn", "india", "in", "russia", "ru", "brazil", "br"
]

def is_valid(v):
    return v.startswith("vless://") and "@" in v and len(v) > 60

def get_name(v):
    try:
        if "#" in v:
            return unquote(v.split("#", 1)[1]).lower()
    except:
        pass
    return ""

def score(v):
    s = 0
    name = get_name(v)

    # Reality / WS bonuses
    if "reality" in v.lower():
        s += 3
    if "ws" in v.lower() or "websocket" in v.lower():
        s += 2

    # Good regions
    if any(r in name for r in GOOD_REGIONS):
        s += 2

    # Bad regions penalty
    if any(r in name for r in BAD_REGIONS):
        s -= 3

    # fallback quality hints
    if "security=tls" in v.lower():
        s += 1

    return s


with open(INPUT, "r", encoding="utf-8") as f:
    lines = [x.strip() for x in f if x.strip()]

# فقط معتبرها
lines = [l for l in lines if is_valid(l)]

# حذف تکراری‌ها
seen = set()
unique = []
for l in lines:
    if l not in seen:
        seen.add(l)
        unique.append(l)

# امتیازدهی
scored = [(score(l), l) for l in unique]
scored.sort(reverse=True, key=lambda x: x[0])

# انتخاب بهترین‌ها
result = [x[1] for x in scored[:MAX]]

os.makedirs("output", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result))
