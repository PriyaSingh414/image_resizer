from PIL import Image
import io
import streamlit as st
import numpy as np
import cv2

base = "dark"
primaryColor = "#1DB954"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

import streamlit as st
hide_streamlit_cloud_elements = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    a[title="View source"] {display: none !important;}
    button[kind="icon"] {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_cloud_elements, unsafe_allow_html=True)
def format_bytes(size):
    for unit in ['Bytes', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

st.header("Welcome To Resize Your Image")
img=st.file_uploader("Upload Your Image",type=["jpeg","jpg","png"])
if img:
    original_size = len(img.getvalue())
    img=Image.open(img).convert("RGB")
    arr_img=np.array(img)
    st.subheader("🖼️ Original Image:")
    st.image(arr_img,caption="Original Image", use_container_width=True)
    st.markdown(f"📦 **Original File Size:** `{format_bytes(original_size)}`")


    width=st.number_input("Enter width",min_value=1,value=arr_img.shape[1])
    height=st.number_input("Enter height",min_value=1,value=arr_img.shape[0])
    flip_value=st.selectbox("Flip Image", ["None", "Horizontal", "Vertical", "Both"])
    if flip_value == "Horizontal":
        flipped = cv2.flip(arr_img, 1)
        arr_img=flipped
    elif flip_value == "Vertical":
        flipped = cv2.flip(arr_img, 0)
        arr_img=flipped
    elif flip_value == "Both":
        flipped = cv2.flip(arr_img, -1)
        arr_img=flipped
    st.image(arr_img,caption="fliped iamge",)
    if st.button("Resize"):
        resize_image=cv2.resize(arr_img,(int(width),int(height)))

        st.image(resize_image, caption="Resized Image", use_container_width=True)

        
        image_pil=Image.fromarray(resize_image)
        buff=io.BytesIO()
        image_pil.save(buff, format="jpeg")
        resized_size = len(buff.getvalue())
        st.success(f"📦 Resized File Size: {format_bytes(resized_size)}")
        st.download_button(
            label="📥 Download Resized Image",
            data=buff.getvalue(),
            file_name="resized_image.jpeg",
            mime="image/png"
        )
