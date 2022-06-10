import io

import torch
from PIL import Image
from torchvision import transforms

import os
import logging
import fastapi

#import aiap_team6_miniproject_fastapi as team6_miniproject_fapi
from PIL import Image
# from utils import read_imagefile
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse, Response
from xxlimited import Str

ROUTER = fastapi.APIRouter()

def get_segments(binary_image):

    input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
    
    # preprocessing steps
    return input_image


@ROUTER.post("/preprocess/image", status_code=fastapi.status.HTTP_200_OK)
async def preprocess_api(file: bytes = File(...)): # place holder for image preprocessing 
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

    segmented_image = get_segments(file)
    bytes_io = io.BytesIO()
    segmented_image.save(bytes_io, format='PNG')
    return Response(bytes_io.getvalue(), media_type="image/png")
#####################################################################################
# # logger = logging.getLogger(__name__)
# #PRED_MODEL = team6_miniproject_fapi.deps.PRED_MODEL

# def read_imagefile(file):
#     """Takes in jpg and png file and Read it

#     Parameters
#     ----------

#     file: Image file with extension jpg or png

#     Returns
#     -------

#     array
#         Image array data
#     """
#     image = Image.open(file)

#     return image

#     try:
#         extension = file.filename.split(".")[-1] in ("jpg","jpeg","png")
#         if not extension:
#             return "Image must be jpg or png format."
#         # logger.info("Uploading Image")
#         image = read_imagefile(file.read())
#         print("image read")
#         # logger.info("Reading Image, starting preprocessing")
#         # processed_image = process_image.preprocess(image) # Placeholder
#         # logger.info("Image preprocessing completed")
        
#         wk_dir = str(os.getcwd())
#         print(wk_dir)
#         filename = file.filename
    
#         print(filename)
#         image = image.save(wk_dir + filename)
#         # Figure a way to save to polyaxon persistent data?
#         # Saving done in the process_image.py file?
#         # Download locally?
#         # Create the address of the saved image
#         saved_location = str(wk_dir + filename)
#         print(saved_location)
#     except Exception as error:
#         print(error)
#         raise fastapi.HTTPException(
#             status_code=500, detail="Internal server error.")

#     return {"address": saved_location} # placeholder for processed image address

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



# # @ROUTER.get("/download/", status_code=fastapi.status.HTTP_200_OK)
# # def download_image_api():
# #     """
# #     """
# #     # need to figure out how to download processed image.
# #     pass


# # @ROUTER.delete("/delete/", status_code=fastapi.status.HTTP_200_OK)
# # def delete_image(file):
# #     """
# #     """

#     # Need to figure out what goes here

#     return {"deleted_file": str} # place holder for deleted image file name.





##############################################################################
# Ryzal Template below

# @ROUTER.post("/predict", status_code=fastapi.status.HTTP_200_OK)
# def predict_sentiment(movie_reviews_json: team6_miniproject_fapi.schemas.MovieReviews):
#     """Endpoint that returns sentiment classification of movie review
#     texts.

#     Parameters
#     ----------
#     movie_reviews_json : team6_miniproject_fapi.schemas.MovieReviews
#         'pydantic.BaseModel' object detailing the schema of the request
#         body

#     Returns
#     -------
#     dict
#         Dictionary containing the sentiments for each movie review in
#         the body of the request.

#     Raises
#     ------
#     fastapi.HTTPException
#         A 500 status error is returned if the prediction steps
#         encounters any errors.
#     """
#     result_dict = {"data": []}

#     try:
#         logger.info("Generating sentiments for movie reviews.")
#         movie_reviews_dict = movie_reviews_json.dict()
#         review_texts_array = movie_reviews_dict["reviews"]
#         for review_val in review_texts_array:
#             curr_pred_result = PRED_MODEL.predict([review_val["text"]])
#             sentiment = ("positive" if curr_pred_result > 0.5
#                         else "negative")
#             result_dict["data"].append(
#                 {"review_id": review_val["id"], "sentiment": sentiment})
#             logger.info(
#                 "Sentiment generated for Review ID: {}".
#                 format(review_val["id"]))

#     except Exception as error:
#         print(error)
#         raise fastapi.HTTPException(
#             status_code=500, detail="Internal server error.")

#     return result_dict


# @ROUTER.get("/version", status_code=fastapi.status.HTTP_200_OK)
# def get_model_version():
#     """Get version (UUID) of predictive model used for the API.

#     Returns
#     -------
#     dict
#         Dictionary containing the UUID of the predictive model being
#         served.
#     """
#     return {"data": {"model_uuid": team6_miniproject_fapi.config.SETTINGS.PRED_MODEL_UUID}}
