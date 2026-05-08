from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def create_text_image(text, output_path, width=1920, height=1080):
    # Create a dark background
    image = Image.new('RGB', (width, height), color=(20, 20, 30))
    draw = ImageDraw.Draw(image)

    # Try to load a font, otherwise use default
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc" # Supports Hindi/Chinese
    ]

    font = None
    for path in font_paths:
        try:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 60)
                break
        except:
            continue

    if font is None:
        font = ImageFont.load_default()

    # Wrap text
    wrapper = textwrap.TextWrapper(width=30)
    lines = wrapper.wrap(text=text)

    # Calculate vertical position to center text
    line_height = font.getbbox("Ay")[3] + 20
    total_text_height = line_height * len(lines)
    y_text = (height - total_text_height) / 2

    for line in lines:
        # Center horizontally
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x_text = (width - line_width) / 2
        draw.text((x_text, y_text), line, font=font, fill=(255, 255, 255))
        y_text += line_height

    image.save(output_path)

if __name__ == "__main__":
    create_text_image("Aaj ki Tech News: AI ka naya Model Launch ho gaya!", "assets/images/test_image.png")
    print("Created test image at assets/images/test_image.png")
