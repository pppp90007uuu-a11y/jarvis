from moviepy import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips, vfx
import os

def assemble_video(media_paths, audio_path, output_path, headline="Breaking News"):
    """
    Assembles a video using multiple clips/images to match audio duration.
    """
    audio = AudioFileClip(audio_path)
    target_duration = audio.duration

    clips = []
    current_duration = 0

    # If no media provided, use a placeholder
    if not media_paths:
        # We need at least one image/video. For now, we'll assume image_gen handled one.
        pass

    while current_duration < target_duration:
        for path in media_paths:
            if current_duration >= target_duration: break

            try:
                if path.endswith(".mp4"):
                    clip = VideoFileClip(path).without_audio()
                    # Crop/Resize to 1080p
                    clip = clip.resized(height=1080)
                    if clip.w > 1920:
                        clip = clip.cropped(x_center=clip.w/2, width=1920)
                else:
                    clip = ImageClip(path, duration=5)
                    clip = clip.resized(height=1080)

                # If clip is longer than remaining time, trim it
                remaining = target_duration - current_duration
                if clip.duration > remaining:
                    clip = clip.subclipped(0, remaining)

                clips.append(clip)
                current_duration += clip.duration
            except Exception as e:
                print(f"Error processing clip {path}: {e}")
                continue

        # If we went through all paths and still have time, loop or use a solid color if empty
        if not media_paths:
            # Fallback (should not happen if image_gen is called)
            break

    if not clips:
        raise Exception("No valid clips found for video assembly")

    final_video = concatenate_videoclips(clips, method="compose")

    try:
        final_video = final_video.with_audio(audio)
    except AttributeError:
        final_video = final_video.set_audio(audio)

    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

    # Cleanup
    for c in clips: c.close()
    audio.close()
    final_video.close()

if __name__ == "__main__":
    pass
