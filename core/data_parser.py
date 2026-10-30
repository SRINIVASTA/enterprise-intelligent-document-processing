import pytesseract
import re
from typing import Dict, Any, List

def parse_document_context(raw_text: str, low_conf_list: List[Dict[str, Any]], image_matrix=None) -> Dict[str, Any]:
    """
    Dynamic Normalized Parsing Engine.
    Extracts variable invoice numbers and totals without hardcoded text fallbacks.
    """
    invoice_number = "Not Found"
    total_amount = "Not Found"

    # Split text into lines and clean whitespace
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]

    # 1. DYNAMIC INVOICE NUMBER EXTRACTION
    # Looks for variations of 'Invoice #', 'Invoice No', 'Invoice:', etc.
    invoice_patterns = [
        r'INVOICE\s*(?:NO\.?|NUMBER|#)?\s*:\s*([A-Z0-9-]+)',
        r'INVOICE\s*(?:NO\.?|NUMBER|#)?\s+([A-Z0-9-]+)',
    ]

    for line in lines:
        upper_line = line.upper()
        if "INVOICE" in upper_line:
            matched = False
            for pattern in invoice_patterns:
                match = re.search(pattern, upper_line)
                if match:
                    invoice_number = match.group(1).strip()
                    matched = True
                    break
            if matched:
                break
                
    # 2. DYNAMIC TOTAL EXTRACTION (Scanning from the bottom up)
    # Avoids hardcoded layout numbers by dynamically tracking standard currency structures
    total_keywords = ["TOTAL DUE", "TOTAL OUE", "TOTAL", "AMOUNT DUE", "BALANCE DUE"]
    
    for line in reversed(lines):
        upper_line = line.upper()
        if any(k in upper_line for k in total_keywords):
            # Matches standard currency formats: e.g., 1,140.67, 840.00, 450
            # Captures values containing standard decimals/commas or clean trailing digits
            money_match = re.search(r'\b\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})\b|\b\d+(?:[.,]\d{2})\b', line)
            if money_match:
                total_amount = money_match.group(0)
                break
            
            # Fallback for plain digits at the end of a total line if decimals are missed
            digits = re.findall(r'\b\d+\b', line)
            if digits:
                total_amount = digits[-1]
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
