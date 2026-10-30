import streamlit as st
import cv2
import numpy as np
import os
import shutil
import json
import pandas as pd
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

# ==============================================================================
# ⚙️ SIDEBAR CONFIGURATION PORTAL
# ==============================================================================
st.sidebar.header("⚙️ Pipeline Configuration")

processing_mode = st.sidebar.radio(
    "Select Document Ingestion Method:",
    ["Option 1: System Default Mock (sample.png)", "Option 2: Upload Files (Supports Single or Bulk Uploads)"]
)

target_files = []  # Array list to manage processing queues
is_ready_to_process = False

if "Option 1" in processing_mode:
    default_mock_path = "sample.png"
    if os.path.exists(default_mock_path):
        st.sidebar.success("✅ Mock reference matrix 'sample.png' loaded.")
        target_files.append({"path": default_mock_path, "name": "sample.png", "is_temp": False})
        is_ready_to_process = True
    else:
        st.sidebar.error("❌ 'sample.png' not found in root directory.")
        
else:
    # Key Change: accept_multiple_files=True allows users to select 1 or up to 50 documents at once
    uploaded_files = st.sidebar.file_uploader(
        "Upload custom document asset(s):", 
        type=["png", "jpg", "jpeg", "tiff"],
        accept_multiple_files=True
    )
    if uploaded_files:
        for uploaded_file in uploaded_files:
            temp_filename = f"temp_{uploaded_file.name}"
            with open(temp_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())
            target_files.append({"path": temp_filename, "name": uploaded_file.name, "is_temp": True})
        is_ready_to_process = True

# ==============================================================================
# 📊 MAIN DASHBOARD VIEWPORTS
# ==============================================================================
col1, col2 = st.columns(2)

if is_ready_to_process and target_files:
    bulk_results_summary = []
    
    # Run the core processing loop iteratively over the queued assets
    for idx, file_node in enumerate(target_files):
        with st.spinner(f"Processing ({idx + 1}/{len(target_files)}): {file_node['name']}..."):
            try:
                # 1. Trigger Core Engine Processing Pipes
                cleaned_matrix = preprocess_image(file_node["path"])
                raw_text_stream, low_confidence_registry = extract_structured_text(cleaned_matrix)
                final_json_payload = parse_document_context(raw_text_stream, low_confidence_registry, cleaned_matrix)
                
                # Append extracted parameters to a summary log list for bulk reporting rows
                bulk_results_summary.append({
                    "Filename": file_node["name"],
                    "Invoice_Number": final_json_payload["extracted_data"]["invoice_number"],
                    "Total_Amount": final_json_payload["extracted_data"]["total_amount"],
                    "Requires_Review": final_json_payload["idp_validation_flags"]["low_confidence_detected"]
                })
                
                # --- INTERACTIVE SINGLE-FILE VISUALIZER TIERS ---
                # If only one file exists, show full visual graphs as before
                if len(target_files) == 1:
                    with col1:
                        st.subheader("🖼️ Processed Image Grid Visualizer")
                        display_img = cv2.cvtColor(cleaned_matrix, cv2.COLOR_GRAY2RGB)
                        st.image(display_img, caption="Enhanced Contrast Matrix Layer sent to OCR core", use_container_width=True)
                        
                        st.write("") 
                        with st.expander("📦 Click to Expand Final Structured JSON Data Output", expanded=False):
                            formatted_json_string = json.dumps(final_json_payload, indent=4, ensure_ascii=False)
                            st.code(formatted_json_string, language="json")

                    with col2:
                        st.header("📝 Raw OCR Extracted Text Payload")
                        st.text_area(label="Text Strings", value=raw_text_stream, height=350, label_visibility="collapsed")
                            
                        st.subheader("⚠️ Human-in-the-Loop Risk Verification")
                        if final_json_payload["idp_validation_flags"]["low_confidence_detected"]:
                            st.error("Low-confidence tokens captured! Manual review required.")
                            st.dataframe(low_confidence_registry, use_container_width=True)
                        else:
                            st.success("All character extraction vectors verified over 50% safety margin.")
            
            except Exception as e:
                st.error(f"Execution Error processing {file_node['name']}: {str(e)}")
                
            finally:
                # Cleanup local workspace tracking nodes safely
                if file_node["is_temp"] and os.path.exists(file_node["path"]):
                    os.remove(file_node["path"])

    # --- MULTI-FILE BULK VIEW PANELS ---
    # If multiple files are processed, display a clean consolidated data table summary block
    if len(target_files) > 1:
        with col1:
            st.header("🏆 Consolidated Bulk Processing Report Summary")
            summary_df = pd.DataFrame(bulk_results_summary)
            st.dataframe(summary_df, use_container_width=True)
            
            # Export results to a structured CSV download button on-screen
            csv_data = summary_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Consolidated Bulk Results CSV Sheet",
                data=csv_data,
                file_name="bulk_idp_extraction_report.csv",
                mime="text/csv"
            )
            
        with col2:
            st.header("📦 Microservice Batch Data Stream")
            with st.expander("🔍 Click to Expand Consolidated Batch JSON Payload", expanded=True):
                st.code(json.dumps(bulk_results_summary, indent=4), language="json")
else:
    with col1:
        st.info("👈 Please select a method or upload document asset(s) in the sidebar portal to trigger processing.")
