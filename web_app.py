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



# Title and Description
st.markdown(
    """
    <style>
        .title-text {
            font-size: 50px;
            font-weight: bold;
            color: #A52A2A;
            margin-bottom: 20px;
        }
        .description-text {
            font-size: 16px;
            color: #FFE4B5;
            margin-bottom: 30px;
            padding: 15px;
            background-color: #333333
        }
        .stApp {
            background-color: #CCCCCC; 
            padding: 20px;
            margin: 15px
        }
        .footer{
            background-color: #A52A2A;
            color: #FFFFFF;
            padding: 5px;
            position; fixed;
            text-align: center;
            bottom: 0;
            width: 100%
        }
    </style>
    """,
    unsafe_allow_html=True
)



st.markdown("<h1 class='title-text'>Animal Classifier Model</h1>", unsafe_allow_html=True)
st.markdown(
    """<p class='description-text'>The existing methods for detecting and grading Diabetic Retinopathy (DR) often rely on subjective assessments and extensive manual labor, leading to 
    inefficiencies and potential inconsistencies in diagnosis. The increasing prevalence of diabetes and the limited availability of ophthalmologists further exacerbate the challenges in 
    timely screening and diagnosis. Therefore, there is a need to develop a robust and reliable automated system that can accurately detect and grade diabetic retinopathy, enabling early 
    intervention and personalized treatment plans. This project aims to address this challenges by leveraging machine learning and computer vision techniques. The proposed system will take 
    fundus images of the retina as input and automatically detect the presence of diabetic retinopathy. The system will also grade the severity of the condition, providing clinicians with 
    valuable information for treatment planning.</p>""",
    unsafe_allow_html=True
)


# File Uploader
uploaded_image = st.file_uploader("Upload an image:", type=["jpg", "jpeg"])

# Display Uploaded Image and Classification Results
if uploaded_image is not None:
    if uploaded_image.type in ["image/jpg", "image/jpeg"]:
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
            model = load_model("model-folder\diabetic-retino-model.h5")
        
        
            # Perform prediction on the patient's image.
            label, confidence_level = predict_image(model=model, image_path=image_path)
            
            # Define the binary class.
            binary_class = ["DR", "NO-DR"]
            
            if confidence_level >= 0.5:
                
                # Display predicted class and confidence score.
                st.write("This patient is likely to be:", classes[label])
                st.write(f"Model's Confidence Score: {round(confidence_level, 4) * 100}%")
            
                
            
            else: 
                
                # Display predicted class and confidence score.
                st.write("This patient is likely to be:", classes[label])
                st.write(f"Model's Confidence Score: {(1 - round(confidence_level, 4) ) * 100}%")
            
          
            # Display bar chart.
            confidence_scores = [round(1 - confidence_level, 4), round(confidence_level, 4)]
            
            st.bar_chart(pd.DataFrame({
                'Confidence': confidence_scores
                }, index=binary_class))
                  
            
            # Delete the model path after making prediction.
            os.remove(image_path)
            
            
    else:
        st.error("Please upload a JPG or JPEG image.", icon="🔴")





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
            padding: 20px;
            margin-top: 20px
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Define the sidebar content using Streamlit's layout components.
st.sidebar.markdown(
    """
    <div class="info">
        <h1 class="h1">About</h1>
        <p>
        This web application aims to develop an automated system for detecting and grading Diabetic Retinopathy (DR) using machine learning and computer vision techniques. Current methods
        rely on subjective assessments and manual labor, leading to inefficiencies and inconsistencies. By analyzing retinal fundus images, the system will accurately identify the presence
        and severity of DR, aiding in early intervention and personalized treatment plans. This addresses the growing prevalence of diabetes and the shortage of ophthalmologists, enhancing
        timely and reliable screening and diagnosis.
        </p>
        <h2 class="header">Purpose</h2>
        <p>
            The purpose of this project is to demonstrate the capabilities of 
            machine learning in image classification and to provide a practical 
            example of how machine learning can be applied to real-world problems.
        </p>
        <h2 class="header">Contributor</h2>
        <p>
            Osunba Silas Tolani
        </p>
        
        
        <h2 class="header">Acknowledgments</h2>
        <p>
            I'd like to thank the Streamlit community for their support 
            and the developers of the underlying libraries used in this project.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)



st.sidebar.markdown("""
    <div class="feedback">
        <h1 class="header">Feedback</h1>
    </div>
""", unsafe_allow_html=True)

feedback = st.sidebar.text_area("Please share your feedback here:", max_chars=500)

if st.sidebar.button("Submit"):
    # Process the feedback (you can save it to a database or send it via email)
    st.sidebar.success("Thank you for your feedback! It has been submitted successfully.")


