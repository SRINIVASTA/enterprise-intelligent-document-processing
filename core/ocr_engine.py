import pytesseract
from typing import Dict, Any, List, Tuple

def extract_structured_text(processed_img) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Executes structural OCR translation using unified block configurations.
    """
    # Enforce Page Segmentation Mode 6 to sweep horizontally across data columns
    psm_config = r'--psm 6'
    ocr_data = pytesseract.image_to_data(processed_img, config=psm_config, output_type=pytesseract.Output.DICT)
    
    raw_strings = " ".join([word for word in ocr_data['text'] if word.strip() != ""])
    
    low_confidence_metrics = []
    for i in range(len(ocr_data['text'])):
        word = ocr_data['text'][i].strip()
        if word != "":
            conf = int(ocr_data['conf'][i])
            # Isolate character confidence zones dropping beneath the 50% safety boundary
            if 0 < conf < 50:
                low_confidence_metrics.append({"word": word, "confidence": f"{conf}%"})
                
    return raw_strings, low_confidence_metrics
