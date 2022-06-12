
from fileinput import filename
import os
import logging
import fastapi
import uuid
#from fastapi.responses import FileResponse

# import aiap_team6_miniproject_fastapi as team6_miniproject_fapi
# import aiap_team6_miniproject.data_prep.process_image as process_image
from PIL import Image
# from utils import read_imagefile
from fastapi import UploadFile, Response, File, Form
from fastapi.responses import FileResponse
from io import BytesIO
import shutil
import shutil
import uuid
from pathlib import Path
from typing import List
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
    with open(str(WRITE_PATH) ,'wb') as myfile:
        contents = await file.read()
        myfile.write(contents)
    return str(WRITE_PATH)
    # return {"source": str(WRITE_PATH)}

@ROUTER.post("/predict", status_code=fastapi.status.HTTP_200_OK)
async def predict(file: UploadFile= File(...)): # place holder for image preprocessing 
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
    with open(str(WRITE_PATH) ,'wb') as myfile:
        contents = await file.read()
        myfile.write(contents)
    # return local file paths
    a = Inference()
    result_dir = a.infer(weights='YOLOMODEL/full_10epoch.pt',project="YOLOMODEL/runs/detect",imgsz=[1280,900], source=WRITE_PATH)
    path = ""
    image = a.get_results(result_dir)
    # return FileResponse(image)
    return image
    bytes_io = BytesIO()
    image.save(bytes_io, format='PNG')
    return {"filepath": result_dir}
    return Response(bytes_io.getvalue(), media_type="image/png")
    return {"filepath": result_dir}

##########################<<<<CODE IVAN AND CHRIS HAVE DONE>>>>>################################
# @ROUTER.post("/preprocess/image", status_code=fastapi.status.HTTP_200_OK)
# def preprocess_api(file: UploadFile = File(...)): # place holder for image preprocessing 
#     """Endpoint that takes in the image from user upload and preprocess it for
#     training or inference.

#     Parameters
#     ----------
#     image : Image that user upload for training or inference.

#     Returns
#     -------
#     str
#         address of the preprocessed image
#     """
#     image = read_imagefile(file.read())
#     image.save(uuid.uuid4().hex + r'.jpg')
#     wk_dir = str(os.getcwd())
#     print(wk_dir)
#     return {"address": wk_dir}


##############################<FELICIA'S CODE FOR PREDICT#######################################
# @ROUTER.post("/infer", status_code=fastapi.status.HTTP_200_OK)
# def predict_model(processed_file_path: str):
#     """Endpoint that returns dirty classification of floor image.

#     Parameters
#     ----------
#     processed_file_path : str

#     Returns
#     -------
#     dict
#         Dictionary containing the prediction for processed image of the request.

#     Raises
#     ------
#     fastapi.HTTPException
#         A 500 status error is returned if the prediction steps
#         encounters any errors.
#     """
#     source = ""
#     a = Inference()
#     a.infer(weights="YOLOMODEL/weights/full_10epoch.pt",project="YOLOMODEL/runs/detect",imgsz=[1280,900],source="YOLOMODEL/runs/detect",imgsz=[1280,900],source= source)

#     try:
#         logger.info("Generating sentiments for floor image.")
#         curr_pred_result, output_file_path = PRED_MODEL.predict(processed_file_path)
#         dirt_prediction = "Dirty" if curr_pred_result == 1 else "Clean"

#         logger.info("Prediction generated for Image ID: {}".format(dirt_prediction))

#     except Exception as error:
#         print(error)
#         raise fastapi.HTTPException(status_code=500, detail="Internal server error.")

#     return {
#         "data": {"prediction": dirt_prediction, "image_file_path": output_file_path}
#         }

############################<<<CODE FEL AND I TRIED>>>##################################
# https://github.com/davidefiocco/streamlit-fastapi-model-serving/blob/master/fastapi/server.py

# # logger = logging.getLogger(__name__)
# #PRED_MODEL = team6_miniproject_fapi.deps.PRED_MODEL
# def get_segments(binary_image):

#     input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")

#     return input_image

# segmented_image = get_segments(file)
#     bytes_io = io.BytesIO()
#     segmented_image.save(bytes_io, format='PNG')
#     return Response(bytes_io.getvalue(), media_type="image/png")