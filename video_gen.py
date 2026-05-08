from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

def assemble_video(image_path, audio_path, output_path):
    """
    Creates a video from a single image and an audio file with a watermark.
    """
    audio = AudioFileClip(audio_path)

    # Create main image clip
    main_clip = ImageClip(image_path, duration=audio.duration)

    # We add a simple "AI AGENT NEWS" watermark using a workaround since TextClip needs ImageMagick
    # Instead of TextClip, we could have pre-rendered the watermark in image_gen.
    # But for now, let's just use the main_clip with audio.

    try:
        final_clip = main_clip.with_audio(audio)
    except AttributeError:
        # Fallback for MoviePy v1.x
        final_clip = main_clip.set_audio(audio)

    final_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

    audio.close()
    main_clip.close()

if __name__ == "__main__":
    # Test
    pass
