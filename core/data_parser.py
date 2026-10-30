import re
import json
import streamlit as st
from typing import Dict, Any, List
from groq import Groq

def parse_document_context_spatial(
    ocr_data: Dict[str, List[Any]], 
    low_conf_list: List[Dict[str, Any]], 
    tolerance_px: int = 8
) -> Dict[str, Any]:
    """
    Spatial & Dynamic Intelligent Parsing Engine.
    Uses pytesseract image_to_data geometry to parse multi-currency invoices,
    fully supporting Western and Indian Rupee (INR / Lakhs / Crores) layouts.
    """
    invoice_number = "Not Found"
    total_amount = "Not Found"

    # 1. FLATTEN OCR DATA INTO BLOCKS WITH GEOMETRY
    words = []
    n_boxes = len(ocr_data.get('text', []))
    for i in range(n_boxes):
        text = str(ocr_data['text'][i]).strip()
        if text:
            words.append({
                'text': text,
                'left': ocr_data['left'][i],
                'top': ocr_data['top'][i],
                'width': ocr_data['width'][i],
                'height': ocr_data['height'][i],
                'line_num': ocr_data['line_num'][i]
            })

    if not words:
        return {
            "document_type": "Invoice",
            "extracted_data": {"invoice_number": invoice_number, "total_amount": total_amount},
            "idp_validation_flags": {"low_confidence_detected": len(low_conf_list) > 0, "review_required_items": low_conf_list}
        }

    # 2. SPATIAL INVOICE NUMBER EXTRACTION
    inv_triggers = {"INVOICE", "BILL", "TAX INVOICE", "FACTURA", "RECHNUNG", "FACTURE", "INV", "NO.", "INVOICE NO"}
    
    for idx, w in enumerate(words):
        norm_text = w['text'].upper().replace(':', '')
        if norm_text in inv_triggers or any(t in norm_text for t in ["INV-", "INV#"]):
            # Strategy A: Look right on the exact same line
            same_line_right = [
                other for other in words[idx+1:idx+6]
                if abs(other['top'] - w['top']) <= tolerance_px and other['left'] > w['left']
            ]
            if same_line_right:
                same_line_right.sort(key=lambda x: x['left'])
                potential_slug = "".join([x['text'] for x in same_line_right])
                if re.search(r'[0-9]', potential_slug):
                    invoice_number = potential_slug
                    break
            
            # Strategy B: Fallback to the immediate block underneath
            underneath = [
                other for other in words 
                if other['top'] > w['top'] and abs(other['left'] - w['left']) <= 50
            ]
            if underneath:
                underneath.sort(key=lambda x: x['top'])
                if re.search(r'[0-9]', underneath[0]['text']):
                    invoice_number = underneath[0]['text']
                    break

    # 3. SPATIAL TOTAL & MULTI-CURRENCY EXTRACTION (Bottom-up Scan)
    total_triggers = {"TOTAL", "DUE", "FAILLIT", "BETRAG", "NETTO", "PAGAR", "SOLDE", "NET PAYABLE", "GRAND TOTAL", "AMOUNT PAYABLE"}
    currency_regex = r'(?:[\$\u20AC\u00A3\u00A5\u20B9]|EUR|USD|GBP|CHF|JPY|INR|Rs\.?)\s*\b\d{1,3}(?:[.,\s]\d{2})*(?:[.,\s]\d{3})*(?:[.,]\d{2})\b|\b\d+(?:[.,]\d{2})\b'

    for idx in range(len(words) - 1, -1, -1):
        w = words[idx]
        norm_text = w['text'].upper()
        
        if any(t in norm_text for t in total_triggers):
            row_items = [
                other for other in words 
                if abs(other['top'] - w['top']) <= tolerance_px and other['left'] > w['left']
            ]
            
            if row_items:
                row_items.sort(key=lambda x: x['left'])
                combined_row_text = " ".join([x['text'] for x in row_items])
                money_match = re.search(currency_regex, combined_row_text)
                if money_match:
                    total_amount = money_match.group(0).strip()
                    break

    return {
        "document_type": "Invoice",
        "extracted_data": {
            "invoice_number": invoice_number,
            "total_amount": total_amount
        },
        "idp_validation_flags": {
            "low_confidence_detected": len(low_conf_list) > 0,
            "review_required_items": low_conf_list
        }
    }


def parse_document_context_via_llm(raw_text_stream: str, low_conf_list: list) -> dict:
    """
    Leverages Groq Cloud API's deterministic JSON Mode to convert 
    unstructured, raw OCR text streams into schema-compliant payloads.
    """
    if "GROQ_API_KEY" not in st.secrets:
        raise KeyError("Groq API configuration missing. Add 'GROQ_API_KEY' to your Streamlit Secrets.")
        
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
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract details from this text stream:\n\n{raw_text_stream}"}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        
        parsed_payload = json.loads(response.choices.message.content)
        parsed_payload["idp_validation_flags"] = {
            "low_confidence_detected": len(low_conf_list) > 0,
            "review_required_items": low_conf_list
        }
        return parsed_payload
        
    except Exception as e:
        return {
            "document_type": "Invoice",
            "extracted_data": {"invoice_number": "Error In Extraction", "total_amount": "Error In Extraction"},
            "idp_validation_flags": {"low_confidence_detected": True, "error": str(e)}
        }
