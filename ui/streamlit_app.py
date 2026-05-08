import streamlit as st
import requests
import os

if "API_URL" in st.secrets:
    API_BASE_URL = st.secrets["API_URL"]
else:
    API_BASE_URL = os.getenv("API_URL", "http://localhost:8000/api")

st.set_page_config(page_title="AI Resume Parser", layout="wide")
st.title("📄 AI Resume Parser")

st.sidebar.header("Upload Document")
uploaded_file = st.sidebar.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx","doc"])

if uploaded_file and st.sidebar.button("Extract Data", type="primary"):
    with st.spinner("Parsing document via Ollama..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post(f"{API_BASE_URL}/upload", files=files)
            
            if response.status_code == 201:
                result = response.json()
                data = result["data"]
                
                st.success(f"Parsing Complete! Document ID: `{result['document_id']}`")
                
                tab1, tab2, tab3 = st.tabs(["Overview", "Experience & Education", "Raw JSON"])
                
                with tab1:
                    contact = data.get("contact_information", {})
                    col1, col2 = st.columns(2)
                    col1.markdown(f"**Name:** {contact.get('name')}")
                    col1.markdown(f"**Email:** {contact.get('email')}")
                    col2.markdown(f"**Phone:** {contact.get('phone')}")
                    col2.markdown(f"**Location:** {contact.get('location')}")
                    
                    st.divider()
                    st.subheader("Summary")
                    st.write(data.get("summary") or "N/A")
                    
                    st.subheader("Skills")
                    st.write(", ".join(data.get("skills", [])) or "N/A")

                with tab2:
                    st.subheader("Work Experience")
                    for exp in data.get("work_experience", []):
                        with st.expander(f"{exp.get('role')} at {exp.get('company')} ({exp.get('duration')})", expanded=True):
                            for resp in exp.get("responsibilities", []):
                                st.markdown(f"- {resp}")
                                
                    st.subheader("Education")
                    for edu in data.get("education", []):
                        st.markdown(f"**{edu.get('degree')}** | {edu.get('institution')} ({edu.get('year')})")

                with tab3:
                    st.json(result)
            else:
                st.error(f"Error: {response.json().get('detail')}")
                
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")