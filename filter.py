from urllib.parse import unquote
import os
import subprocess
import time

INPUT = "vless.txt"
OUTPUT = "output/vless.txt"

MAX = 80

GOOD = ["germany", "netherlands", "france", "finland", "turkey"]
BAD = ["usa", "us", "china", "cn", "india", "ru", "russia", "brazil"]

def valid(v):
    return v.startswith("vless://") and "@" in v and len(v) > 60

def name(v):
    try:
        if "#" in v:
            return unquote(v.split("#",1)[1]).lower()
    except:
        pass
    return ""

def latency(v):
    # تست سبک (proxy check سریع)
    start = time.time()
    try:
        subprocess.run(
            ["bash", "-c", f"curl -s --max-time 2 '{v[:50]}'"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
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

for v in unique:
    n = name(v)
    score = 0

    if any(g in n for g in GOOD):
        score += 2

    if any(b in n for b in BAD):
        score -= 3

    score -= latency(v) / 1000

    ranked.append((score, v))

ranked.sort(reverse=True, key=lambda x: x[0])

result = [x[1] for x in ranked[:MAX]]

os.makedirs("output", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result))
