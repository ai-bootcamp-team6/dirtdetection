import os
import logging
import hydra
import streamlit as st
import aiap_dsp_mlops as amlo
from PIL import Image
import aiap_dsp_mlops as amlo

@st.cache(allow_output_mutation=True)
def load_model(model_path):
    return amlo.modeling.utils.load_model(model_path)

@st.cache(allow_output_mutation=True)
def load_image(image_file):
	img = Image.open(image_file)
	return img

@hydra.main(config_path="../conf/base", config_name="pipelines.yml")
def main(args):
    """This main function does the following:
    - load logging config
    - loads trained model on cache
    - gets string input from user to be loaded for inferencing
    - conducts inferencing on string
    - outputs prediction results on the dashboard
    """

    logger = logging.getLogger(__name__)
    logger.info("Setting up logging configuration.")
    logger_config_path = os.path.\
        join(hydra.utils.get_original_cwd(),
            "conf/base/logging.yml")
    amlo.general_utils.setup_logging(logger_config_path)

    logger.info("Loading the model...")
    pred_model = load_model(args["inference"]["model_path"])

    logger.info("Loading dashboard...")
    
    st.subheader("AIAP Team 6")
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
    if image_file is not None:

        # To See details
        file_details = {"filename":image_file.name, "filetype":image_file.type,
                            "filesize":image_file.size}
        st.write(file_details)

        # To View Uploaded Image
        st.image(load_image(image_file))

        st.download_button(
        label="Download image",
        data=image_file,
        file_name="imagename.png",
        mime="image/png")
        
        # To change this
        if st.button("Get sentiment"):
            logger.info("Conducting inferencing on text input...")
            curr_pred_result = float(pred_model.predict([image_file])[0])
            sentiment = ("positive" if curr_pred_result > 0.5
                        else "negative")
            logger.info(
                "Inferencing has completed. Text input: {}. Sentiment: {}"
                .format(image_file, sentiment))
            st.write("The sentiment of the review is {}."
                .format(sentiment))
        else:
            st.write("Awaiting a review...")
if __name__ == "__main__":
    main()
