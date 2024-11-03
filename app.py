from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Set the page configuration at the very beginning
st.set_page_config(page_title="Gemini Image Demo", page_icon="smiley")

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro Model and Get Responses
def get_gemini_response(user_input, image):
    if user_input != "":
        model = genai.GenerativeModel("gemini-1.5-flash")  # Load the Gemini 1.5 vision model for images
        try:
            # Make sure to handle image input properly, some APIs require separate handling
            if image:
                response = model.generate_content([user_input, image])  # Generating content using input and image
            else:
                response = model.generate_content([user_input])  # If there's no image, just send the input text

            return response.text  # Accessing the response properly
        except AttributeError as e:
            return f"Error: {e}. Please check the API documentation for the correct method."
        except TypeError as e:
            return f"Error: {e}. Please check the response format."
    else:
        return "Please provide valid input."

# Background styling
page_bg = """
<style>
.stApp {
    background-image: url("https://wallpapercave.com/wp/wp7335926.png");
    background-size: cover;
    background-position: center;
    color: white;  /* Set default font color */
}
.sidebar .sidebar-content {
    background-color: rgba(0, 0, 0, 0.7);  /* Semi-transparent sidebar background */
}
header {
    color: #FFC107;  /* Header color */
}
</style>
"""

# Injecting CSS
st.markdown(page_bg, unsafe_allow_html=True)

# Initialize the Streamlit App
st.header("Gemini LIM Application")

user_input = st.text_input("Input:", key="input")

uploaded_file = st.file_uploader("Choose an Image...", type=["jpg", "jpeg", "png", "pdf"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the Image")

# When Submit is clicked
if submit:
    if user_input:  # Check if there is an input
        response = get_gemini_response(user_input, image)  # Corrected the function call
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please enter a question.")
