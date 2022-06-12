import os
import logging
import streamlit as st
import requests
import aiap_team6_miniproject as a6
from PIL import Image
import fastapi
import io
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

##############JULIA WORKING CODE##########################################

# # interact with FastAPI endpoint
test_url = "http://127.0.0.1:8080/api/v1/model/preprocess/image"
predict_url = "http://127.0.0.1:8080/api/v1/model/infer"

def main():
    """This main function does the following:
    - load logging config
    - loads trained model on cache
    - gets string input from user to be loaded for inferencing
    - conducts inferencing on string
    - outputs prediction results on the dashboard
    """
    st.subheader("AIAP Team 6")
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
    if image_file is not None:
        
        # To See details
        file_details = {"filename":image_file.name, "filetype":image_file.type,
                            "filesize":image_file.size}
        st.write(file_details)
        # To View Uploaded Image
    

        test_file = image_file.read()
        # test_file = open(image_file)
        test_response = requests.post('http://127.0.0.1:8080/preprocess/image', files = {"file": test_file})
        saved_address = test_response.text
        st.write("Uploaded file saved at: " + str(saved_address))
        st.write("This is the original image")
        st.image(Image.open(image_file))

        if test_response.ok:
            st.write("Upload completed successfully!")
        else:
            st.write("Something went wrong!")

        if st.button("Predictions"):
            test_response = requests.post('http://127.0.0.1:8080/predict', files = {"file": test_file})
            st.write(test_response.json())
            st.write("This is the returned image")
            st.image(Image.open(test_response.json()))

            # saved_address = test_response.text
            # st.write("Uploaded file saved at: " + str(saved_address))
        
        st.download_button(
        label="Download image", 
        data=image_file,
        file_name="imagename.png",
        mime="image/png")

if __name__ == "__main__":
    main()

##############################################################################


# def process(image, server_url: str):

#     m = MultipartEncoder(fields={"file": ("filename", image, "image/jpeg")})

#     r = requests.post(
#         server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000
#     )

#     return r


# image = st.file_uploader('insert image')

# if st.button('Get segmentation map'):
#     if image == None:
#         st.write("Insert an image!")  # handle case with no image
#     else:
#         segments = process(image, test_url)
#         segmented_image = Image.open(io.BytesIO(segments.content)).convert('RGB')
#         st.image([image, segmented_image], width=300)  # output dyptich




# #@hydra.main(config_path="../conf/base", config_name="pipelines.yml")


###############################################################################
    # logger = logging.getLogger(__name__)
    # logger.info("Setting up logging configuration.")
    # logger_config_path = os.path.\
    #     join(hydra.utils.get_original_cwd(),
    #         "conf/base/logging.yml")
    # a6.general_utils.setup_logging(logger_config_path)

    # logger.info("Loading the model...")
    # pred_model = load_model(args["inference"]["model_path"])

    # logger.info("Loading dashboard...")

        # curr_pred_result = float(pred_model.predict([image_file])[0])
        # sentiment = ("positive" if curr_pred_result > 0.5
        #             else "negative")
        # logger.info(
        #     "Inferencing has completed. Text input: {}. Sentiment: {}"
        #     .format(image_file, sentiment))
        # st.write("The sentiment of the review is {}."
        #     .format(sentiment))
    # else:
    #     st.write("Awaiting a review...")
