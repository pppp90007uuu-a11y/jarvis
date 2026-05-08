from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import scraper
import voice_gen
import image_gen
import video_gen
import asyncio
import os
import uuid

app = Flask(__name__)
CORS(app)

# Configuration
STATIC_VIDEO_DIR = "static/videos"
ASSETS_AUDIO_DIR = "assets/audio"
ASSETS_IMAGES_DIR = "assets/images"

# Ensure directories exist
for d in [STATIC_VIDEO_DIR, ASSETS_AUDIO_DIR, ASSETS_IMAGES_DIR]:
    os.makedirs(d, exist_ok=True)

def generate_script(headline, lang):
    """
    Acts as the AI script writer.
    """
    if lang == 'hi':
        return f"नमस्ते दोस्तों! आज की बड़ी टेक न्यूज़ है: {headline}. यह खबर तकनीक की दुनिया में काफी हलचल मचा रही है। ऐसे ही और अपडेट्स के लिए हमारे चैनल को सब्सक्राइब करें।"
    else:
        return f"Hello everyone! Today's top tech news is: {headline}. This development is creating quite a buzz in the tech world. Stay tuned for more updates and don't forget to subscribe."

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
    headline = data.get('headline')
    lang = data.get('lang', 'hi')

    if not headline:
        return jsonify({"error": "Headline is required"}), 400

    job_id = str(uuid.uuid4())
    audio_path = os.path.join(ASSETS_AUDIO_DIR, f"{job_id}.mp3")
    image_path = os.path.join(ASSETS_IMAGES_DIR, f"{job_id}.png")
    video_filename = f"{job_id}.mp4"
    video_path = os.path.join(STATIC_VIDEO_DIR, video_filename)

    # 1. Generate Script
    script = generate_script(headline, lang)

    # 2. Generate Voice
    voice_name = "hi-IN-MadhurNeural" if lang == 'hi' else "en-US-GuyNeural"
    try:
        asyncio.run(voice_gen.generate_voice(script, voice_name, audio_path))
    except Exception as e:
        return jsonify({"error": f"Voice generation failed: {str(e)}"}), 500

    # 3. Generate Image
    try:
        image_gen.create_text_image(headline, image_path)
    except Exception as e:
        return jsonify({"error": f"Image generation failed: {str(e)}"}), 500

    # 4. Assemble Video
    try:
        video_gen.assemble_video(image_path, audio_path, video_path)
    except Exception as e:
        return jsonify({"error": f"Video assembly failed: {str(e)}"}), 500

    return jsonify({
        "success": True,
        "video_url": f"/static/videos/{video_filename}",
        "script": script
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
