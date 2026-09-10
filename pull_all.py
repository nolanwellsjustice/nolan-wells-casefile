import os, json, re, requests, yaml
from datetime import datetime
import yt_dlp

# QUERIES THE SCRIPT WILL HUNT FOR ON ITS OWN
YOUTUBE_QUERIES = [
    "Officer Tatum Nolan Wells interview",
    "Nolan Wells Horn Island interview",
    "Nolan Wells friend interview WLOX",
    "Nolan Wells friend interview WXXV",
    "Nolan Wells family interview news",
    "Nolan Wells Sun Herald interview",
    "Nolan Wells Horn Island July 4th video",
    "Horn Island search team Nolan Wells",
    "Nolan Wells Mississippi missing",
    "Jackson County Sheriff Nolan Wells"
]

MDMR_QUERIES = [
    "https://dmr.ms.gov",
    "MDMR Nolan Wells report PDF"
]

os.makedirs("forensic/youtube", exist_ok=True)
os.makedirs("forensic/reports", exist_ok=True)

all_videos = []
all_transcripts = []

ydl_opts = {
    'quiet': True,
    'skip_download': True,
    'extract_flat': False,
    'noplaylist': True,
}

print("=== AUTO-HUNTER V3 STARTING ===")

for query in YOUTUBE_QUERIES:
    try:
        search = f"ytsearch15:{query}"
        print(f"\nHUNTING: {query}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search, download=False)
            for entry in info.get('entries', []):
                if not entry: continue
                vid = {
                    "id": entry.get('id'),
                    "title": entry.get('title'),
                    "channel": entry.get('uploader') or entry.get('channel'),
                    "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
                    "upload_date": entry.get('upload_date'),
                    "description": (entry.get('description') or "")[:1000],
                    "query_match": query,
                    "thumbnail": entry.get('thumbnail')
                }
                # Avoid duplicates
                if not any(v['id']==vid['id'] for v in all_videos):
                    all_videos.append(vid)
                    print(f" FOUND: {vid['title'][:80]}")
                    
                    # Try transcript
                    try:
                        from youtube_transcript_api import YouTubeTranscriptApi
                        transcript = YouTubeTranscriptApi.get_transcript(vid['id'])
                        text = " ".join([t['text'] for t in transcript])
                        all_transcripts.append({
                            "video_id": vid['id'],
                            "video_title": vid['title'],
                            "url": vid['url'],
                            "transcript": text[:15000],
                            "query": query
                        })
                        with open(f"forensic/youtube/{vid['id']}.json","w", encoding="utf-8") as f:
                            json.dump({"video": vid, "transcript": text}, f, indent=2)
                    except Exception as e:
                        print(f"  no transcript: {e}")
                        with open(f"forensic/youtube/{vid['id']}.json","w", encoding="utf-8") as f:
                            json.dump({"video": vid, "transcript": ""}, f, indent=2)
    except Exception as e:
        print(f"Error hunting {query}: {e}")

# Try MDMR / Scanner placeholders - will save what it finds
try:
    print("\nHUNTING: MDMR reports")
    # This will be expanded as official reports surface
    r = requests.get("https://dmr.ms.gov", timeout=10)
    with open("forensic/reports/mdmr_portal_check.json","w") as f:
        json.dump({"checked": str(datetime.now()), "status": r.status_code}, f, indent=2)
except Exception as e:
    print(f"MDMR check failed: {e}")

# MASTER OUTPUTS
master = {
    "generated_at": str(datetime.now()),
    "total_videos_found": len(all_videos),
    "queries_used": YOUTUBE_QUERIES,
    "videos": all_videos
}

with open("forensic/master_timeline.json","w", encoding="utf-8") as f:
    json.dump(master, f, indent=2)

with open("forensic/evidence.json","w", encoding="utf-8") as f:
    json.dump({"videos": all_videos, "transcripts": all_transcripts}, f, indent=2)

# Auto-build contradictions from transcripts
contradictions = []
for t in all_transcripts:
    txt = t['transcript'].lower()
    if "1:55" in txt or "one fifty five" in txt:
        contradictions.append({"video": t['video_title'], "url": t['url'], "issue": "Mentions 1:55 PM scene timing", "transcript_snippet": t['transcript'][:300]})
    if "alternate ride" in txt or "other boat" in txt or "different boat" in txt:
        contradictions.append({"video": t['video_title'], "url": t['url'], "issue": "Mentions alternate ride / other boat", "transcript_snippet": t['transcript'][:300]})

with open("forensic/contradictions.json","w", encoding="utf-8") as f:
    json.dump(contradictions, f, indent=2)

print(f"\n=== DONE: {len(all_videos)} videos, {len(all_transcripts)} transcripts ===")
