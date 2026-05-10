import asyncio
import google.generativeai as genai
import os
import re

# Configure Gemini if API key is present
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

def generate_ai_script(headline, niche="Tech News", lang="hi"):
    """
    Generates a detailed script (30-80s) and search keywords.
    """
    prompt = f"""
    Create a detailed YouTube script for a {niche} channel.
    Topic: {headline}
    Language: {"Hindi (in Devanagari script)" if lang == 'hi' else "English"}

    Requirements:
    1. Duration: Must be around 45-60 seconds when spoken (approx 120-150 words).
    2. Structure: Catchy Hook, Detailed Explanation, Interesting Fact, and Call to Action.
    3. Output Format:
       SCRIPT: [The full script here]
       KEYWORDS: [5-8 comma separated English keywords for stock video search related to this topic]
       HASHTAGS: #tag1 #tag2 #tag3
    """

    if model:
        try:
            response = model.generate_content(prompt)
            return parse_ai_response(response.text, headline, niche, lang)
        except Exception as e:
            print(f"AI Generation failed: {e}")
            return fallback_script(headline, niche, lang)
    else:
        return fallback_script(headline, niche, lang)

def parse_ai_response(text, headline, niche, lang):
    script_match = re.search(r"SCRIPT:(.*?)(?=KEYWORDS:|$)", text, re.DOTALL | re.IGNORECASE)
    keywords_match = re.search(r"KEYWORDS:(.*?)(?=HASHTAGS:|$)", text, re.DOTALL | re.IGNORECASE)
    hashtags_match = re.search(r"HASHTAGS:(.*)", text, re.DOTALL | re.IGNORECASE)

    script = script_match.group(1).strip() if script_match else text
    keywords = keywords_match.group(1).strip() if keywords_match else "technology, innovation, future"
    hashtags = hashtags_match.group(1).strip() if hashtags_match else "#tech #news"

    return {
        "script": f"{script}\n\n{hashtags}",
        "keywords": [k.strip() for k in keywords.split(",")]
    }

def fallback_script(headline, niche, lang):
    # Expanded fallback to ensure minimum length
    if lang == 'hi':
        script = f"नमस्ते दोस्तों! {niche} में आज एक बहुत बड़ी अपडेट आई है। खबर है कि {headline}। यह तकनीक की दुनिया में एक बड़ा बदलाव ला सकता है। जानकारों का मानना है कि इससे आने वाले समय में हमें काफी कुछ नया देखने को मिलेगा। क्या आप इसके लिए तैयार हैं? हमें कमेंट्स में बताएं और ऐसे ही और भी मजेदार और जानकारीपूर्ण वीडियोस के लिए हमारे चैनल को अभी सब्सक्राइब करना न भूलें! धन्यवाद।"
    else:
        script = f"Hey everyone! We have a major update in the world of {niche}. Today we are talking about {headline}. This development is expected to revolutionize how we interact with technology in our daily lives. Industry experts are already calling it a game-changer. What are your thoughts on this? Let us know in the comments below! Don't forget to hit that subscribe button for more deep dives into the latest tech. See you in the next one!"

    return {
        "script": script + "\n\n#tech #news #innovation",
        "keywords": ["technology", "innovation", "future", "news", "digital"]
    }

if __name__ == "__main__":
    res = generate_ai_script("SpaceX Starship Launch", "Science", "en")
    print(f"Script Length: {len(res['script'].split())} words")
    print(f"Keywords: {res['keywords']}")
