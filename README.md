# EduLens 🔎

AI-powered study material assessment and weak-topic detector using Streamlit, Python and Ollama.

## Features

- Upload PDF, PPTX, TXT or DOCX study material
- Select test difficulty
- Select number of questions
- Generate questions using only uploaded material
- Categories:
  - Concept Understanding
  - Concept Application
  - Analysis
  - Problem Solving
- Automatic scoring
- Topic-wise performance
- Category-wise performance
- Weak topic detection
- AI-generated personalized feedback
- Local Ollama model, so no paid AI API is required

## 1. Install Python

Use Python 3.10+.

## 2. Create virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
venv\Scripts\activate.bat
```

## 3. Install packages

```powershell
pip install -r requirements.txt
```

## 4. Install/check Ollama

Install Ollama from its official website.

Then check:

```powershell
ollama --version
```

Pull a model, for example:

```powershell
ollama pull llama3.2
```

Check installed models:

```powershell
ollama list
```

Make sure Ollama is running before starting EduLens.

## 5. Run EduLens

```powershell
streamlit run app.py
```

The browser will open the Streamlit application.

## Recommended project demo flow

1. Upload a DBMS/Python/Java PDF.
2. Select Medium difficulty.
3. Select 5 questions.
4. Generate the test.
5. Answer the questions.
6. Submit.
7. Show score.
8. Show category performance.
9. Show topic-wise performance.
10. Show the "Weak Points Detected" section.

## Important design idea

Python performs deterministic calculations such as marks, accuracy and topic aggregation.

Ollama performs:
- question generation
- short-answer evaluation
- personalized weakness explanation

This separation makes the application easier to test and demonstrate.
