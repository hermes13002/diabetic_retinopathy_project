import os 
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
import tensorflow as tf
from tensorflow import keras
import numpy as np
from model import predict_image
from tensorflow.keras.models import load_model




# ==================== Configure Streamlit page ==================== #

st.set_page_config(
    page_title="SA App",
    page_icon=":bar_chart:",
    layout="wide",
)


# ==================== Styling ==================== #


st.markdown(
    """
    <style>
        .title-text {
            background: linear-gradient(to right, #ff69b4, #9400d3); /* Vibrant pink/purple gradient */
            color: white; /* White text for the header */
            padding: 25px; /* Increased padding for more space */
            text-align: center;
            border-radius: 10px; /* Rounded corners for a softer look */
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1); /* Subtle shadow for depth */
        }
        
        .title-text h1{
            font-size: 3rem; /* Larger font size for the header */
        }
        
        .stApp {
            background-color: #FFFFFF; 
            padding: 10px;
            margin: 15px
        }
        
        .footer{
            background-color: #A52A2A;
            color: #FFFFFF;
            padding: 5px;
            position; fixed;
            text-align: center;
            bottom: 0;
            width: 100%;
            height: 50px;
        }
        
    </style>
    """,
    unsafe_allow_html=True
    )



# ==================== Header ==================== #

st.markdown("""
            <div class="title-text">
            <h1>Automated Detection of Diabetic Retinopathy</h1>
            </div>
            """, 
            unsafe_allow_html=True
            )




# ==================== Spacing ==================== #
st.markdown("&nbsp;", unsafe_allow_html=True)




# ==================== Styling ==================== #

st.markdown(
    """
    <style>
        .about-text, .get-started-section {
            # background-color: #fff; /* White background */
            border: 1px solid #ddd; /* Subtle border */
            padding: 25px; /* More padding for better readability */
            border-radius: 10px; /* Rounded corners for a softer look */
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1); /* Subtle shadow for depth */
        }

        .about-text h2, .get-started-section h3 {
            color: #fffff;
            margin-bottom: 15px;
        }

        .about-text p, .get-started-section p {
            line-height: 1.5;
        }
    </style>
    """,
    unsafe_allow_html=True,
)




# ==================== About the App Section =================== #


with st.container():
    
    with st.expander("About the App"):
        
        st.markdown(
            """
            <div class="about-text">
                <p>
                This application automates the detection and grading of Diabetic Retinopathy (DR) using machine learning and computer vision. It analyzes retinal fundus images to provide 
                accurate, consistent, and efficient identification of DR severity, supporting early intervention and personalized treatment. By leveraging these techniques, it addresses 
                challenges posed by subjective assessments and manual labor in existing methods. The model, fine-tuned using Convolutional Neural Networks, achieves an impressive 96%
                accuracy and recall score, ensuring effective detection of diabetic retinopathy cases amidst rising diabetes prevalence and ophthalmologist shortages.
                </p>            
            </div>
            """,
            unsafe_allow_html=True
            )
        
        
        

# ==================== Get Started Section =================== #

with st.container():
    st.markdown(
        """
        <div class="get-started-section">
            <h3>Get Started</h3>
            <p>
            Just upload your retinal fundus image, and the system will quickly analyze it to detect and grade the presence of Diabetic Retinopathy (DR) along with the percentage level of 
            confidence.
            </p>
        </div>
        """,
        unsafe_allow_html=True
        )




# ==================== Spacing ==================== #
st.markdown("&nbsp;")
st.markdown("&nbsp;")




# ==================== Create Tabs ==================== #

# tab1, tab2 = st.tabs(["🎯 Objectives", "🎯 App Features"])

# Define tabs with emojis
tab1, tab2 = st.columns(2)

# Objectives tab
with tab1:
    st.write("🎯 Objectives")
    with st.expander("Click to see objectives"):
        st.markdown(
            """
            <ul>
                <li>Automate the detection of Diabetic Retinopathy (DR) using machine learning and computer vision.</li>
                <li>Enhance accuracy in identifying different stages and severity levels of DR from retinal fundus images.</li>
                <li>Support early intervention by providing timely and reliable screening results.</li>
                <li>Reduce reliance on subjective assessments and manual labor for DR diagnosis.</li>
                <li>Address challenges posed by the increasing prevalence of diabetes and the shortage of ophthalmologists.</li>
                <li>Develop a robust and scalable system for DR detection and grading.</li>
                <li>Enable personalized treatment plans based on precise DR severity assessments.</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

# Features tab
with tab2:
    st.write("📱 App Features")
    with st.expander("Click to see features"):
        st.markdown(
            """
            <ul>
                <li>Upload retinal fundus images for DR analysis.</li>
                <li>Utilize machine learning and computer vision techniques for analysis.</li>
                <li>Display accurate detection results and severity grading.</li>
                <li>Provide confidence level in DR detection.</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )










































# ==================== Image Input Section ==================== #


