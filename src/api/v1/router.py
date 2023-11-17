import os
from typing import Dict, List, Optional
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
from functools import partial

from requests_toolbelt import MultipartEncoder
from fastapi import UploadFile, File, APIRouter, HTTPException, status
from fastapi.responses import Response
from src.core.config import app_settings
from src.process_data.cnn import model_processing


router = APIRouter()

messages = (
    "% вероятность ЗАРН\nВысокая вероятность ЗАРН, требуется проверка!",
    "% вероятность ЗАРН\n"
)

def write_file(file: UploadFile, in_chunks):
    try:
        contents = file.file.read()
        res_folder = os.path.join(app_settings.res_path, file.filename)
        with open(res_folder, 'wb') as f:
            with open(res_folder, 'wb') as f:
                f.write(contents)
    except Exception as exc:
        return {"message": f"There was an error while uploading the file: {exc}"}
    finally:
        file.file.close()
    return res_folder


@router.post("/upload_file")
def upload_file(file: UploadFile = File(...), in_chunks=False):
    """
    Uploads single file
    :param file: File that is being uploaded
    :param in_chunks: If file is too big to fit into memory,
    set this value to true
    :return:
    """
    if (path_to_file := write_file(file, in_chunks)) is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="There was an error while retrieving"
                                   "uploaded file")
    try:
        probability = model_processing(path_to_file)
    except Exception:
        return {"message": "There was an error while processing the file"}
    is_pathology = (probability > 0.7)
    m = MultipartEncoder(
        fields={
            'message': messages[0] if is_pathology else messages[1],
            'image': (file.filename, open(path_to_file, 'rb'), 'image/jpeg')
        }
    )
    return Response(m.to_string(), media_type=m.content_type)

@router.post('/upload_files')
def upload_files(
        files: List[UploadFile] = File(...), in_chunks=False
):
    """
    Uploads multiple files
    :param files: List of files that are being uploaded
    :param in_chunks: If files are big set this value to True
    :return: returns text message and images with pathology
    """
    with ThreadPool() as thread_pool:
        path_to_files = thread_pool.map(partial(write_file, in_chunks=in_chunks), files)
    with Pool() as process_pool:
        probabilities = process_pool.map(model_processing, path_to_files)
    results = []
    for i, probability in enumerate(probabilities):
        is_pathology = probability > 0.7
        results = {
            f'message{i}': messages[0] if is_pathology else messages[1],
            f'image{i}': (
                files[i].filename, open(path_to_files[i], 'rb'), 'image/jpeg'
            )
        }
    m = MultipartEncoder(results)
    return Response(m.to_string(), media_type=m.content_type)
