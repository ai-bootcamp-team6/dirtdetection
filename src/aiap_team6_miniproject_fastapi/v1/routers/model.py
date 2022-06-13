
from email.header import Header
from fileinput import filename
from gzip import WRITE
import os
import fastapi
import uuid
from PIL import Image
# from utils import read_imagefile
from fastapi import UploadFile, Response, File, Form
from fastapi.responses import FileResponse
from io import BytesIO
import shutil
import shutil
import uuid
from pathlib import Path
from typing import List, Optional
from infer import Inference

# logger = logging.getLogger(__name__)
ROUTER = fastapi.APIRouter()
# PRED_MODEL = team6_miniproject_fapi.deps.PRED_MODEL
#################################Julia working codes########################
  
@ROUTER.post("/preprocess/image", status_code=fastapi.status.HTTP_200_OK)
async def preprocess_api(file: UploadFile=File(...)): # place holder for image preprocessing 
    """Endpoint that takes in the image from user upload and preprocess it for
    training or inference.
    
    Parameters
    ----------
    image : Image that user upload for training or inference.

    Returns
    -------
    str
        address of the preprocessed image
    """
    WORK_DIR = os.getcwd()
    # UUID to prevent file overwrite
    # 'beautiful' path concat instead of WORK_DIR + '/' + REQUEST_ID
    WORKSPACE = WORK_DIR
    if not os.path.exists(WORKSPACE):
        # recursively create workdir/unique_id
        os.makedirs(WORKSPACE)
    # iterate through all uploaded files
    file.filename = f"{uuid.uuid4()}.jpg"
    FILE_PATH = Path(file.filename)
    WRITE_PATH = WORK_DIR / FILE_PATH
    with open((WRITE_PATH) ,'wb') as myfile:
        contents = await file.read()
        myfile.write(contents)
    return WRITE_PATH
    # return {"source": str(WRITE_PATH)}


@ROUTER.post("/predict", status_code=fastapi.status.HTTP_200_OK)
async def predict(WRITE_PATH: str = Form(...)): # place holder for image preprocessing 
    """Endpoint that takes in the image from user upload and preprocess it for
    training or inference.
    
    Parameters
    ----------
    image : Image that user upload for training or inference.

    Returns
    -------
    str
        address of the preprocessed image
    """
    a = Inference()
    result_dir = a.infer(weights='YOLOMODEL/full_10epoch.pt',project="YOLOMODEL/runs/detect",imgsz=[1280,900], source=WRITE_PATH)
    image = a.get_results(result_dir)
    # return FileResponse(image)
    return image