# File Uploader
uploaded_images = st.file_uploader("Upload retinal fundus images for analysis", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Display Uploaded Image and Classification Results
if uploaded_images is not None:
    
    # Loop through the uploaded images.
    for uploaded_image in uploaded_images:
        
        if uploaded_image.type in ["image/jpg", "image/jpeg", "image/png"]:
    
            # Display loading spinner
            with st.spinner('Classifying...'):
                
                image = Image.open(uploaded_image)
                st.image(image, caption="Uploaded Image")
            
                # Save the uploaded image to the working directory.
                image_path = os.path.join("diabetic_retinopathy_dataset", "uploaded_image.jpg")
                image.save(image_path)
                
                # The classes to be predicted.
                classes = ["Presence of Diabetic Retinopathy [DR]", "Absence of Diabetic Retinopathy [NO-DR]"]
                
                # Load the model.
                model = load_model("model-folder/diabetic-retino-model.h5")
            
            
                # Perform prediction on the patient's image.
                confidence_level = predict_image(model=model, image_path=image_path)
                
                # Define the binary class.
                binary_class = ["DR", "NO-DR"]
            
                if confidence_level >= 0.5:
                    
                    label = 1
                    # Display predicted class and confidence score.
                    st.write("This patient is likely to be", classes[label])
                    
                    # confidence_level = np.round(confidence_level, 4)* 100
                    score = list(confidence_level[0][0])
                    st.write(f"Model's Confidence Score: {round(score, 4) * 100}%")
            
                else: 
                    
                    label = 0
                    # Display predicted class and confidence score.
                    st.write("This patient is likely to be", classes[label])
                    
                    # confidence_level = (1 - np.round(confidence_level, 4) ) * 100
                    score = list(confidence_level[0][0])
                    st.write(f"Model's Confidence Score: {round(score, 4) * 100}%")
                
            
                # # Display bar chart.
                # confidence_scores = [np.round(1 - confidence_level, 4), np.round(confidence_level, 4)]
                
                # st.bar_chart(pd.DataFrame({
                #     'Confidence': confidence_scores
                #     }, index=binary_class))
                    
                
                # Delete the model path after making prediction.
                os.remove(image_path)
        
        
       
            
            
        else:
            st.error("Please upload a JPG or JPEG or PNG image.", icon="🔴")


st.markdown("&nbsp;", unsafe_allow_html=True)
st.markdown("&nbsp;", unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)  # Adding a single line break


# ----------------------------------Footer----------------------------------------#


st.markdown(
    """
    <div class="footer"> 
    <p>Copyright 2024 &copy;</p>
    </div>
    """, 
    unsafe_allow_html=True
)





#-------------------------------Add styling to sidebar using CSS styling.------------------------------------#
st.markdown(
    """
    <style>
        .sidebar .sidebar-content{
            background-color: #FFFFFF;
        }
        .h1{
            color: #A52A2A;
            font-size: 16px;
        } 
        .header{
            color: #A52A2A
        } 
        .info {
            padding: 20px;
            border-radius: 10px;
            font-size: 12px;
            background-color: #D3D3D3;
            color: #000000;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .sidebar-close {
            color: #666666; /* Dark Gray */
        }
        .feedback {
            background-color: #D3D3D3;
            font-size: 12px;
            color: #A52A2A;
            padding: 5px;
            margin-top: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            height: 70px;
        
            
        }
    </style>
    """,
    unsafe_allow_html=True
)


# # Define the sidebar content using Streamlit's layout components.
# st.sidebar.markdown(
#     """
#     <div class="info">
#         <h1 class="h1">About</h1>
#         <p>
#         This web application automates the detection and grading of Diabetic Retinopathy (DR) using machine learning and computer vision. By analyzing retinal fundus images, it aims to provide
#         accurate, consistent, and efficient identification of DR severity, supporting early intervention and personalized treatment. This addresses the rising diabetes prevalence and 
#         ophthalmologist shortage, enhancing timely and reliable screening and diagnosis.
#         </p>
#         <h2 class="header">Purpose</h2>
#         <p>
#         The purpose of this project is to demonstrate the capabilities of machine learning in image classification and to provide a practical example of how machine learning can be applied 
#         to real-world problems.
#         </p>
#         <h2 class="header">Contributors</h2>
#         <p>
#         <a href="https://github.com/TolaniSilas" target="_blank">Osunba Silas Tolani</a>
#         </p>
#         <p>
#         <a href="https://github.com/TolaniSilas" target="_blank">Soares Ayoigbala</a>
#         </p>
#         <p>
#         <a href="https://github.com/TolaniSilas" target="_blank">Ogundipe Elijah</a>
#         </p>        
#         <h2 class="header">Acknowledgments</h2>
#         <p>I'd like to thank the Streamlit community for their support and the developers of the underlying libraries used in this project.</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )



# st.sidebar.markdown("""
#     <div class="feedback">
#         <h1 class="header">Feedback</h1>
#     </div>
# """, unsafe_allow_html=True)

# feedback = st.sidebar.text_area("Please share your feedback here:", max_chars=500)

# if st.sidebar.button("Submit"):
#     # Process the feedback (you can save it to a database or send it via email)
#     st.sidebar.success("Thank you for your feedback! It has been submitted successfully.")


