# FIXED pull_all.py — Auto-pulls all 25 layers — No manual entry
import requests, os, json, hashlib, yaml, time
from pathlib import Path

BASE = "https://justicefornolanwells.com"
HEADERS = {"User-Agent": "JusticeForNolanWells-Bot/1.0"}

print("Starting auto-pull...")

# 1. Make sure forensic folder exists
Path("forensic").mkdir(exist_ok=True)
Path("forensic/evidence_files").mkdir(exist_ok=True, parents=True)

# 2. Read your sources.yaml — this has all your sources
try:
    sources = yaml.safe_load(open("sources.yaml", encoding="utf-8"))
    print(f"Loaded sources.yaml with {len(sources)} entries")
except:
    sources = {}
    print("No sources.yaml found, will create from 25 layers")

# 3. THE 25 LAYERS WE MAPPED — auto-pull each one
LAYERS = [
    "/", "/evidence-archive", "/case-summary", "/witness-claim-ledger",
    "/reconstruction-lab", "/account-order-story", "/documents-archive",
    "/drift-lab", "/video-archive", "/plunder-source-archive",
    "/dispatch-audio-timeline", "/information-chain-review",
    "/body-recovery-record", "/ucn-report-review", "/social-source-ledger",
    "/facebook-research-audit", "/last-contact-matrix", "/contradictions",
    "/missing-evidence-tracker", "/coordinate-explorer", "/question-tracker",
    "/people-connections", "/boats", "/timeline-gaps", "/methodology",
    "/llms.txt", "/llms-full.txt"
]

all_layers = {}
for path in LAYERS:
    try:
        url = BASE + path if not path.startswith("/llms") else BASE + path
        if path in ["/llms.txt", "/llms-full.txt"]:
            url = BASE + path
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            all_layers[path] = {
                "url": url,
                "status": "OK",
                "length": len(r.text),
                "sha256": hashlib.sha256(r.text.encode()).hexdigest()
            }
            # Save each layer as file so you can see it
            safe_name = path.strip("/").replace("/", "_") or "home"
            open(f"forensic/{safe_name}.html", "w", encoding="utf-8").write(r.text)
            print(f"✓ Pulled {path}")
        else:
            print(f"✗ Failed {path} {r.status_code}")
        time.sleep(1) # be nice to server
    except Exception as e:
        print(f"✗ Error {path}: {e}")

# 4. Save master manifest — this proves what we pulled and when
json.dump(all_layers, open("forensic/manifest.json", "w", encoding="utf-8"), indent=2)

# 5. Save coordinates we mapped — Layer 19
coords = [
    {"name":"Northwest Horn Island recovery ref","lat":30.242014,"lon":-88.778409},
    {"name":"El Camino Real Road","lat":30.433343,"lon":-88.848426},
    {"name":"Horn Island west tip","lat":30.243508,"lon":-88.777755},
    {"name":"MI4088BU slow movement","lat":30.288414,"lon":-88.790442},
    {"name":"Garmin anchor","lat":30.243767,"lon":-88.777150},
    {"name":"Sea Tow caller","lat":30.244733,"lon":-88.779833},
]
json.dump(coords, open("forensic/coordinates.json","w"), indent=2)

print(f"\nDONE — Pulled {len(all_layers)} layers into /forensic/")
print("Check forensic/manifest.json for proof")
