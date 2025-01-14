from io import BytesIO
import os
from pathlib import Path
import cv2
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from utils.video_processing import video_to_bw
from functions.check_image_or_video import check_file_type
from utils.response_helpers import error_response, success_response

BASE_DIR = Path(__file__).parents[2]
UPLOAD_DIR = "uploads"

class DataBody(BaseModel):
    file_name: str

router = APIRouter(
    prefix='/process',
    tags=['process_data']
)

@router.post('/upload/')
async def upload_chunk(
    file_chunk: UploadFile = File(...),
    chunk_number: int = Form(...),
    total_chunks: int = Form(...),
    file_name: str = Form(...)
):
    try:
        file_path = os.path.join(UPLOAD_DIR, file_name)
        with open(file_path, "ab") as f:
            while content := await file_chunk.read(1024):  # Read chunk data in smaller blocks
                f.write(content)

        if chunk_number == total_chunks:
            return success_response(
            data={
                "file_name": file_name
            },
            message="Upload complete",
            code=200
        )

        return success_response(
            data={
                "chunk_number": chunk_number
            },
            message="Chunk received",
            code=200
        )
    except:
        return error_response(
            error_type="Internal Server Error",
            details="Some Interval Server Error Occured",
            message="Server could not complete the request",
            code=500
        )


@router.post('/process/')
async def process_data(
    body: DataBody
):
    file_path = os.path.join(BASE_DIR, UPLOAD_DIR, body.file_name)
    print(file_path)
    file_type = check_file_type(body.file_name)

    if file_type == 'image':
        image = cv2.imread(file_path)
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, encoded_image = cv2.imencode(".png", gray_image)
        return StreamingResponse(BytesIO(encoded_image.tobytes()), media_type="image/png")

    elif file_type == 'video':
        output_file = os.path.join(BASE_DIR, UPLOAD_DIR, f"bw_{body.file_name}")

        out_bw_video_path = video_to_bw(input_video_path=file_path, output_video_path=output_file)

        return StreamingResponse(open(out_bw_video_path, "rb"), media_type="video/mp4")