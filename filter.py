from urllib.parse import unquote
import os
import json
import socket
import time

INPUT = "vless.txt"
OUTPUT = "output/vless.txt"
CACHE = "ai_cache.json"

MAX = 80

GOOD = ["germany", "netherlands", "france", "finland", "turkey"]
BAD = ["usa", "us", "china", "india", "russia", "brazil"]

# -------------------
# حافظه AI
# -------------------
if os.path.exists(CACHE):
    with open(CACHE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

def save_memory():
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

# تست سبک latency (برای گیم)
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

base_latency = latency_test()

ranked = []

for v in unique:
    n = name(v)

    # امتیاز قبلی (یادگیری)
    score = memory.get(v, 0)

    # region bonus
    if any(g in n for g in GOOD):
        score += 3

    if any(b in n for b in BAD):
        score -= 3

    # latency penalty
    score -= base_latency / 1000

    # یادگیری
    if score > 2:
        memory[v] = min(memory.get(v, 0) + 1, 10)
    else:
        memory[v] = max(memory.get(v, 0) - 1, -10)

    ranked.append((score, v))

ranked.sort(reverse=True, key=lambda x: x[0])

result = [x[1] for x in ranked[:MAX]]

os.makedirs("output", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result))

save_memory()
