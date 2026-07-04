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
# MEMORY
# -------------------
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

# -------------------
# REAL (light) latency check
# -------------------
def latency_test():
    start = time.time()
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect(("1.1.1.1", 53))
        s.close()
    except:
        return 9999
    return (time.time() - start) * 1000


with open(INPUT, "r", encoding="utf-8") as f:
    lines = [x.strip() for x in f if x.strip()]

# keep valid only
lines = [l for l in lines if valid(l)]

# remove duplicates
seen = set()
unique = []
for l in lines:
    if l not in seen:
        seen.add(l)
        unique.append(l)

# -------------------
# FIXED TEST POOL (NO RANDOM)
# -------------------
test_pool = unique[:min(30, len(unique))]

real_score = {}

for v in test_pool:
    real_score[v] = -latency_test() / 1000

ranked = []

for v in unique:
    n = name(v)

    score = memory.get(v, 0)

    # region logic (soft)
    if any(g in n for g in GOOD):
        score += 2

    if any(b in n for b in BAD):
        score -= 2

    # real test boost
    if v in real_score:
        score += real_score[v]
        memory[v] = min(memory.get(v, 0) + 2, 20)
    else:
        score += 0.2

    # stability penalty
    if memory.get(v, 0) < -5:
        score -= 2

    ranked.append((score, v))

# sort best first
ranked.sort(key=lambda x: x[0], reverse=True)

result = [v for _, v in ranked[:MAX]]

os.makedirs("output", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result))

save()
