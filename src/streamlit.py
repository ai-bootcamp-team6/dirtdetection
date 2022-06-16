import streamlit as st
import requests
from PIL import Image
from streamlit_option_menu import option_menu
import cv2

# # interact with FastAPI endpoint
upload_url = "http://127.0.0.1:8080/upload"
predict_url = "http://127.0.0.1:8080/predict"
live_url = "http://127.0.0.1:8080/live"

def main():
    """This main function does the following:
    - format streamlit app
    - loads trained model on cache
    - Gets file/ live webcam image from user to be loaded for inferencing
    - conducts inferencing on file
    - outputs predicted annotated image on the dashboard
    """
    
    LIVE_CAM= "Live Detection"
    IMG_PRED = "Image Prediction"
    # Header showing "AIAP Team 6 Dirt Detection"
    st.write('AIAP Team 6 Dirt Detection')

    # Subheader showing "You never know how dirty your floor is!"
    st.write('You never know how dirty your floor is!')

    
    # Sidebar with options: "Image Prediction" & "Live Detection"
    with st.sidebar:
        selected = option_menu("", 
                                [IMG_PRED, 
                                LIVE_CAM],
                                icons=['image', 'camera'], 
                                menu_icon="cast", 
                                default_index=1)

    st.markdown('#')    
    # For detection via static image upload
    if selected == IMG_PRED:
        image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
        if image_file is not None:
            # To See details
            file_details = {"filename":image_file.name, 
                            "filetype":image_file.type, 
                            "filesize":image_file.size}
            st.write(file_details)
            # Get response from FASTAPI preprocess_url
            test_response = requests.post(upload_url, 
                                        files = {"file": image_file.read()})
            
            # Prints out saved uploaded file filepath
            saved_address = test_response.text
            st.write("Uploaded file saved at: " + str(saved_address))
            st.write('Original image uploaded')
            st.image(Image.open(image_file))

            if test_response.ok:
                st.write('Upload completed successfully!')
                st.markdown('#') 
            else:
                st.write("Something went wrong!")

            # Predict button
            if st.button("Predictions"):
                waiting_text = st.empty()
                waiting_text.text("Generating prediction...")
                # Get response from FASTAPI predict_url
                predict = requests.post(predict_url, 
                data = {"write_path": test_response.json()})
                st.write('Dirty floor or not?')
                st.image(Image.open(predict.json()))
                
                with open(predict.json(), 'rb') as file:
                    st.download_button(
                    label="Download image", 
                    data=file,
                    file_name="annotated_image.png",
                    mime="image/png")


    st.markdown('#')
    # For detection via webcam live feed
    if selected == LIVE_CAM:
        if st.button(LIVE_CAM):
            waiting_text = st.empty()
            waiting_text.text("Please press 'q' to exit...")
            # Get response from FASTAPI live_url
            requests.post(live_url, 
            data = {"WRITE_PATH": 1})   
            while cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    main()
