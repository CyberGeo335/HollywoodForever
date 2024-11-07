import streamlit as st
import requests
from PIL import Image
import io
import base64

URL = "http://backend:8000/back/"

st.title("Загрузка фотографии")

uploaded_file = st.file_uploader("Выберите фото...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    response = requests.post(
        URL,
        files={"file": uploaded_file.getvalue()}
    )
    if response.status_code == 200:
        data = response.json()
        original_image = Image.open(io.BytesIO(base64.b64decode(data["original_image"])))
        st.image(original_image, caption="Оригинальная фотография", use_column_width=True)

        st.write("Обрезанные фотографии с распознанным текстом:")
        for cropped in data["cropped_images"]:
            cropped_image = Image.open(io.BytesIO(base64.b64decode(cropped["image"])))
            st.image(cropped_image, caption="Обрезанная фотография", use_column_width=True)

            # Display OCR results from EasyOCR
            st.write("EasyOCR результаты:")
            for ocr in cropped["ocr_results_easyocr"]:
                st.write(f"Распознанный текст: {ocr['text']}")
                st.write(f"Вероятность: {ocr['probability'] * 100:.2f}%")

            # Display OCR results from PaddleOCR
            st.write("PaddleOCR результаты:")
            for ocr in cropped["ocr_results_paddleocr"]:
                st.write(f"Распознанный текст: {ocr['text']}")
                st.write(f"Вероятность: {ocr['probability'] * 100:.2f}%")

            # Display Median Voting Result
            st.write("Результат медианного голосования:")
            st.write(f"Распознанный текст: {cropped['voting_result']['text']}")
            st.write(f"Медианная вероятность: {cropped['voting_result']['median_probability'] * 100:.2f}%")
    else:
        st.write("Произошла ошибка при загрузке фотографии.")
