import io
import base64
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

font_path = os.path.join(os.path.dirname(__file__), 'opensans-regular.ttf')

def complete_image(image_content, translated_texts, bounding_info):
    image = Image.open(io.BytesIO(image_content)).convert("RGB")
    cv_image = np.array(image)

    for i, (x, y, w, h) in enumerate(bounding_info):
        if w < 0 or h < 0:
            continue
        # Create mask for in-painting
        mask = np.zeros(cv_image.shape[:2], dtype=np.uint8)
        mask[y:y+h, x:x+w] = 255

        # In-paint
        inpainted_image = cv2.inpaint(cv_image, mask, inpaintRadius=15, flags=cv2.INPAINT_TELEA)
        cv_image = inpainted_image  # Update cv_image for the next iteration

    # After inpainting, overlay translated text on the inpainted image
    text_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)

    for i, (x, y, w, h) in enumerate(bounding_info):
        if w < 0 or h < 0:
            continue

        # Get translated text for current bounding box
        translated_text = translated_texts[i]

        font_size = int(h * 0.8)
        font = ImageFont.truetype(font_path, font_size)

        text_width = draw.textlength(translated_text, font=font)
        text_height = font_size

        # Draw actual text in black
        draw.text(((x + (w - text_width) / 2), (y + (h - text_height) / 2)), translated_text, font=font, fill="red")

        # Draw bounding box in red
        draw.rectangle(((x, y), (x + w, y + h)), outline="red")

    out = Image.alpha_composite(Image.fromarray(cv_image, mode='RGB').convert('RGBA'), text_image)
    return out

def convert_to_response_format(pil_image):
    """Convert PIL Image to base64 encoded string."""
    buffered = io.BytesIO()
    pil_image.save(buffered, format="PNG")  # or "JPEG", etc.
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # You might want to prefix with data URI scheme for direct embedding in HTML
    return f"data:image/png;base64,{base64_image}"

