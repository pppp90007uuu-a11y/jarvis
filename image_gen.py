from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def create_text_image(text, output_path, width=1920, height=1080):
    # Create a gradient-like background (dark blue to black)
    image = Image.new('RGB', (width, height), color=(15, 15, 25))
    draw = ImageDraw.Draw(image)

    # Draw a simple border
    draw.rectangle([20, 20, width-20, height-20], outline=(50, 50, 100), width=5)

    # Try to load a font
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\msgothic.ttc"
    ]

    font = None
    for path in font_paths:
        try:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 70)
                break
        except:
            continue

    if font is None:
        font = ImageFont.load_default()

    # Wrap text
    wrapper = textwrap.TextWrapper(width=40)
    lines = wrapper.wrap(text=text)

    # Calculate vertical position
    line_height = 90
    total_text_height = line_height * len(lines)
    y_text = (height - total_text_height) / 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x_text = (width - line_width) / 2

        # Draw shadow
        draw.text((x_text+4, y_text+4), line, font=font, fill=(0, 0, 0))
        # Draw main text
        draw.text((x_text, y_text), line, font=font, fill=(255, 255, 255))
        y_text += line_height

    image.save(output_path)

if __name__ == "__main__":
    create_text_image("Next-Gen AI is here to stay and change everything!", "assets/images/test_v2.png")
