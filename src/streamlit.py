import streamlit as st
import requests
from PIL import Image
from streamlit_option_menu import option_menu
import cv2

# # interact with FastAPI endpoint
preprocess_url = "http://127.0.0.1:8080/preprocess/image"
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
    # Header showing "AIAP Team 6 Dirt Detection"
    st.markdown(f'<p style="color:#050505;text-align:center;font-size:48px;border-radius:2%;">AIAP Team 6 Dirt Detection</p>', unsafe_allow_html=True)

    # Subheader showing "You never know how dirty your floor is!"
    st.markdown(f'<p style="background-color:#f50505;color:#f7f5f5;text-align:center;font-size:36px;border-radius:2%;">You never know how dirty your floor is!</p>', unsafe_allow_html=True)

    # Sidebar with options: "Image Prediction" & "Live Detection"
    with st.sidebar:
        selected = option_menu("Main Menu", ["Image Prediction", 'Live Detection'],icons=['image', 'camera'], menu_icon="cast", styles={'nav-link': {'background-color':'#f50505'}}, default_index=1)

    st.markdown('#')    
    # For detection via static image upload
    if selected == 'Image Prediction':
        image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
        if image_file is not None:
            # To See details
            file_details = {"filename":image_file.name, "filetype":image_file.type, "filesize":image_file.size}
            st.write(file_details)
            # Get response from FASTAPI preprocess_url
            test_response = requests.post(preprocess_url, files = {"file": image_file.read()})
            saved_address = test_response.text
            # Prints out saved uploaded file filepath
            st.write("Uploaded file saved at: " + str(saved_address))
            st.markdown(f'<p style="color:#050505;font-size:22px;border-radius:2%;">Original image uploaded</p>', unsafe_allow_html=True)
            st.image(Image.open(image_file))

            if test_response.ok:
                st.markdown(f'<p style="color:#050505;font-size:22px;border-radius:2%;">Upload completed successfully!</p>', unsafe_allow_html=True)
                st.markdown('#') 
            else:
                st.write("Something went wrong!")

            # Predict button
            if st.button("Predictions"):
                waiting_text = st.empty()
                waiting_text.text("Generating prediction...")
                # Get response from FASTAPI predict_url
                predict = requests.post(predict_url, 
                data = {"WRITE_PATH": test_response.json()})
                st.markdown(f'<p style="color:#050505;font-size:22px;border-radius:2%;">Dirty floor or not?</p>', unsafe_allow_html=True)
                st.image(Image.open(predict.json()))
                
                with open(predict.json(), 'rb') as file:
                    st.download_button(
                    label="Download image", 
                    data=file,
                    file_name="annotated_image.png",
                    mime="image/png")


    st.markdown('#')
    # For detection via webcam live feed
    if selected == 'Live Detection':
        if st.button('Live Detection'):
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
