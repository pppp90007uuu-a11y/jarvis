# AI Tech News YouTube Automation Agent

This is a free, automated tool to generate Tech News videos for YouTube. It scrapes trending news, writes a script, generates a voiceover, and assembles a video with a dashboard.

## Features
- **Scraper**: Fetches latest tech news headlines.
- **Voiceover**: Uses `edge-tts` for high-quality, natural Hindi and English voices.
- **Video Generator**: Creates MP4 videos using `MoviePy` and `Pillow`.
- **Dashboard**: Easy-to-use web interface.

## Prerequisites
- Python 3.7+
- **FFmpeg**: Essential for video processing.
  - Linux: `sudo apt install ffmpeg`
  - Mac: `brew install ffmpeg`
  - Windows: Download from ffmpeg.org and add to PATH.

## Installation

1. Clone or download this repository.
2. Install the required Python libraries:
   ```bash
   pip install flask flask-cors moviepy edge-tts requests googlesearch-python Pillow
   ```

## How to Use

1. **Start the Server**:
   Run the following command in your terminal:
   ```bash
   python3 app.py
   ```
2. **Open Dashboard**:
   Open your web browser and go to:
   `http://localhost:5000`
3. **Generate Video**:
   - Click **"Refresh"** to load the latest tech topics.
   - Click the **"Hindi"** or **"English"** button next to a topic.
   - Wait for the "Generating Video..." loader to finish.
4. **Preview & Get Video**:
   - The video will play automatically in the preview window.
   - The final video file is saved in the `static/videos/` folder.

## Project Structure
- `app.py`: Main Flask application and API.
- `scraper.py`: Scrapes tech news from Google.
- `voice_gen.py`: Handles text-to-speech conversion.
- `image_gen.py`: Creates text-based image frames for the video.
- `video_gen.py`: Assembles the audio and image into an MP4 file.
- `templates/`: Contains the dashboard HTML.
- `static/videos/`: All generated videos are stored here.
- `assets/`: Temporary audio and image files.
