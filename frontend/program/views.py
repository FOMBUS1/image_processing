import base64
from fastapi import FastAPI, File, Form, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List

import httpx
import os

app = FastAPI()

templates = Jinja2Templates(directory='templates')

rotate_url = os.getenv("ROTATE-SERVER")
mirror_url = os.getenv("MIRROR-SERVER")
invert_url = os.getenv("INVERT-SERVER")
resize_url = os.getenv("RESIZE-SERVER") 

print(rotate_url)
print(mirror_url)
print(invert_url)
print(resize_url)

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse('main-page.html', {'request': request})

@app.get("/index/{filter}", response_class=HTMLResponse)
async def index(filter: str, request: Request):
    print('-'*100)
    print(filter)
    dop_inf = ''
    if filter == 'Поворот картинки':
        id_func = 1
        dop_inf = '''
            <div class="form-group d-flex align-items-center">
                <label class="mr-2" for="angleInput">Угол:</label>
                <input type="text" class="form-control" id="angleInput" placeholder="Введите угол поворота">
            </div>
        '''
    elif filter == 'Негатив картинки':
        id_func = 2
    elif filter == 'Изменение размеров':
        id_func = 3
        dop_inf = '''
            <div class="form-group d-flex align-items-center">
                <label class="mr-2" for="xInput">X:</label>
                <input type="text" class="form-control" id="xInput" placeholder="Введите значение X">
            </div>
            <div class="form-group d-flex align-items-center">
                <label class="mr-2" for="yInput">Y:</label>
                <input type="text" class="form-control" id="yInput" placeholder="Введите значение Y">
            </div>
        '''
    elif filter == 'Отзеркалить картинку':
        id_func = 4

    else:
        id_func = 0

    return templates.TemplateResponse('index.html', {'request': request, 'classificator': filter, 'id_func': id_func, 'dop_inf': dop_inf})


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    type_func: int = Form(...),
    size: list[int] = Form(...),
    angle: int = Form(...)
):
    try:
        file_contents = await file.read()
        match type_func:
            case 1:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{rotate_url}/rotate",
                        files={"image": (file.filename, file_contents)},
                        data={"angle": angle}
                    )
            case 2:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{invert_url}/invert/",
                        files={"image": file_contents}
                    )
            case 3:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{resize_url}/resize_image/",
                        files={"image": file_contents},
                        data={"size": size}
                    )
            case 4:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{mirror_url}/mirror_image/",
                        files={"image": file_contents}
                    )
            case _:
                img_str = base64.b64encode(file_contents).decode("utf-8")
        if response.status_code == 200:
            mirrored_image_bytes = response.content
            img_str = base64.b64encode(mirrored_image_bytes).decode("utf-8")
            return JSONResponse(
                content={"image": f"data:image/png;base64,{img_str}"},
                media_type="application/json"
            )
        else:
            return JSONResponse(
                content={"error": f"Ошибка обработки файла на сервере: {response.text}"},
                media_type="application/json"
            )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Ошибка обработки файла: {str(e)}"},
            media_type="application/json"
        )


app.mount("/static", StaticFiles(directory="static"), name="static")