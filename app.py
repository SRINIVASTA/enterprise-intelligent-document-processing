import streamlit as st
import cv2
import numpy as np
import os
from core.vision_engine import preprocess_image
from core.ocr_engine import extract_structured_text
from core.data_parser import parse_document_context

# Configure Web Page metadata
st.set_page_config(
    page_title="Enterprise IDP & OCR Engine",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Enterprise Intelligent Document Processing (IDP) Platform")
st.markdown("---")

# Setup layout blocks: Left column for operations, Right column for raw text tracking
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Document Input Subsystem")
    uploaded_file = st.file_uploader(
        "Upload a noisy document or invoice screenshot...", 
        type=["png", "jpg", "jpeg", "tiff"]
    )

if uploaded_file is not None:
    # 1. Temporarily buffer incoming stream payload to disk node
    temp_filename = f"temp_{uploaded_file.name}"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.success("File securely uploaded and buffered successfully!")

    # 2. Trigger Core Engine Processing Pipes
    with st.spinner("Executing Computer Vision Filters & Running OCR engine..."):
        try:
            # OpenCV Layer
            cleaned_matrix = preprocess_image(temp_filename)
            
            # OCR Engine Layer
            raw_text_stream, low_confidence_registry = extract_structured_text(cleaned_matrix)
            
            # Parsing Analytics Layer
            final_json_payload = parse_document_context(raw_text_stream, low_confidence_registry)
            
            # 3. Render Visual Analytics Panels
            with col1:
                st.subheader("🖼️ Processed Image Grid Visualizer")
                # Convert grayscale matrix back to RGB channel sequence for screen mapping
                display_img = cv2.cvtColor(cleaned_matrix, cv2.COLOR_GRAY2RGB)
                st.image(display_img, caption="Cleaned Image Layer sent to OCR engine", use_container_width=True)
                
                st.subheader("📦 Final Structured JSON Data Output")
                st.json(final_json_payload)

            with col2:
                st.header("📝 Raw OCR Extracted Text Payload")
                if raw_text_stream.strip():
                    st.text_area(label="Translated Text Strings Output", value=raw_text_stream, height=350)
                else:
                    st.warning("OCR Engine returned empty token array strings.")
                    
                # Highlight active error-handling validation parameters
                st.subheader("⚠️ Human-in-the-Loop Risk Verification")
                if final_json_payload["idp_validation_flags"]["low_confidence_detected"]:
                    st.error("Low-confidence tokens captured! Verification required.")
                    st.dataframe(low_confidence_registry)
                else:
                    st.success("All character extraction vectors verified over 50% safety margin.")

        except Exception as e:
            st.error(f"Execution Error within pipeline pipelines: {str(e)}")
            
        finally:
            # Cleanup storage matrix vectors to maintain container stateless profiles
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
