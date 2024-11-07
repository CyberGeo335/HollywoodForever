# cropping_files.py
from ultralytics import YOLO
from PIL import Image
import io
import os
import torch
import onnxruntime as ort

# Относительные пути к модели и директории загрузки
model_path = os.path.abspath(os.path.join("model_repository", "models", "1", "model.onnx"))
upload_dir = os.path.abspath("upload")
print(f"Model path: {os.path.abspath(model_path)}")
print(f"Upload directory: {os.path.abspath(upload_dir)}")

# Создаём директорию upload, если она не существует
os.makedirs(upload_dir, exist_ok=True)

# Настройка провайдеров для onnxruntime, исключая TensorRT
#providers = ["CUDAExecutionProvider", "CPUExecutionProvider"] if torch.cuda.is_available() else ["CPUExecutionProvider"]
providers = ["CPUExecutionProvider"]
print(f"Using providers: {providers}")

def crop_image(image_data):
    # Сохраняем изображение в JPEG для совместимости с моделью
    image = Image.open(io.BytesIO(image_data))
    image = image.convert("RGB")

    # Генерируем уникальное имя файла для хранения
    image_path = os.path.join(upload_dir, "uploaded_image.jpg")
    image.save(image_path, format="JPEG")

    # Настраиваем ONNX Runtime с указанными провайдерами
    session = ort.InferenceSession(model_path, providers=providers)

    # Выполнение предсказания
    model = YOLO(model_path)
    results = model.predict(image_path, device="cuda" if "CUDAExecutionProvider" in providers else "cpu")

    cropped_images = []
    for result in results:
        if hasattr(result, 'boxes'):
            for box in result.boxes:
                if hasattr(box, 'xyxy') and box.xyxy.shape[-1] == 4:
                    x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
                    padding = 0.1

                    # Увеличиваем размеры рамки с padding
                    width, height = image.size
                    x_min = max(0, int(x_min - padding * (x_max - x_min)))
                    y_min = max(0, int(y_min - padding * (y_max - y_min)))
                    x_max = min(width, int(x_max + padding * (x_max - x_min)))
                    y_max = min(height, int(y_max + padding * (y_max - y_min)))

                    # Обрезаем изображение по рамке и добавляем в список
                    cropped_image = image.crop((x_min, y_min, x_max, y_max))
                    cropped_images.append(cropped_image)

    # Удаляем исходное изображение после обработки
    os.remove(image_path)

    return cropped_images