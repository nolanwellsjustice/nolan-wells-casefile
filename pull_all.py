import os, yaml, json, re
from datetime import datetime

print("=== NOLAN WELLS FORENSIC ENGINE V2 ===")

# Load sources
with open('sources.yaml','r') as f:
    sources = yaml.safe_load(f)

os.makedirs('evidence/interviews', exist_ok=True)
os.makedirs('evidence/videos', exist_ok=True)
os.makedirs('evidence/reports', exist_ok=True)
os.makedirs('evidence/audio', exist_ok=True)
os.makedirs('forensic', exist_ok=True)

timeline = []
contradictions = []
discrepancies = []

# Baseline verified events from your case (from justicefornolanwells.com)
timeline.append({"time":"11:14 AM July 4","event":"Official GPS Arrival - MI4088BU Horn Island west tip","source":"GPS Log","verified":"YES"})
timeline.append({"time":"11:30:33 AM","event":"Alternate Ride Request - JCSO dispatched to check mainland launches - Negative contact","source":"Dispatch","verified":"YES"})
timeline.append({"time":"4:31 PM","event":"MDMR Movement Marker - Vessel position change detected offshore","source":"MDMR/GPS","verified":"YES"})
timeline.append({"time":"4:48 PM","event":"Sea Tow Distress Call - Triton distress: sinking, bilge pump failure - Caller Jerry Atkerson","source":"Sea Tow Audio","verified":"YES"})
timeline.append({"time":"5:52-6:06 PM","event":"Fort Bayou Excursion - GPS shows movement","source":"GPS Track","verified":"YES"})

contradictions.append({
 "title":"ALTERNATE RIDE: UNCONFIRMED",
 "details":"Dispatch 11:30 AM request, negative 12:21 PM. No vehicle/vessel ID. Contradicts early working theory.",
 "sources":["Dispatch","JCSO Log"]
})
contradictions.append({
 "title":"1:55 PM SCENE TIMING",
 "details":"Counsel letter cites 1:55 PM for three-boat cluster. No native timestamp available. Conflicts with GPS chain 11:14 arrival + 4:31 movement. ~2hr41min gap unresolved.",
 "sources":["Counsel Letter","GPS"]
})
contradictions.append({
 "title":"VESSEL POSITION CHANGE",
 "details":"Shoreline position claimed fixed until 4:00 PM per initial statement. GPS data shows movement at 4:31 PM.",
 "sources":["Initial Statement","GPS"]
})

discrepancies.extend([
 "Chain of Custody: No native photo/video metadata for 1:55 PM scene",
 "Registration IDs: Boats in cluster not independently verified",
 "Communications: 4:48 PM call lacks membership number confirmation",
 "Movement: 5:52-6:06 PM Fort Bayou not captured in initial shoreline account"
])

# Process sources.yaml links (placeholders for auto-pull)
for cat, items in sources.items():
    if isinstance(items, list):
        for it in items:
            url = it.get('url') if isinstance(it, dict) else it
            if url and 'EXAMPLE' not in url:
                print(f"Would pull: {cat} - {url}")
                # Here: youtube_transcript_api, newspaper3k, pdfminer would run
                timeline.append({"time":"From Source","event":f"{cat}: {url}","source":url,"verified":"NEEDS REVIEW"})

# Save forensic outputs
with open('forensic/master_timeline.json','w') as f:
    json.dump(timeline, f, indent=2)
with open('forensic/contradictions.json','w') as f:
    json.dump(contradictions, f, indent=2)
with open('forensic/discrepancies.json','w') as f:
    json.dump(discrepancies, f, indent=2)

print(f"Saved {len(timeline)} events, {len(contradictions)} contradictions, {len(discrepancies)} discrepancies")
print("V2 Engine ready — now add your real YouTube / news / MDMR links to sources.yaml")
