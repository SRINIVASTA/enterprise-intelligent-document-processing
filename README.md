# Enterprise Intelligent Document Processing (IDP) Engine

An enterprise-grade, microservice-ready **Intelligent Document Processing (IDP)** pipeline engineered in Python. This repository combines advanced computer vision text enhancement pipelines, raw Optical Character Recognition (OCR) matrix extraction arrays, and semantic data structure parsing architectures to convert unstructured, noisy document images into schema-compliant, structured JSON datasets.

---

## 🏗️ System Architecture & Workflow Pipeline

The layout below illustrates how data transforms as it flows sequentially through the system matrix segments, from raw ingestion up to the validation gateway:

```mermaid
graph TD
    A[Raw Image / Invoice Upload] -->|Ingestion Layer| B(Sidebar Router: app.py)
    B -->|Option 1: Mock Ingestion| C[sample.png Matrix Node]
    B -->|Option 2: Custom Asset| D[Temp Buffer Stream]
    
    C & D -->|Image Ingestion Array| E[core/vision_engine.py]
    
    subgraph OpenCV Vision Engine Pipeline
        E -->|Interpolation Scaling| F[2x Cubic Spline Matrix Scaling]
        F -->|Chroma Channel Strip| G[Grayscale Conversion]
        G -->|Dynamic Histogram Evaluation| H[Adaptive Background Inversion]
    end
    
    H -->|Enhanced Contrast Gray Matrix| I[core/ocr_engine.py]
    
    subgraph Tesseract OCR Engine Array
        I -->|Enforce PSM 6 Bounds| J[Horizontal Cross-Column Sweep]
        J -->|Token Generation Loop| K[Raw Text Block Accumulation]
        J -->|Isolate Certainty Anomalies| L[Flag Low-Confidence Words < 50%]
    end
    
    K & L -->|Text Block + Confidence Logs| M[core/data_parser.py]
    
    subgraph Deterministic IDP Validation Subsystem
        M -->|Reverse Inspection Tree| N[Bottom-Up Line Boundary Parsing]
        N -->|Regex Block Token Matching| O[Extract Invoice & Revenue Keys]
        O -->|Semantic Optimization| P[Text-Normalization & Noise Removal]
    end
    
    P -->|Schema Assembly| Q[Collapsible JSON Viewer with Code Indents]
    L -->|Risk Registry Array| R[Human-in-the-Loop Verification Panel]
```

---

## 🚀 Key Architectural Features

*   **Adaptive Computer Vision Tier:** Leverages **OpenCV** to automate matrix interpolation (Cubic Splines), grayscale channel separation, and automated background binarisation to maximize text structural clarity before downstream translation.
*   **Context-Preserving OCR Infrastructure:** Utilises structural Page Segmentation Modes (`--psm 6`) via **Tesseract** to retain geometric cross-column coordinates across fragmented data tables and invoices.
*   **Deterministic IDP & Validation Subsystem:** Implements custom fallback regular expressions and reverse line scan mechanics to extract critical business metrics despite text translation degradation.
*   **Human-in-the-Loop Risk Profiling:** Programmatically maps word-level confidence indicators under 50% to automatically flag high-risk translations for manual review.
*   **Interactive Streamlit Control Panel:** Features a responsive layout hosting a configuration sidebar interface, clean dual-mode toggle components, and collapsible, 4-space indented code blocks using custom JSON syntax configurations.

---

## 🛠️ Technology Stack & Dependencies

*   **Language Layer:** Python 3.10+ (Fully validated on Python 3.14 environments)
*   **Vision Subsystem:** OpenCV (`opencv-python-headless`)
*   **OCR Matrix Architecture:** Tesseract OCR Engine Engine (`pytesseract`)
*   **Web Portal Architecture:** Streamlit Cloud Framework Core
*   **Data Layouts:** Native JSON, Advanced Regex Systems (`re`)

---

## 📦 Project Layout Overview

```text
enterprise-intelligent-document-processing/
│
├── .streamlit/
│   └── config.toml            # UI Theme & Display Properties
│
├── core/                      # System Engine Submodules
│   ├── __init__.py            # Module Registration Node
│   ├── vision_engine.py       # OpenCV Matrix Operations
│   ├── ocr_engine.py          # Tesseract String Translations
│   └── data_parser.py         # Advanced Document Regex Logic
│
├── app.py                     # Streamlit Main Dashboard Gateway
├── sample.png                 # Mock Invoice Reference Matrix
├── requirements.txt           # Python Package Manifest
├── packages.txt               # OS Binary Component Flags (tesseract-ocr)
└── README.md                  # Project System Documentation
```

---

## ⚙️ Local Installation & Sandbox Launch

### 1. Provision Operating System Engine (Ubuntu/Debian)
The underlying OCR infrastructure requires direct system binaries to evaluate image pixel locations:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr -y
```

### 2. Configure Virtual Environment & Packages
```bash
# Clone the repository node
git clone https://github.com
cd enterprise-intelligent-document-processing

# Instantiate independent environment sandbox
python3 -m venv venv
source venv/bin/activate

# Install component runtime libraries
pip install -r requirements.txt
```

### 3. Start the Web Server Locally
```bash
streamlit run app.py
```

---
💡 *Engineered with automated data processing logic to bridge the gap between unstructured image assets and structured database records.*
