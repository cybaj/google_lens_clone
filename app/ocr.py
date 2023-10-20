from typing import cast, Dict
import pytesseract
from PIL import Image
import io

def extract_text(image_content):
    image = Image.open(io.BytesIO(image_content))
    result = cast(Dict, pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT))

    extracted_texts = []
    bounding_info = []

    for i in range(len(result['text'])):
        if result['conf'][i] > 80:  # you can adjust this confidence threshold
            x, y, w, h = result['left'][i], result['top'][i], result['width'][i], result['height'][i]
            if (w < 5) and (h < 5):
                continue
            if (result['text'][i].strip() == ''):
                continue
            extracted_texts.append(result['text'][i])
            bounding_info.append((x, y, w, h))

    return extracted_texts, bounding_info

