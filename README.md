# 🌐 AI Language Translator

![Python](https://img.shields.io/badge/Python-3.13.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Transformers-FFD21E?style=for-the-badge)
![Vibe Coding](https://img.shields.io/badge/Day-01-blueviolet?style=for-the-badge&label=100%20Days%20of%20Vibe%20Coding)

A high-performance, **offline-first** neural machine translation engine. This application leverages **Helsinki-NLP's MarianMT** transformer models to provide private, low-latency translations without the need for external APIs or internet connectivity after the initial model download.

---

## 🚀 Key Features
* **Zero-API Dependency:** No OpenAI or Anthropic keys required; runs entirely on local compute.
* **High Privacy:** Your data never leaves your machine—perfect for sensitive translations.
* **6+ Language Pairs:** Seamlessly translate between English and French, German, Spanish, Hindi, Italian, and Dutch.
* **Modern Interface:** A clean, dark-themed UI built with Streamlit and custom CSS for a premium user experience.

---

## 🛠️ Tech Stack
* **Frontend:** Streamlit.
* **ML Framework:** Hugging Face Transformers & PyTorch.
* **Inference Engine:** MarianMT (Helsinki-NLP).
* **Python Version:** 3.13.12.

---

## 💻 How to Run

### 1. Prerequisites
Ensure you have Python 3.13.12 installed. It is recommended to use a virtual environment.

### 2. Installation
Clone the repository and install the dependencies from the `requirements.txt` file:

```bash
git clone [https://github.com/Swapnil-bo/AI-Language-Translator.git](https://github.com/Swapnil-bo/AI-Language-Translator.git)
cd AI-Language-Translator
pip install -r requirements.txt