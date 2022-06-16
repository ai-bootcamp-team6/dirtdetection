import os
import fastapi
from fastapi import UploadFile, File, Form
import uuid
from pathlib import Path
from infer import Inference

APP = fastapi.APIRouter()
  
@APP.post("/upload", status_code=fastapi.status.HTTP_200_OK)
async def upload(file: UploadFile=File(...)):
    """Takes in the image from user saves image locally.
    
    Args:
        File (PNG/JPG/JPEG): Image that user upload for training or inference.

    Returns:
        WRITE_PATH (str): File path of the preprocessed image
    """
    
    WORK_DIR = os.getcwd()
    if not os.path.exists(WORK_DIR):
        os.makedirs(WORK_DIR)
    # save files as unique id
    file.filename = f"{uuid.uuid4()}.jpg"
    FILE_PATH = Path(file.filename)
    WRITE_PATH = WORK_DIR / FILE_PATH
    with open((WRITE_PATH) ,'wb') as myfile:
        contents = await file.read()
        myfile.write(contents)
        
    return WRITE_PATH

@APP.post("/predict", status_code=fastapi.status.HTTP_200_OK)
async def predict(write_path: str = Form(...)):
    """Takes in filepath of image uploaded to be fitted into YOLOMODEL and
    returns filepath of predicted annotated image
    
    Args:
        WRITE_PATH (str): File path of the preprocessed image

    Returns:
        Image_path (str): File path of the predicted annotated image
    """
    
    result_dir = Inference().infer(weights='YOLOMODEL/full_10epoch.pt',
                        project="YOLOMODEL/runs/detect",
                        imgsz=[1280,900], 
                        source=write_path)
    image_path = Inference().get_results(result_dir)

    return image_path


@APP.post("/live", status_code=fastapi.status.HTTP_200_OK)
async def live(): 
    """Activate Live Inference
    
    Args:
        None

    Returns:
        None
    """
    Inference()._run(weights='YOLOMODEL/full_10epoch.pt', 
                    project="YOLOMODEL/runs/detect",
                    imgsz=[1280,900], 
                    source=0)
    

    return None

