from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from PIL import Image
import io

app = FastAPI()

@app.post("/mirror_image/")
async def upload_image(image: UploadFile = File(...)):
    contents = await image.read()
    img = Image.open(io.BytesIO(contents))
    mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    buffered = io.BytesIO()
    mirrored_img.save(buffered, format=img.format)
    buffered.seek(0)
    return Response(content=buffered.read(), media_type=image.content_type)
