import os, json
from datetime import datetime
import yt_dlp

# FULL AUTO-HUNT — 30 QUERIES — NO LINKS NEEDED FROM YOU
QUERIES = [
    "Officer Tatum Nolan Wells",
    "Officer Tatum Jackson County Sheriff Nolan Wells",
    "Nolan Wells Horn Island interview",
    "Nolan Wells friend interview",
    "Nolan Wells friend WLOX",
    "Nolan Wells friend WXXV",
    "Nolan Wells WLOX news",
    "Nolan Wells WXXV 25",
    "Nolan Wells Sun Herald",
    "Nolan Wells family interview",
    "Nolan Wells mom interview",
    "Nolan Wells dad interview",
    "Horn Island July 4 Nolan Wells",
    "Horn Island search Nolan Wells",
    "Horn Island boat Nolan Wells",
    "Nolan Wells Mississippi missing boat",
    "Nolan Wells Jackson County search",
    "Nolan Wells Sea Tow",
    "Nolan Wells boat sinking",
    "Nolan Wells Fort Bayou",
    "Nolan Wells July 4 2026",
    "Justice for Nolan Wells",
    "Nolan Wells update",
    "Nolan Wells press conference",
    "Nolan Wells sheriff interview",
]

os.makedirs("forensic/youtube", exist_ok=True)
all_videos = []

opts = {'quiet': True, 'skip_download': True, 'noplaylist': True}

print("=== HUNTER V4 FULL PULL ===")
for q in QUERIES:
    try:
        print(f"HUNTING: {q}")
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(f"ytsearch15:{q}", download=False)
            for e in info.get('entries', []):
                if not e: continue
                v = {
                    "id": e.get('id'),
                    "title": e.get('title'),
                    "channel": e.get('uploader') or e.get('channel'),
                    "url": f"https://www.youtube.com/watch?v={e.get('id')}",
                    "query_match": q,
                    "upload_date": e.get('upload_date'),
                    "description": (e.get('description') or "")[:1000],
                    "thumbnail": e.get('thumbnail')
                }
                if not any(x['id']==v['id'] for x in all_videos):
                    all_videos.append(v)
    except Exception as ex:
        print(f"Fail {q}: {ex}")

# Keep verified case data so we don't lose contradictions/discrepancies
verified = {
    "timeline": [
        {"time": "11:14 AM July 4", "event": "GPS Arrival MI4088BU Horn Island", "verified": True},
        {"time": "11:30 AM", "event": "Alternate Ride Request — JCSO check — Negative", "verified": True},
        {"time": "4:31 PM", "event": "Vessel Movement detected", "verified": True},
        {"time": "4:48 PM", "event": "Sea Tow Distress — Jerry Atkerson — bilge pump failure", "verified": True},
        {"time": "5:52-6:06 PM", "event": "Fort Bayou Transit", "verified": True},
    ],
    "contradictions": [
        {"id": 1, "title": "Alternate Ride UNCONFIRMED", "detail": "Dispatch 11:30 AM negative at 12:21 PM, no vehicle identified"},
        {"id": 2, "title": "1:55 PM Scene Timing", "detail": "Counsel letter cites 1:55 PM three-boat cluster — no native timestamp metadata — conflicts with 11:14 arrival"},
        {"id": 3, "title": "Vessel Position Change", "detail": "Claimed fixed until 4 PM — GPS shows movement 4:31 PM"},
    ],
    "discrepancies": [
        "Chain of Custody: No native photo/video metadata for 1:55 PM scene",
        "Registration IDs: Boats in cluster not independently verified",
        "Communications: 4:48 PM Sea Tow call lacks membership confirmation",
        "Movement: Fort Bayou 5:52-6:06 not in initial shoreline account",
        "MDMR report: Awaiting official PDF export",
        "Scanner audio: Dispatch + Sea Tow original files needed"
    ]
}

with open("forensic/evidence.json","w",encoding="utf-8") as f:
    json.dump({"videos": all_videos, "total": len(all_videos), "generated_at": str(datetime.now()), "verified": verified}, f, indent=2)

with open("forensic/master_timeline.json","w",encoding="utf-8") as f:
    json.dump(verified, f, indent=2)

with open("forensic/contradictions.json","w",encoding="utf-8") as f:
    json.dump(verified["contradictions"], f, indent=2)

print(f"DONE V4: {len(all_videos)} total videos")
