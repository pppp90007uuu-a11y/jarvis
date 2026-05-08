import requests
import os
import random

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

def fetch_visuals(keywords, count=3, media_type="video"):
    """
    Fetches free videos or images from Pexels.
    """
    if not PEXELS_API_KEY:
        print("Pexels API Key not found. Skipping download.")
        return []

    headers = {"Authorization": PEXELS_API_KEY}
    media_paths = []

    # Create temp directory
    temp_dir = "assets/temp_media"
    os.makedirs(temp_dir, exist_ok=True)

    for query in keywords[:2]: # Use first two keywords
        url = f"https://api.pexels.com/videos/search?query={query}&per_page={count}&orientation=landscape"
        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            videos = data.get("videos", [])
            for v in videos:
                # Get the best quality file
                files = v.get("video_files", [])
                if not files: continue

                # Filter for HD or mobile
                video_url = None
                for f in files:
                    if f.get("width") == 1920 or f.get("quality") == "hd":
                        video_url = f.get("link")
                        break
                if not video_url: video_url = files[0].get("link")

                # Download
                filename = f"vid_{v['id']}.mp4"
                path = os.path.join(temp_dir, filename)
                if not os.path.exists(path):
                    r = requests.get(video_url, stream=True)
                    with open(path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk: f.write(chunk)

                media_paths.append(path)
                if len(media_paths) >= count: break
        except Exception as e:
            print(f"Failed to fetch pexels: {e}")

    return media_paths

if __name__ == "__main__":
    # Test
    # print(fetch_visuals(["coding", "technology"]))
    pass
