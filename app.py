import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv() # helps to load all the env variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



def get_gemini_response(input_prompt,image ):
    model=genai.GenerativeModel("gemini-pro-vision")
    response=model.generate_content([input_prompt ,image[0]])
    return response.text




def input_image_setup(uploaded_file):
    # checking if the file is uploaded or not
    if uploaded_file is not None:
        # reading files into bytes
        bytes_data=uploaded_file.getvalue()


        image_parts=[
            {
                "mime_type":uploaded_file.type, # getting mime type of the uploaded file
                "data":bytes_data
            }
        ]
        return image_parts  
    else:
        raise FileNotFoundError("No file uploaded")
    


    

# initializing streamlit app
st.set_page_config(page_title="NutriScan")

st.header("NutriScan")
uploaded_file=st.file_uploader("choose an image..",type=["jpg","jpeg","png"])
image="none"
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="uploaded image",use_column_width=True)
submit = st.button("Calculate nutritional values")



input_prompt="""  
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
        finally you can also mention weather the food is healthy or not and also mention the 
        percentage slpit of ratio of carbohydrates,fats, fiber, sugar and all other important macros 
        in our diet according to 100 grams 

"""


if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.header("The response is")
    st.write(response)











