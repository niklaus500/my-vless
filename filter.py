from urllib.parse import unquote
import os
import random

INPUT = "vless.txt"
OUTPUT = "output/vless.txt"

MAX = 80

def is_valid(v):
    return v.startswith("vless://") and "@" in v and len(v) > 50

def decode_name(v):
    try:
        if "#" in v:
            return unquote(v.split("#",1)[1]).lower()
    except:
        pass
    return ""

with open(INPUT, "r", encoding="utf-8") as f:
    lines = [x.strip() for x in f if x.strip()]

# فقط vless های سالم
lines = [l for l in lines if is_valid(l)]

# حذف تکراری
seen = set()
unique = []
for l in lines:
    if l not in seen:
        seen.add(l)
        unique.append(l)

epodonios = []
barry = []

for l in unique:
    if "epodonios" in l.lower():
        epodonios.append(l)
    else:
        barry.append(l)

random.shuffle(epodonios)
random.shuffle(barry)

half = MAX // 2

result = epodonios[:half] + barry[:half]

# اگر کم بود جبران
rest = [x for x in unique if x not in result]
random.shuffle(rest)
result += rest[:MAX - len(result)]

os.makedirs("output", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result))
