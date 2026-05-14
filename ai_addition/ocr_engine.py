import pytesseract
from PIL import Image


def extract(image_path):

    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='eng')
        return text.strip()

    except Exception as e:
        print(e)
        return ""