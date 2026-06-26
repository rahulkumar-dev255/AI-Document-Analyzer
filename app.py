import streamlit as st
import PyPDF2
from google import genai
from fpdf import FPDF
import os


# PDF banane ka function
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Text ko PDF mein likho
    pdf.multi_cell(0, 10, txt=text.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')


api_key = st.secrets["GOOGLE_API_KEY"]
client = genai.Client(api_key=api_key)


st.title("AI Document Analyzer")

uploaded_file = st.file_uploader("PDF upload karo", type=["pdf"])

if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    if st.button("Analyze Karo"):
      with st.spinner("Analyzing..."):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=f"You are an expert. Extract points from: {text}"
            )
            analysis_text = response.text
            
            st.subheader("Analysis Report:")
            st.markdown(analysis_text) # Output dikhao
            
            # Ab download button yahan ayega
            pdf_data = create_pdf(analysis_text)
            st.download_button(
             label="📥 PDF Report Download Karo",
              data=pdf_data,
              file_name="analysis_report.pdf",
               mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error: {e}")    
    
   
