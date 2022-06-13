
import streamlit as st
import matplotlib.pyplot as plt

from PIL import Image

def load_image(image_file):
	img = Image.open(image_file)
	return img


def image_processing():
    st.subheader("Image")
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
    if image_file is not None:

        # To See details
        file_details = {"filename":image_file.name, "filetype":image_file.type,
                            "filesize":image_file.size}
        st.write(file_details)

        # To View Uploaded Image
        st.image(load_image(image_file))
        img = load_image(image_file)

        # Add to flip button here (preprocessing steps)
        # Add preprocessing button here
        rotated_img = img.rotate(180) #Number of degree's
        fig = plt.figure()
        plt.imshow(rotated_img)
        plt.axis("off")
        st.pyplot(fig)

def main():
    selected_box = st.sidebar.selectbox(
    'Choose one of the following',
    ('Image Processing',)
    )
    
    if selected_box == 'Image Processing':
        image_processing()

if __name__ == "__main__":
    main()