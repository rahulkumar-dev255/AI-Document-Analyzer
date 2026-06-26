import streamlit as st
import PyPDF2
from google import genai
from fpdf import FPDF

# PDF banane ka function
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Text ko PDF mein likho
    pdf.multi_cell(0, 10, txt=text.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# Nayi library ka client
client = genai.Client(api_key="AQ.Ab8RN6IZPj044f_qrvuvNKMPyfqmwkep5r91_fJXzmD37YVwhQ")

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
    
    # if st.button("Analyze Karo"):
    #     with st.spinner("AI analyze kar raha hai..."):
    #         try:
    #             # Sahi model name (gemini-3.5-flash)
    #             response = client.models.generate_content(
    #                 model="gemini-2.5-flash",
    #                 contents=f"You are an expert. Extract Imprtant points   from this text. ANSWER IN ENGLISH ONLY. Document text: {text}"
    #             )
    #             analysis_text =  response.text
    #             st.markdown("Analysis Report:")
    #             # st.markdown(response.text)
    #             # st.sidebar
    #             st.markdown(analysis_text)
    #             st.success("Analysis complete!")

    #         except Exception as e:
    #             st.error(f"Error: {e}")

    #             # st.download_button("Download Report", response.text, file_name="analysis.txt")
    #             st.download_button("Download Report", response.text, file_name="analysis.txt")