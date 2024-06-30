import streamlit as st
import os
import PyPDF2
from langchain_mistralai.chat_models import ChatMistralAI
import json
from dotenv import load_dotenv
from PIL import Image
import pytesseract
import time

load_dotenv()

# Set up the Mistral AI client
mistral_api_key = os.getenv("MISTRAL_API_KEY")
client = ChatMistralAI(api_key=mistral_api_key)

# Define the input prompts
input_prompt1 = """
You are an skilled Applicant Tracking System scanner with a deep understanding of Applicant Tracking System functionality,
your task is to evaluate the resume against the provided job description.
Show  a single percentage reflecting the overall match between resume and job description.
"""

input_prompt2 = """
You are an skilled Applicant Tracking System scanner with a deep understanding of Applicant Tracking System functionality,
your task is to evaluate the resume against the provided job description.
Find out the requirements the make this resume disqualified for this job in a list.
"""

input_prompt3 = """
You are an skilled Applicant Tracking System scanner with a deep understanding of Applicant Tracking System functionality,
your task is to evaluate the resume against the provided job description.
Find out the most critical keywords in the resume that match the job description in a list.
"""

input_prompt4 = """
You are submitting a resume to a job with the provided job description.
Find out the requirements in the job description you should add to make you qualify for this job.
"""

input_prompt5 = """
You are the applicant who applied for this job and want to compose a strong but concise coverletter to convince the employer you have the skills and the expereince for this job.
The first paragraph of the  cover letter must briefly discuss the your backgroud.
The second paragraph discuss how the applicant fit this role based on your skillsets matches the job requirements.
The third paragraph discuss the your interest in this role and thanks for the consideration .
"""

# Define a function to extract text from a PDF file
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

# Set up the Streamlit app
st.set_page_config(page_title="Resume Match Maker", page_icon=":robot:", layout="wide")

# Add a header to the app
st.header("Resume Match Maker")
st.markdown("## Created by Gokul Palanisamy")

# Add a ticker to the app
st.markdown("""<div style='position:fixed;bottom:0;left:0;background-color:#222;color:#fff;padding:10px;border-radius:5px;'>
                  <marquee behavior="scroll" direction="left">Resume Match Maker helps you match your resume to job descriptions and generate cover letters. Created by Gokul Palanisamy.</marquee>
               </div>""", unsafe_allow_html=True)

# Add a sidebar to the app
with st.sidebar:
    st.markdown("# Resume Match Maker")
    st.markdown("## Match your resume to job descriptions and generate cover letters")

# Add input fields for job description and resume
use_image = st.checkbox("Use Image for Job Description")

if use_image:
    job_description_image = st.file_uploader("Upload Job Description Image", type=["jpg", "jpeg", "png"])
    if job_description_image:
        # Perform OCR on the image
        image = Image.open(job_description_image)
        gray_image = image.convert("L")
        job_description = pytesseract.image_to_string(gray_image)
    else:
        job_description = ""
else:
    job_description = st.text_area("Enter Job Description", value="")

st.markdown("## Upload Resume")
resume = st.file_uploader("", type="pdf")

# Add a button to generate results
if st.button("Generate Results"):
    # Display a loading spinner while the results are being generated
    with st.spinner("Generating results..."):
        # Display a progress bar while the results are being generated
        progress_bar = st.progress(0)

        # Extract text from the resume
        if resume:
            resume_text = extract_text_from_pdf(resume)
        else:
            st.error("Please upload a resume.")
            resume_text = ""

        # Generate results using Mistral AI
        if job_description and resume_text:
            # Match percentage
            response1 = client.invoke(input_prompt1 + resume_text + job_description)
            progress_bar.progress(20)
            time.sleep(0.5)

            # Disqualifying factors
            response2 = client.invoke(input_prompt2 + resume_text + job_description)
            progress_bar.progress(40)
            time.sleep(0.5)

            # Matching keywords
            response3 = client.invoke(input_prompt3 + resume_text + job_description)
            progress_bar.progress(60)
            time.sleep(0.5)

            # Missing keywords
            response4 = client.invoke(input_prompt4 + resume_text + job_description)
            progress_bar.progress(80)
            time.sleep(0.5)

            # Cover letter
            response5 = client.invoke(input_prompt5 + resume_text + job_description)
            progress_bar.progress(100)
            time.sleep(0.5)

            # Display the results
            st.markdown("## Match Percentage")
            st.markdown(f'* {response1.content}')

            st.markdown("## Disqualifying Factors")
            st.markdown(f'* {response2.content}')

            st.markdown("## Matching Keywords")
            st.markdown(f'* {response3.content}')

            st.markdown("## Missing Keywords")
            st.markdown(f'* {response4.content}')

            st.markdown("## Cover Letter")
            st.markdown(f'* {response5.content}')

        else:
            st.error("Please enter a job description and upload a resume.")
