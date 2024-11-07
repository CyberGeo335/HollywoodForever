from fastapi import FastAPI, File, UploadFile
import base64
import io
from cropping_files import crop_image
from ocr_recognize import recognize_text_easyocr, recognize_text_paddleocr
from voting import median_voting

app = FastAPI()


@app.post("/back/")
async def upload_photo(file: UploadFile = File(...)):
    image_data = await file.read()
    cropped_images = crop_image(image_data)

    ocr_results_easyocr = recognize_text_easyocr(cropped_images)
    ocr_results_paddleocr = recognize_text_paddleocr(cropped_images)

    voting_results = median_voting(ocr_results_easyocr, ocr_results_paddleocr)

    cropped_images_base64 = []
    for img, ocr_easy, ocr_paddle, voting_result in zip(cropped_images, ocr_results_easyocr, ocr_results_paddleocr,
                                                        voting_results):
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        cropped_images_base64.append({
            "image": img_base64,
            "ocr_results_easyocr": ocr_easy,
            "ocr_results_paddleocr": ocr_paddle,
            "voting_result": voting_result
        })

    original_image_base64 = base64.b64encode(image_data).decode("utf-8")

    return {"original_image": original_image_base64, "cropped_images": cropped_images_base64}
