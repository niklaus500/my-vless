from urllib.parse import urlparse, parse_qs, unquote

INPUT = "vless.txt"
OUTPUT = "output/vless.txt"

ALLOW = [
    "Germany", "DE",
    "Netherlands", "NL",
    "Finland", "FI",
    "Turkey", "TR",
    "France", "FR",
    "Singapore", "SG"
]

seen = set()
result = []

with open(INPUT, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line.startswith("vless://"):
            continue
        if line in seen:
            continue
        seen.add(line)

        try:
            name = unquote(line.split("#", 1)[1]) if "#" in line else ""
        except:
            name = ""

        if any(x.lower() in name.lower() for x in ALLOW):
            result.append(line)

import os
os.makedirs("output", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result))
