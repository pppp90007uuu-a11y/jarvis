import unittest
import os
import asyncio
import scraper
import voice_gen
import image_gen
import video_gen
import ai_engine

class TestAutomationAgent(unittest.TestCase):

    def test_scraper(self):
        news = scraper.get_tech_news()
        self.assertIsInstance(news, list)
        self.assertGreater(len(news), 0)

    def test_ai_engine(self):
        script = ai_engine.generate_ai_script("Test headline", "Tech", "en")
        self.assertIn("Test headline", script)

    def test_voice_gen(self):
        output = "assets/audio/unit_test.mp3"
        if os.path.exists(output): os.remove(output)
        asyncio.run(voice_gen.generate_voice("Test audio", "en-US-GuyNeural", output))
        self.assertTrue(os.path.exists(output))

    def test_image_gen(self):
        output = "assets/images/unit_test.png"
        if os.path.exists(output): os.remove(output)
        image_gen.create_text_image("Test Image", output)
        self.assertTrue(os.path.exists(output))

if __name__ == "__main__":
    unittest.main()
