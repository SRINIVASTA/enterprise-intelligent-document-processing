# Enterprise Intelligent Document Processing (IDP) Engine

An enterprise-grade, microservice-ready **Intelligent Document Processing (IDP)** pipeline engineered in Python. This repository combines advanced computer vision text enhancement pipelines, raw Optical Character Recognition (OCR) matrix extraction arrays, spatial regular expression trees, and advanced LLM semantic parsing via Groq Cloud API to convert unstructured, noisy document images into schema-compliant, structured JSON datasets.

## About

**Enterprise Intelligent Document Processing (IDP) workstation** built with **Streamlit**, **OpenCV**, **Tesseract OCR**, and **Groq LLM (Llama 3)**. Combines **adaptive image preprocessing**, **spatial bounding-box regex parsing**, and **heuristic math fallback** to convert noisy invoices and documents into **structured JSON**.

---
![Enterprise IDP Platform](assets/dashboard-preview.png)
---

## 🏗️ System Architecture & Workflow Pipeline

The layout below illustrates how data transforms as it flows sequentially through the system matrix segments, branching dynamically into either Spatial Regex Parsing or the Heuristic Math LLM Engine depending on your selected Pipeline Configuration:

```mermaid
flowchart TD
    A[Raw Image / Invoice Upload] e1@-->|Ingestion Layer| B(Sidebar Router: app.py)
    B e2@-->|Option 1: Mock Ingestion| C[sample.png Matrix Node]
    B e3@-->|Option 2: Spatial Regex Mode| D[Temp Buffer Stream]
    B e4@-->|Option 3: Groq LLM Mode| DM[Temp Buffer Stream]
    
    C e5@-->|Image Ingestion Array| E[core/vision_engine.py]
    D e6@-->|Image Ingestion Array| E
    DM e7@-->|Image Ingestion Array| E
    
    subgraph OpenCV_Vision_Engine_Pipeline [OpenCV Vision Engine Pipeline]
        E e8@-->|Interpolation Scaling| F[2x Cubic Spline Matrix Scaling]
        F e9@-->|Chroma Channel Strip| G[Grayscale Conversion]
        G e10@-->|Dynamic Histogram Evaluation| H[Adaptive Background Inversion]
    end
    
    H e11@-->|Enhanced Contrast Gray Matrix| I[core/ocr_engine.py]
    
    subgraph Tesseract_OCR_Engine_Array [Tesseract OCR Engine Array]
        I e12@-->|Enforce PSM 6 Bounds| J[Horizontal Cross-Column Sweep]
        J e13@-->|Token Generation Loop| K[Raw Text Block Accumulation]
        J e14@-->|Isolate Certainty Anomalies| L[Flag Low-Confidence Words < 50%]
    end
    
    K e15@-->|Pipeline Branching Route| M{Routing Controller}
    L e16@-->|Pipeline Branching Route| M
    
    subgraph Dynamic_Dual_Engine_Parsing_Core [Dynamic Dual-Engine Parsing Core]
        M e17@-->|Option 1 & 2: Spatial Match| N[parse_document_context_spatial]
        N e18@-->|Geometry Box Evaluation| O[Bottom-Up Line Boundary Regex Mapping]
        
        M e19@-->|Option 3: Groq Mode| P[parse_document_context_via_llm]
        P e20@-->|Streamlit Secrets Authorization| Q[Secure API Gateway Tunnel]
        Q e21@-->|Llama-3 Structured Context Reasoning| R[Heuristic Math Fallback Engine]
        R e22@-->|Predictive Line-Item Computation| S[Reconstruct Corrupted/Missing Totals]
    end
    
    O e23@-->|Schema Assembly| T[Consolidated Streamlit JSON Dashboard View]
    S e24@-->|Schema Assembly| T
    L e25@-->|Risk Registry Array| U[Human-in-the-Loop Verification Panel]

    %% Running Flow Animation Definitions
    e1@{ animate: true }
    e2@{ animate: true }
    e3@{ animate: true }
    e4@{ animate: true }
    e5@{ animate: true }
    e6@{ animate: true }
    e7@{ animate: true }
    e8@{ animate: true }
    e9@{ animate: true }
    e10@{ animate: true }
    e11@{ animate: true }
    e12@{ animate: true }
    e13@{ animate: true }
    e14@{ animate: true }
    e15@{ animate: true }
    e16@{ animate: true }
    e17@{ animate: true }
    e18@{ animate: true }
    e19@{ animate: true }
    e20@{ animate: true }
    e21@{ animate: true }
    e22@{ animate: true }
    e23@{ animate: true }
    e24@{ animate: true }
    e25@{ animate: true }
```

