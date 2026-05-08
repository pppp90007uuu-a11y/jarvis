from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import scraper
import voice_gen
import image_gen
import video_gen
import ai_engine
import asyncio
import os
import uuid
import threading
import time

app = Flask(__name__)
CORS(app)

# Configuration
STATIC_VIDEO_DIR = "static/videos"
ASSETS_AUDIO_DIR = "assets/audio"
ASSETS_IMAGES_DIR = "assets/images"

# Ensure directories exist
for d in [STATIC_VIDEO_DIR, ASSETS_AUDIO_DIR, ASSETS_IMAGES_DIR]:
    os.makedirs(d, exist_ok=True)

# Global Job Management
jobs_status = {} # { job_id: { "status": str, "headline": str, "video_url": str, "script": str, "progress": int } }

def video_worker(job_id, headline, lang, niche):
    try:
        jobs_status[job_id]["status"] = "Generating Script..."
        jobs_status[job_id]["progress"] = 20
        script = ai_engine.generate_ai_script(headline, niche, lang)
        jobs_status[job_id]["script"] = script

        jobs_status[job_id]["status"] = "Generating Voice..."
        jobs_status[job_id]["progress"] = 40
        audio_path = os.path.join(ASSETS_AUDIO_DIR, f"{job_id}.mp3")
        voice_name = "hi-IN-MadhurNeural" if lang == 'hi' else "en-US-GuyNeural"
        asyncio.run(voice_gen.generate_voice(script, voice_name, audio_path))

        jobs_status[job_id]["status"] = "Generating Image..."
        jobs_status[job_id]["progress"] = 60
        image_path = os.path.join(ASSETS_IMAGES_DIR, f"{job_id}.png")
        image_gen.create_text_image(headline, image_path)

        jobs_status[job_id]["status"] = "Assembling Video..."
        jobs_status[job_id]["progress"] = 80
        video_filename = f"{job_id}.mp4"
        video_path = os.path.join(STATIC_VIDEO_DIR, video_filename)
        video_gen.assemble_video(image_path, audio_path, video_path)

        jobs_status[job_id]["status"] = "Completed"
        jobs_status[job_id]["progress"] = 100
        jobs_status[job_id]["video_url"] = f"/static/videos/{video_filename}"

    except Exception as e:
        print(f"Job {job_id} failed: {e}")
        jobs_status[job_id]["status"] = f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/trends')
def trends():
    news = scraper.get_tech_news()
    return jsonify(news)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    headlines = data.get('headlines', [])
    lang = data.get('lang', 'hi')
    niche = data.get('niche', 'Tech News')

    if not headlines:
        return jsonify({"error": "Headlines are required"}), 400

    job_ids = []
    for headline in headlines:
        job_id = str(uuid.uuid4())
        job_ids.append(job_id)

        jobs_status[job_id] = {
            "status": "In Queue",
            "headline": headline,
            "progress": 0,
            "lang": lang,
            "niche": niche,
            "created_at": time.time()
        }

        # Start worker thread
        thread = threading.Thread(target=video_worker, args=(job_id, headline, lang, niche))
        thread.start()

    return jsonify({"success": True, "job_ids": job_ids})

@app.route('/api/status', methods=['GET'])
def get_status():
    # Return all jobs created in the last 1 hour to keep it clean
    current_time = time.time()
    active_jobs = {jid: info for jid, info in jobs_status.items() if current_time - info.get("created_at", 0) < 3600}
    return jsonify(active_jobs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
