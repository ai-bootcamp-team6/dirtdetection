import streamlit as st
import requests
from PIL import Image

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
        file_details = {"filename":image_file.name, "filetype":image_file.type, "filesize":image_file.size}
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
            predict = requests.post('http://127.0.0.1:8080/predict', 
            data = {"WRITE_PATH": test_response.json()})
            st.write(predict.json())
            st.write("This is the returned image")
            st.image(Image.open(predict.json()))

            # saved_address = test_response.text
            # st.write("Uploaded file saved at: " + str(saved_address))
        
        st.download_button(
        label="Download image", 
        data=image_file,
        file_name="imagename.png",
        mime="image/png")

if __name__ == "__main__":
    main()
