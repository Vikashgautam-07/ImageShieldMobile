from PIL import Image, ImageDraw, ImageFont
import piexif
import os

def add_watermark(image_path, output_path, text="SAFE SHARE", opacity=128, angle=45, position="bottom-right"):
    image = Image.open(image_path).convert("RGBA")
    watermark = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    font_size = int(min(image.size) / 10)
    font = ImageFont.load_default()

    text_width, text_height = draw.textsize(text, font)
    x, y = {
        "top-left": (10, 10),
        "top-right": (image.width - text_width - 10, 10),
        "bottom-left": (10, image.height - text_height - 10),
        "bottom-right": (image.width - text_width - 10, image.height - text_height - 10)
    }.get(position, (10, 10))

    draw.text((x, y), text, fill=(0, 0, 255, opacity), font=font)

    watermarked = Image.alpha_composite(image, watermark).rotate(angle)
    watermarked = watermarked.convert("RGB")
    watermarked.save(output_path)

    # Strip metadata
    piexif.remove(output_path)

    return output_path