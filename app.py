## Invoice Extractor

#it will help us to load all my environment variables
from dotenv import load_dotenv

#load all environment variables from .env
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

## Configuring API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro vision model and get response
def get_gemini_response(input,image,prompt):
    ##call my model (loading the gemini model)
    model=genai.GenerativeModel('gemini-pro-vision')

    #get the response
    response=model.generate_content([input,image[0],prompt])

    #return the response
    return response.text


## function to get the image data in terms of Byte
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data =uploaded_file.getvalue()  #convert into bytes

        image_parts =[
            {
                "mime_type":uploaded_file.type, # Get the mime type of uploaded file
                "data":bytes_data
            }
        ]
        return image_parts
    else :
        raise FileNotFoundError("No file uploaded")
    

## Create our streamlit app
#PAge title
st.set_page_config(page_title="Invoice Extractor")
st.header("Gemini Application")
# text box is my input
input=st.text_input("Input Prompt: ", key="input")

#uploaded file can be any type jpg,png,jepg
uploaded_file= st.file_uploader("Choose an image....", type =["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    # open the uploaded file
    image=Image.open(uploaded_file)
    #display the file
    st.image(image,caption="Uploaded Image.",use_column_width=True)

# create the submit button
submit=st.button("Tell me about the invoice ")




## Give my input prompt how my Gemini pro model behave
input_prompt="""
You are an expert in understanding invoices.You will recieve input images as invoices and you will have to answer questions based on the input image.
"""


## If submit button is clicked then imageinfo and prompt hit to the gemini model
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image,input) #get the response


    #display the response
    st.subheader("The Response is")
    st.write(response)