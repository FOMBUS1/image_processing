from fastapi import FastAPI, File, Form, UploadFile, Response
from PIL import Image
import io

app = FastAPI()

@app.post("/resize_image/")
async def resize_image(
    image: UploadFile = File(...),
    size: list[int] = Form(...)
):
    try:
        file_contents = await image.read()
        byte_stream = io.BytesIO(file_contents)
        img = Image.open(byte_stream)
        new_width, new_height = size
        resized_img = img.resize((new_width, new_height))
        resized_bytes = io.BytesIO()
        resized_img.save(resized_bytes, format='PNG')
        return Response(content=resized_bytes.getvalue(), media_type="image/png")
    except Exception as e:
        return {"error": f"Ошибка обработки файла: {str(e)}"}