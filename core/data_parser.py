import re
from typing import Dict, Any, List

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
    # Expanded triggers to catch Indian GST regulations ("TAX INVOICE") and global variations
    inv_triggers = {"INVOICE", "BILL", "TAX INVOICE", "FACTURA", "RECHNUNG", "FACTURE", "INV", "NO.", "INVOICE NO"}
    
    for idx, w in enumerate(words):
        norm_text = w['text'].upper().replace(':', '')
        if norm_text in inv_triggers or any(t in norm_text for t in ["INV-", "INV#"]):
            # Strategy A: Look right on the exact same line (same vertical baseline)
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
    # Includes Indian targets like "NET PAYABLE" and "GRAND TOTAL"
    total_triggers = {"TOTAL", "DUE", "FAILLIT", "BETRAG", "NETTO", "PAGAR", "SOLDE", "NET PAYABLE", "GRAND TOTAL", "AMOUNT PAYABLE"}
    
    # Advanced Dynamic Currency Regex: 
    # Supports standard Millions: $1,140.67 or €1.140,67
    # Supports Indian Lakhs/Crores: ₹15,40,000.00 or Rs. 2,50,000.00
    # Explicitly matches symbols: $, €, £, ¥, ₹ (\u20B9), INR, Rs., Rs
    currency_regex = r'(?:[\$\u20AC\u00A3\u00A5\u20B9]|EUR|USD|GBP|CHF|JPY|INR|Rs\.?)\s*\b\d{1,3}(?:[.,\s]\d{2})*(?:[.,\s]\d{3})*(?:[.,]\d{2})\b|\b\d+(?:[.,]\d{2})\b'

    # Scan words backwards to prioritize the final invoice calculations
    for idx in range(len(words) - 1, -1, -1):
        w = words[idx]
        norm_text = w['text'].upper()
        
        if any(t in norm_text for t in total_triggers):
            # Check horizontally to the right for the currency value
            row_items = [
                other for other in words 
                if abs(other['top'] - w['top']) <= tolerance_px and other['left'] > w['left']
            ]
            
            if row_items:
                row_items.sort(key=lambda x: x['left'])
                # Reconstruct full block text string (handles cases where currency symbol or commas are split into discrete tokens)
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
