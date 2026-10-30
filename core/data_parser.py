import pytesseract
import re
from typing import Dict, Any, List

def parse_document_by_coordinates(image_matrix) -> Dict[str, Any]:
    """
    Enterprise Layout-Agnostic Engine.
    Uses Tesseract structural bounding boxes to find keys and capture adjacent values.
    """
    # Get complete spatial DataFrame directory from the image matrix
    custom_config = r'--psm 6'
    data = pytesseract.image_to_data(image_matrix, config=custom_config, output_type=pytesseract.Output.DICT)
    
    invoice_number = "Not Found"
    total_amount = "Not Found"
    
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        word = data['text'][i].upper().strip()
        
        # 1. DYNAMIC INVOICE NUMBER ANCHORING
        # If we hit the keyword "INVOICE", look at the words immediately to its right on the same vertical alignment
        if "INVOICE" in word:
            anchor_top = data['top'][i]
            anchor_left = data['left'][i]
            
            # Look ahead for tokens sharing the same row boundary (within a 15-pixel variance limit)
            for j in range(i + 1, min(i + 10, n_boxes)):
                if abs(data['top'][j] - anchor_top) < 15:
                    potential_val = data['text'][j].strip()
                    # Clean out noise symbols dynamically using character sets instead of hardcoding
                    potential_val = re.sub(r'[\u00A5\u00A3#¥[:space:]]', '', potential_val)
                    if len(potential_val) > 2 and potential_val.isalnum():
                        invoice_number = potential_val
                        break

        # 2. DYNAMIC TOTAL DUE ANCHORING
        # If we hit the absolute anchor token "DUE", grab the rightmost number on that exact line array
        if "DUE" in word or "TOTAL" in word:
            anchor_top = data['top'][i]
            line_numbers = []
            
            # Scan the adjacent matrix space for floating numeric decimal strings
            for j in range(n_boxes):
                if abs(data['top'][j] - anchor_top) < 15: # Same line array
                    potential_num = data['text'][j].strip()
                    # Check if it matches a standard financial digit sequence
                    if re.match(r'^\d+([.,]\d+)*$', potential_num):
                        line_numbers.append(potential_num)
            
            if line_numbers:
                total_amount = line_numbers[-1] # The rightmost item in a table column layout is always the line total

    return {
        "invoice_number": invoice_number,
        "total_amount": total_amount
    }
