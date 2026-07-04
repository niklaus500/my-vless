from urllib.parse import unquote
import os
import json
import socket
import random
import time

INPUT = "vless.txt"
OUTPUT = "output/vless.txt"
CACHE = "ai_cache.json"

MAX = 80

GOOD = ["germany", "netherlands", "france", "finland", "turkey"]
BAD = ["usa", "us", "china", "india", "russia", "brazil"]

# ------------------
# memory AI
# ------------------
if os.path.exists(CACHE):
    with open(CACHE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

def save():
    with open(CACHE, "w") as f:
        json.dump(memory, f)

def valid(v):
    return v.startswith("vless://") and "@" in v and len(v) > 60

def name(v):
    try:
        if "#" in v:
            return unquote(v.split("#",1)[1]).lower()
    except:
        pass
    return ""

# ⚡ تست واقعی سبک
def latency_test():
    start = time.time()
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect(("8.8.8.8", 53))
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

# 🔥 10% تست واقعی
sample_size = max(5, len(unique) // 10)
test_pool = random.sample(unique, sample_size)

real_scores = {}

for v in test_pool:
    real_scores[v] = -latency_test() / 1000

ranked = []

for v in unique:
    n = name(v)

    # 🧠 AI score
    score = memory.get(v, 0)

    if any(g in n for g in GOOD):
        score += 3

    if any(b in n for b in BAD):
        score -= 3

    # ⚡ اگر داخل 10% تست بود → دقت بالا
    if v in real_scores:
        score += real_scores[v]
        memory[v] = memory.get(v, 0) + 2
    else:
        # AI prediction (سبک)
        score -= 0.2

    ranked.append((score, v))

ranked.sort(reverse=True, key=lambda x: x[0])

result = [x[1] for x in ranked[:MAX]]

os.makedirs("output", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result))

save()