---

## 🚀 Key Architectural Features

*   **Adaptive Computer Vision Tier:** Leverages **OpenCV** to automate matrix interpolation (Cubic Splines), grayscale channel separation, and automated background binarisation to maximize text structural clarity before downstream translation.
*   **Context-Preserving OCR Infrastructure:** Utilises structural Page Segmentation Modes (`--psm 6`) via **Tesseract** to retain geometric cross-column coordinates across fragmented data tables and invoices.
*   **Dual-Route Parsing Architecture:** 
    *   **Deterministic Spatial Parser:** Uses bounding box geometry mapping coordinates (`left`, `top`, `width`, `height`) to extract critical financial indicators across complex global and Indian Rupee layouts.
    *   **Cognitive LLM Parser:** Leverages Groq Cloud API's deterministic JSON Mode to read noisy OCR text contextually. Includes an automated mathematical fallback engine that programmatically recalculates broken total values using up-table line items.
*   **Human-in-the-Loop Risk Profiling:** Programmatically maps word-level confidence indicators under 50% to automatically flag high-risk translations for manual review.
*   **Interactive Streamlit Control Panel:** Features a responsive layout hosting a configuration sidebar interface, clean triple-mode toggle components, and collapsible, 4-space indented code blocks using custom JSON syntax configurations.

---

## 🛠️ Technology Stack & Dependencies

*   **Language Layer:** Python 3.10+ (Fully validated on Python 3.14 environments)
*   **Vision Subsystem:** OpenCV (`opencv-python-headless`)
*   **OCR Matrix Architecture:** Tesseract OCR Engine Engine (`pytesseract`)
*   **Generative AI Gateway:** Groq Python SDK Client Core (`groq`)
*   **Web Portal Architecture:** Streamlit Cloud Framework Core
*   **Data Layouts:** Native JSON, Advanced Regex Systems (`re`)

---

## 📦 Project Layout Overview

```text
enterprise-intelligent-document-processing/
│
├── .streamlit/
│   └── config.toml            # UI Theme & Display Properties
│   └── secrets.toml           # Encrypted API Authorization Tokens (Local Sandbox)
│
├── core/                      # System Engine Submodules
│   ├── __init__.py            # Module Registration Node
│   ├── vision_engine.py       # OpenCV Matrix Operations
│   ├── ocr_engine.py          # Tesseract String Translations
│   └── data_parser.py         # Advanced Document Regex & Groq LLM Logic
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

### 3. Add API Authentication Credentials
Create a local file inside your project structure at `.streamlit/secrets.toml` and inject your active Groq Cloud key matching this layout:
```toml
GROQ_API_KEY = "gsk_yOuRGroQApiKeyHerE..."
```
To permanently bind the web portal interface to port 8506, confirm your `.streamlit/config.toml` includes:
```toml
[server]
port = 8506
address = "localhost"
```
### 4. Start the Web Server Locally
```bash
streamlit run app.py --server.port 8506 --server.address localhost
```

---

## ⚠️ Disclaimer

This project is an **Intelligent Document Processing (IDP)** proof-of-concept intended strictly for educational, research, and technical evaluation purposes. Automated OCR and LLM-extracted JSON outputs may contain inaccuracies on degraded or complex documents and must undergo human-in-the-loop verification before use in production accounting, financial auditing, or compliance workflows.

Users are responsible for securing their own `GROQ_API_KEY` locally (such as within `.streamlit/secrets.toml`), adhering to Groq API rate limits and terms of service, and ensuring that sensitive invoices, personal identifiable information (PII), or confidential documents are handled in compliance with applicable data privacy laws.

---

## 🛡️ License, Copyright & Compliance Notices

**All Rights Reserved © 2026 T A Srinivas.**

> **Strict Intellectual Property Notice:** This repository is strictly for portfolio viewing and technical evaluation purposes. **DO NOT COPY, CLONE, FORK, OR REDISTRIBUTE** this source code, architecture, or documentation. Stolen copies or unauthorized forks will be reported immediately for a **GitHub DMCA copyright takedown**.

For corporate licensing, enterprise deployment, or commercial inquiries, please contact **`tasrinivass@gmail.com`**.

* **Lead Architect & Developer:** [Srinivasta](https://github.com/SRINIVASTA)

### 🌐 Let’s Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/srinivas-t-a-557637119/)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/srinivasta)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tasrinivass@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/srinivasta)
[![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=website&logoColor=white)](https://srinivasta.github.io)

💡 *Engineered with automated data processing logic to bridge the gap between unstructured, degraded image assets and structured database records.*
