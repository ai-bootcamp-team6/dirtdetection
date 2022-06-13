import streamlit as st
import requests
from PIL import Image
from streamlit_option_menu import option_menu
import cv2

# # interact with FastAPI endpoint
test_url = "http://127.0.0.1:8080/preprocess/image"
predict_url = "'http://127.0.0.1:8080/predict'"

def main():
    """This main function does the following:
    - load logging config
    - loads trained model on cache
    - gets string input from user to be loaded for inferencing
    - conducts inferencing on string
    - outputs prediction results on the dashboard
    """
    st.markdown(f'<p style="color:#050505;text-align:center;font-size:48px;border-radius:2%;">AIAP Team 6 Dirt Detection</p>', unsafe_allow_html=True)

    st.markdown(f'<p style="background-color:#f50505;color:#f7f5f5;text-align:center;font-size:36px;border-radius:2%;">You never know how dirty your floor is!</p>', unsafe_allow_html=True)

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
                waiting_text = st.empty()
                waiting_text.text("Generating prediction...")
                predict = requests.post('http://127.0.0.1:8080/predict', 
                data = {"WRITE_PATH": test_response.json()})
                st.write(predict.json())
                st.write("This is the returned image")
                st.image(Image.open(predict.json()))
                an_img = predict.json()
                # saved_address = test_response.text
                # st.write("Uploaded file saved at: " + str(saved_address))
            
                # saved_address = test_response.text
                # st.write("Uploaded file saved at: " + str(saved_address))
                with open(an_img, 'rb') as file:
                    st.download_button(
                    label="Download image", 
                    data=file,
                    file_name="annotated_image.png",
                    mime="image/png")



    st.markdown('#')
    # For detection via webcam live feed
    if selected == 'Live Detection':
        if st.button('Live Detection'):
            waiting_text.text("Please press 'q' to exit...")
            requests.post('http://127.0.0.1:8080/live', 
            data = {"WRITE_PATH": 1})   
            #st.image(Image.open(predict.json()))
            while cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
