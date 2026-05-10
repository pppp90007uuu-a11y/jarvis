import asyncio
import edge_tts

async def generate_voice(text, voice_name, output_path):
    """
    Generates an audio file from text using edge-tts.
    voice_name: 'hi-IN-MadhurNeural' or 'en-US-GuyNeural'
    """
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(output_path)

if __name__ == "__main__":
    # Test generation
    text = "नमस्ते, यह एक टेस्ट वीडियो है।"
    voice = "hi-IN-MadhurNeural"
    output = "assets/audio/test_hindi.mp3"
    asyncio.run(generate_voice(text, voice, output))
    print(f"Generated test audio at {output}")
