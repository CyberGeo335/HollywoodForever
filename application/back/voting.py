from statistics import median


def median_voting(ocr_results_easyocr, ocr_results_paddleocr):
    voting_results = []
    for easyocr_results, paddleocr_results in zip(ocr_results_easyocr, ocr_results_paddleocr):
        # Собираем все тексты и вероятности для текущего обрезанного изображения
        texts = []
        probabilities = []

        # Обрабатываем результаты EasyOCR
        for result in easyocr_results:
            texts.append(result["text"])
            probabilities.append(result["probability"])

        # Обрабатываем результаты PaddleOCR
        for result in paddleocr_results:
            texts.append(result["text"])
            probabilities.append(result["probability"])

        # Вычисляем медианную вероятность
        median_probability = median(probabilities)

        # Находим текст, наиболее близкий к медианной вероятности
        closest_index = min(range(len(probabilities)), key=lambda i: abs(probabilities[i] - median_probability))
        selected_text = texts[closest_index]

        voting_results.append({
            "text": selected_text,
            "median_probability": median_probability
        })

    return voting_results
