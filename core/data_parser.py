import json
import streamlit as st
from groq import Groq

def parse_document_context_via_llm(raw_text_stream: str, low_conf_list: list) -> dict:
    """
    Leverages Groq Cloud API's deterministic JSON Mode to convert 
    unstructured, raw OCR text streams into schema-compliant payloads.
    """
    # Safeguard against missing API keys in Streamlit Management Console
    if "GROQ_API_KEY" not in st.secrets:
        raise KeyError("Groq API configuration missing. Add 'GROQ_API_KEY' to .streamlit/secrets.toml")
        
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    system_prompt = (
        "You are an expert Intelligent Document Processing (IDP) parser. Your task is to extract "
        "the 'invoice_number' and 'total_amount' from raw OCR text blocks.\n"
        "Return ONLY a valid JSON object matching this schema exactly:\n"
        "{\n"
        "  \"document_type\": \"Invoice\",\n"
        "  \"extracted_data\": {\n"
        "    \"invoice_number\": \"string or 'Not Found'\",\n"
        "    \"total_amount\": \"string or 'Not Found'\"\n"
        "  }\n"
        "}"
    )

    try:
        # Enforce highly dense structured extraction models via Llama-3
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract details from this text stream:\n\n{raw_text_stream}"}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        
        # Safe JSON parse payload structures
        parsed_payload = json.loads(response.choices[0].message.content)
        
        # Inject standard validation tracking flags to align with spatial architectures
        parsed_payload["idp_validation_flags"] = {
            "low_confidence_detected": len(low_conf_list) > 0,
            "review_required_items": low_conf_list
        }
        return parsed_payload
        
    except Exception as e:
        # Fallback to an empty schema structure on API layer breakdowns
        return {
            "document_type": "Invoice",
            "extracted_data": {"invoice_number": "Error In Extraction", "total_amount": "Error In Extraction"},
            "idp_validation_flags": {"low_confidence_detected": True, "error": str(e)}
        }
