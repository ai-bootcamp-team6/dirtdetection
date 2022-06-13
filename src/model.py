import os
import fastapi
import uuid
from fastapi import UploadFile, File, Form
import uuid
from pathlib import Path
from infer import Inference

ROUTER = fastapi.APIRouter()
  
@ROUTER.post("/preprocess/image", status_code=fastapi.status.HTTP_200_OK)
async def preprocess_api(file: UploadFile=File(...)):
    """Takes in the image from user upload and preprocess it for
    training or inference. Uploaded image is saved in local.
    
    Args:
        File (PNG/JPG/JPEG): Image that user upload for training or inference.

    Returns:
        WRITE_PATH (str): File path of the preprocessed image
    """
    WORK_DIR = os.getcwd()
    WORKSPACE = WORK_DIR
    if not os.path.exists(WORKSPACE):
        os.makedirs(WORKSPACE)
    # save files as unique id
    file.filename = f"{uuid.uuid4()}.jpg"
    FILE_PATH = Path(file.filename)
    WRITE_PATH = WORK_DIR / FILE_PATH
    with open((WRITE_PATH) ,'wb') as myfile:
        contents = await file.read()
        myfile.write(contents)
    return WRITE_PATH

@ROUTER.post("/predict", status_code=fastapi.status.HTTP_200_OK)
async def predict(WRITE_PATH: str = Form(...)):
    """Takes in filepath of image uploaded to be fitted into YOLOMODEL and
    returns filepath of predicted 
    annotated image
    
    Args:
        WRITE_PATH (str): File path of the preprocessed image

    Returns:
        Image_path (str): File path of the predicted annotated image
    """
    a = Inference()
    result_dir = a.infer(weights='YOLOMODEL/full_10epoch.pt',project="YOLOMODEL/runs/detect",imgsz=[1280,900], source=WRITE_PATH)
    Image_path = a.get_results(result_dir)
    return Image_path


@ROUTER.post("/live", status_code=fastapi.status.HTTP_200_OK)
async def live(WRITE_PATH: str = Form(...)): 
    """Takes in filepath of image uploaded to be fitted into YOLOMODEL and
    returns filepath of predicted live webcam
    
    Args:
        WRITE_PATH (str): File path of the preprocessed image

    Returns:
        live_path (str): File path of live webcam
    """
    result_dir = Inference()._run(weights='YOLOMODEL/full_10epoch.pt',project="YOLOMODEL/runs/detect",imgsz=[1280,900], source=0)
    live_image = Inference().get_results(result_dir)
    return live_image

