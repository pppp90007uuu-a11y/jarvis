import asyncio
import google.generativeai as genai
import os

# Configure Gemini if API key is present
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

def generate_ai_script(headline, niche="Tech News", lang="hi"):
    """
    Generates an engaging YouTube script using Gemini AI or a template fallback.
    """
    prompt = f"""
    Write a 3-sentence engaging YouTube Short script for a {niche} channel.
    Topic: {headline}
    Language: {"Hindi (in Devanagari script)" if lang == 'hi' else "English"}
    Structure:
    1. A catchy hook line to grab attention.
    2. A brief but informative body about the news.
    3. An outro asking viewers to subscribe.
    Include 3 relevant hashtags at the end.
    """

    if model:
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"AI Generation failed: {e}")
            return fallback_script(headline, niche, lang)
    else:
        return fallback_script(headline, niche, lang)

def fallback_script(headline, niche, lang):
    if lang == 'hi':
        return f"नमस्ते दोस्तों! {niche} में आज की बड़ी खबर है: {headline}. यह तकनीक की दुनिया को पूरी तरह से बदल सकता है। ऐसे ही और शानदार अपडेट्स के लिए हमारे चैनल को अभी सब्सक्राइब करें! #TechNews #India #Tech"
    else:
        return f"Hey everyone! Today's big {niche} update is about: {headline}. This could be a game-changer for the industry. For more such exciting updates, make sure to subscribe! #Tech #Innovation #Update"

if __name__ == "__main__":
    # Quick test
    print(generate_ai_script("AI model is now free for everyone", "Tech News", "hi"))
