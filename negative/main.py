from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image, ImageOps

app = FastAPI()


@app.post("/invert/")
async def process_image(image: UploadFile = File(...)):
    image_data = await image.read()
    image = Image.open(BytesIO(image_data)).convert('RGB')

    # инверсия цветов
    image = ImageOps.invert(image)

    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    # Возвращаем обработанное изображение как ответ
    return StreamingResponse(img_byte_arr, media_type="image/png")