from urllib.parse import unquote
import os

INPUT = "vless.txt"
OUTPUT = "output/vless.txt"

MAX_CONFIGS = 80

ALLOW = [
    "Germany", "DE",
    "Netherlands", "NL",
    "Finland", "FI",
    "France", "FR",
    "Turkey", "TR",
    "United Arab Emirates", "UAE", "AE"
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

        if any(country.lower() in name.lower() for country in ALLOW):
            result.append(line)

result = result[:MAX_CONFIGS]

os.makedirs("output", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result))
