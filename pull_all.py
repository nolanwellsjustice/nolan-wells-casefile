import os, json
from datetime import datetime
import yt_dlp

QUERIES = [
    "Officer Tatum Nolan Wells",
    "Nolan Wells friend interview WLOX",
    "Nolan Wells WXXV interview",
    "Nolan Wells Sun Herald",
    "Horn Island July 4 Nolan Wells",
    "Nolan Wells Mississippi search",
]

os.makedirs("forensic/youtube", exist_ok=True)

all_videos = []

opts = {
    'quiet': True,
    'skip_download': True,
    'noplaylist': True,
    'extract_flat': False,
}

print("=== AUTO-HUNTER STABLE START ===")

for q in QUERIES:
    try:
        print(f"HUNTING: {q}")
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(f"ytsearch10:{q}", download=False)
            for e in info.get('entries', []):
                if not e: continue
                v = {
                    "id": e.get('id'),
                    "title": e.get('title'),
                    "channel": e.get('uploader') or e.get('channel'),
                    "url": f"https://www.youtube.com/watch?v={e.get('id')}",
                    "query_match": q,
                    "thumbnail": e.get('thumbnail'),
                    "description": (e.get('description') or "")[:800]
                }
                if not any(x['id']==v['id'] for x in all_videos):
                    all_videos.append(v)
                    print(f"  FOUND: {v['title'][:70]}")
    except Exception as ex:
        print(f"Error on {q}: {ex}")

# Save master files
with open("forensic/evidence.json","w",encoding="utf-8") as f:
    json.dump({"videos": all_videos, "generated_at": str(datetime.now())}, f, indent=2)

with open("forensic/master_timeline.json","w",encoding="utf-8") as f:
    json.dump({"total": len(all_videos), "videos": all_videos}, f, indent=2)

with open("forensic/contradictions.json","w",encoding="utf-8") as f:
    json.dump([], f, indent=2)

print(f"DONE: {len(all_videos)} videos found")
