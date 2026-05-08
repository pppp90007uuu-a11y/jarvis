from moviepy import ImageClip, AudioFileClip

def assemble_video(image_path, audio_path, output_path):
    """
    Creates a video from a single image and an audio file.
    """
    audio = AudioFileClip(audio_path)
    # Create image clip with the same duration as audio
    clip = ImageClip(image_path, duration=audio.duration)
    # Set audio to the clip
    clip = clip.with_audio(audio)
    # Write to file
    clip.write_videofile(output_path, fps=24, codec="libx264")

    audio.close()
    clip.close()

if __name__ == "__main__":
    assemble_video("assets/images/test_image.png", "assets/audio/test_hindi.mp3", "static/videos/test_video.mp4")
    print("Created test video at static/videos/test_video.mp4")
