import streamlit as st
import cv2
import numpy as np
import os
import shutil
from core.vision_engine import preprocess_image
from core.ocr_engine import extract_structured_text
from core.data_parser import parse_document_context

st.set_page_config(
    page_title="Enterprise IDP & OCR Engine",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Enterprise Intelligent Document Processing (IDP) Platform")
st.markdown("---")

st.sidebar.header("⚙️ Pipeline Configuration")

processing_mode = st.sidebar.radio(
    "Select Document Ingestion Method:",
    ["Option 1: System Default Mock (sample.png)", "Option 2: Upload Custom Document Asset"]
)

target_file_path = None
is_ready_to_process = False

if "Option 1" in processing_mode:
    default_mock_path = "sample.png"
    if os.path.exists(default_mock_path):
        st.sidebar.success("✅ Mock reference matrix 'sample.png' loaded.")
        target_file_path = default_mock_path
        is_ready_to_process = True
    else:
        st.sidebar.error("❌ 'sample.png' not found in root directory.")
        
else:
    uploaded_file = st.sidebar.file_uploader(
        "Upload custom document asset:", 
        type=["png", "jpg", "jpeg", "tiff"]
    )
    if uploaded_file is not None:
        temp_filename = f"temp_{uploaded_file.name}"
        with open(temp_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
        target_file_path = temp_filename
        is_ready_to_process = True

col1, col2 = st.columns(2)

if is_ready_to_process and target_file_path is not None:
    with st.spinner("Executing Computer Vision Filters & Running OCR engine..."):
        try:
            cleaned_matrix = preprocess_image(target_file_path)
            raw_text_stream, low_confidence_registry = extract_structured_text(cleaned_matrix)
            
            # Key Change: Passing the cleaned image matrix into the third positional parameter slot
            final_json_payload = parse_document_context(raw_text_stream, low_confidence_registry, cleaned_matrix)
            
            with col1:
                st.subheader("🖼️ Processed Image Grid Visualizer")
                display_img = cv2.cvtColor(cleaned_matrix, cv2.COLOR_GRAY2RGB)
                st.image(display_img, caption="Enhanced Contrast Matrix Layer sent to OCR core", use_container_width=True)
                st.subheader("📦 Final Structured JSON Data Output")
                st.json(final_json_payload)

            with col2:
                st.header("📝 Raw OCR Extracted Text Payload")
                if raw_text_stream.strip():
                    st.text_area(label="Translated Text Strings Output", value=raw_text_stream, height=350)
                else:
                    st.warning("OCR Engine returned empty token array strings.")
                    
                st.subheader("⚠️ Human-in-the-Loop Risk Verification")
                if final_json_payload["idp_validation_flags"]["low_confidence_detected"]:
                    st.error("Low-confidence tokens captured! Manual review required.")
                    st.dataframe(low_confidence_registry)
                else:
                    st.success("All character extraction vectors verified over 50% safety margin.")

        except Exception as e:
            st.error(f"Execution Error within pipeline pipelines: {str(e)}")
            
        finally:
            if target_file_path.startswith("temp_") and os.path.exists(target_file_path):
                os.remove(target_file_path)
else:
    with col1:
        st.info("👈 Please select a method or upload a file in the sidebar portal to trigger processing.")
