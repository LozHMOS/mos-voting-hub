import streamlit as st
from utils.db import insert_idea
import pypdf

st.title("📤 Submit New Idea")

name = st.text_input("Application name")
description = st.text_area("Short description")
demo_link = st.text_input("Demo link (URL)")

uploaded_file = st.file_uploader("Upload readme or supporting information (markdown, text or PDF)", type=["md", "txt", "pdf"])

if st.button("Submit Idea"):
    if name and description:
        readme_content = ""
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                pdf_reader = pypdf.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    readme_content += page.extract_text() + "\n"
            else:
                readme_content = uploaded_file.getvalue().decode("utf-8")
        
        voter = st.session_state.get("voter_name", "Unknown")
        idea_id = insert_idea(name, description, readme_content, demo_link, voter)
        if idea_id:
            st.success(f"Idea '{name}' submitted successfully!")
            st.rerun()
    else:
        st.error("Name and description are required.")