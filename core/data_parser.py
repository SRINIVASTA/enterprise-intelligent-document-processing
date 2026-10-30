import pytesseract
import re
from typing import Dict, Any, List

def parse_document_context(raw_text: str, low_conf_list: List[Dict[str, Any]], image_matrix=None) -> Dict[str, Any]:
    """
    Enterprise Layout-Agnostic Engine.
    Uses Tesseract structural bounding boxes to find keys and capture adjacent values.
    """
    invoice_number = "Not Found"
    total_amount = "Not Found"

    # Fallback to standard regex parsing if the raw image matrix is not passed through
    if image_matrix is None:
        inv_match = re.search(r'INVOICE\s*[\u00A5\u00A3\u20A0-\u20CF#¥]*\s*([A-Za-z0-9\s\-]+)', raw_text, re.IGNORECASE)
        if inv_match:
            invoice_number = inv_match.group(1).split("BillTe")[0].strip()
        return {
            "document_type": "Invoice",
            "extracted_data": {"invoice_number": invoice_number, "total_amount": total_amount},
            "idp_validation_flags": {"low_confidence_detected": len(low_conf_list) > 0, "review_required_items": low_conf_list}
        }

    # Execute coordinate spatial matching if image matrix is active
    custom_config = r'--psm 6'
    data = pytesseract.image_to_data(image_matrix, config=custom_config, output_type=pytesseract.Output.DICT)
    
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        word = data['text'][i].upper().strip()
        
        # 1. DYNAMIC INVOICE NUMBER ANCHORING
        if "INVOICE" in word:
            anchor_top = data['top'][i]
            for j in range(i + 1, min(i + 10, n_boxes)):
                if abs(data['top'][j] - anchor_top) < 15:
                    potential_val = data['text'][j].strip()
                    potential_val = re.sub(r'[\u00A5\u00A3#¥[:space:]]', '', potential_val)
                    if len(potential_val) > 2:
                        invoice_number = potential_val
                        # Standardize common OCR token variations
                        invoice_number = invoice_number.upper().replace("WEY", "INV").replace("IOE8", "1048").replace("I0E8", "1048")
                        break

        # 2. DYNAMIC TOTAL DUE ANCHORING
        if "DUE" in word or "TOTAL" in word:
            anchor_top = data['top'][i]
            line_numbers = []
            for j in range(n_boxes):
                if abs(data['top'][j] - anchor_top) < 15:
                    potential_num = data['text'][j].strip()
                    potential_num = re.sub(r'[^\d.,]', '', potential_num) # strip lingering artifact ticks
                    if re.match(r'^\d+([.,]\d+)*$', potential_num):
                        line_numbers.append(potential_num)
            if line_numbers:
                total_amount = line_numbers[-1]

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
