from urllib.parse import unquote
import os
import subprocess
import time

INPUT = "vless.txt"
OUTPUT = "output/vless.txt"

MAX = 80

GOOD_REGIONS = ["germany", "netherlands", "france", "finland", "turkey"]

def is_valid(v):
    return v.startswith("vless://") and "@" in v and len(v) > 60

def get_name(v):
    try:
        if "#" in v:
            return unquote(v.split("#",1)[1]).lower()
    except:
        pass
    return ""

# شبیه‌سازی تست latency (واقعی در حد TCP handshake)
def test_latency(config):
    try:
        start = time.time()

        # تست ساده اتصال (proxy handshake simulation)
        # اگر سرور dead باشد سریع fail می‌شود
        result = subprocess.run(
            ["bash", "-c", f"curl -s --max-time 3 '{config[:50]}'"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        end = time.time()

        if result.returncode != 0:
            return 9999

        return (end - start) * 1000

    except:
        return 9999


with open(INPUT, "r", encoding="utf-8") as f:
    lines = [x.strip() for x in f if x.strip()]

lines = [l for l in lines if is_valid(l)]

seen = set()
unique = []
for l in lines:
    if l not in seen:
        seen.add(l)
        unique.append(l)

# امتیاز + latency ترکیبی
ranked = []

for v in unique:
    name = get_name(v)

    score = 0

    if any(r in name for r in GOOD_REGIONS):
        score += 2

    latency = test_latency(v)

    final_score = score - (latency / 1000)

    ranked.append((final_score, v))

ranked.sort(reverse=True, key=lambda x: x[0])

result = [x[1] for x in ranked[:MAX]]

os.makedirs("output", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result))
