import cv2
import numpy as np

def preprocess_image(image_path: str) -> np.ndarray:
    """
    Applies computer vision transformations to optimize document text strokes.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Unable to locate image matrix at: {image_path}")
    
    # 2x scale interpolation using Cubic Splines to thicken thin textual character boundaries
    scaled = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Strip chroma channels to analyze raw structural luminosity metrics
    gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)
    
    # Dynamic dark-mode background detection and inversion
    if np.mean(gray) < 127: 
        gray = cv2.bitwise_not(gray)
        
    return gray
