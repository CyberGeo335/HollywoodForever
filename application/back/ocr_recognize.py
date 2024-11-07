# ocr_recognize.py
import easyocr
from PIL import Image
import io
from paddleocr import PaddleOCR

# Инициализация моделей EasyOCR и PaddleOCR
easyocr_reader = easyocr.Reader(['en'])
# Модель PaddleOCR для английского языка
paddleocr_reader = PaddleOCR(lang='en')

def recognize_text_easyocr(cropped_images):
    ocr_results = []
    for img in cropped_images:
        if not isinstance(img, Image.Image):
            img = Image.fromarray(img)

        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_bytes = img_byte_array.getvalue()

        result = easyocr_reader.readtext(img_bytes)
        texts = []
        for (bbox, text, prob) in result:
            texts.append({"text": text, "probability": prob})
            print(f"EasyOCR - Detected text: {text}, Probability: {prob}")

        ocr_results.append(texts if texts else [{"text": "", "probability": 0.0}])

    return ocr_results

def recognize_text_paddleocr(cropped_images):
    ocr_results = []
    for img in cropped_images:
        if not isinstance(img, Image.Image):
            img = Image.fromarray(img)

        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_bytes = img_byte_array.getvalue()

        result = paddleocr_reader.ocr(img_bytes, cls=True)
        texts = []
        for line in result[0]:
            text = line[1][0]
            prob = line[1][1]
            texts.append({"text": text, "probability": prob})
            print(f"PaddleOCR - Detected text: {text}, Probability: {prob}")

        ocr_results.append(texts if texts else [{"text": "", "probability": 0.0}])

    return ocr_results
