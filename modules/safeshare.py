from PIL import Image, ImageDraw, ImageFont

def generate_safe_preview(pil_image, text="SAFE SHARE", opacity=120, angle=30, position="bottom-right"):
    """
    Adds a watermark and removes metadata.
    """
    img = pil_image.copy().convert("RGBA")
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    text_size = draw.textbbox((0, 0), text, font=font)
    w, h = text_size[2]-text_size[0], text_size[3]-text_size[1]

    positions = {
        "bottom-right": (img.width - w - 20, img.height - h - 20),
        "bottom-left": (20, img.height - h - 20),
        "top-right": (img.width - w - 20, 20),
        "top-left": (20, 20),
    }
    pos = positions.get(position, positions["bottom-right"])

    draw.text(pos, text, font=font, fill=(255, 255, 255, opacity))
    txt_layer = txt_layer.rotate(angle, expand=1)
    watermarked = Image.alpha_composite(img, txt_layer)
    return watermarked.convert("RGB")
