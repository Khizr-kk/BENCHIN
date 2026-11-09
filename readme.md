# BENCHIN
### Multilingual Speech Transcription & Evaluation Platform

**Powered by Gnani AI — Prisma v3.0**

BENCHIN is a speech transcription and evaluation platform designed to make Indian-language speech recognition measurable. It uses Gnani AI's Prisma speech-to-text model to convert audio into text and evaluates transcription quality using Word Error Rate (WER), Character Error Rate (CER), and edit-operation analysis.

The current MVP focuses on Gujarati-English code-mixed speech.

---

## Problem Statement

India has a diverse linguistic landscape where people frequently switch between regional languages and English during everyday conversations.

Transcribing such speech accurately presents challenges, particularly when dealing with code-mixed language, different pronunciations, and variations in spoken language.

Generating a transcript is only one part of the problem. Understanding how closely that transcript represents the actual speech is equally important.

BENCHIN addresses this by combining speech transcription with a measurable evaluation workflow.

## Key Features

### 1. AI-Powered Speech Transcription
- Integrates Gnani AI's Prisma v3.0 speech-to-text API.
- Supports audio uploads in WAV, MP3, OGG, FLAC, AAC and M4A formats.
- Configured for Gujarati-English code-mixed transcription.
- Displays generated transcripts through a web interface.

### 2. Interactive Speech Workspace
- Audio upload and drag-and-drop support.
- Audio preview before transcription.
- Editable transcription output.
- Copy and download transcript functionality.

### 3. Transcription Evaluation

BENCHIN compares an AI-generated transcript against a human-verified reference transcript.

It calculates:

| Metric | Description |
|---|---|
| WER | Word Error Rate |
| CER | Character Error Rate |
| Substitutions | Words or characters replaced incorrectly |
| Deletions | Words or characters missing from the generated transcript |
| Insertions | Extra words or characters in the generated transcript |

**Word Error Rate:**

WER = (S + D + I) / N

**Character Error Rate:**

CER = (S + D + I) / N

Where:
- S = Substitutions
- D = Deletions
- I = Insertions
- N = Number of words for WER or characters for CER in the reference.

Lower WER and CER indicate fewer transcription errors. WER can exceed 100% when insertions are sufficiently high.

---

## Technology Stack

| Component | Technology |
|---|---|
| AI Speech Recognition | Gnani AI Prisma v3.0 |
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| API Communication | REST API |
| Evaluation | Custom Python WER and CER implementation |
| Validation | Pytest |
| Environment Configuration | Python dotenv |

---

## System Architecture

```text
          User
           |
           v
     BENCHIN Web UI
           |
           v
       FastAPI
           |
           v
    Gnani Prisma v3.0
           |
           v
   Generated Transcript
           |
           v
    Editable Transcript
           |
           v
 Human Reference Transcript
           |
           v
   Evaluation Engine
           |
           v
    WER / CER Results
           |
           v
  Error Analysis Dashboard
```

---

## Project Structure

```text
BENCHIN/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── gnani_client.py
│   └── transcription_metrics.py
│
├── data/
│   ├── benchmark.jsonl
│   ├── results.json
│   ├── test_audio.wav
│   └── test_audio_trimmed.wav
│
├── tests/
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .env
├── .gitignore
└── pyproject.toml
```

---

## Getting Started

### Prerequisites

- Python 3.10 or later
- Gnani AI API credentials
- Git

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/BENCHIN.git
cd BENCHIN
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn python-multipart requests python-dotenv pytest
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GNANI_API_KEY_ID=your_gnani_api_key_id
```

Never commit your API credentials to GitHub.

### 5. Run the application

```bash
python -m uvicorn app.main:app --reload
```

Open:

**http://127.0.0.1:8000**

API documentation:

**http://127.0.0.1:8000/docs**

---

## API Endpoints

### POST `/transcribe`

Accepts an audio file and returns its generated transcription using Gnani Prisma.

**Request:** Multipart form data containing `audio_file`.

**Response example:**

```json
{
  "success": true,
  "transcript": "Generated transcription",
  "model": "prisma-v3.0",
  "detected_language_code": "gu-IN",
  "processing_time": 2.5
}
```

The response fields depend on the information returned by the Gnani API.

### POST `/evaluate`

Compares a human reference transcript against an AI-generated hypothesis.

**Request:**

```json
{
  "reference": "hello world this is benchin",
  "hypothesis": "hello there this is benchin"
}
```

**Response:**

```json
{
  "reference_words": 5,
  "substitutions": 1,
  "deletions": 0,
  "insertions": 0,
  "wer": 0.2,
  "cer": 0.18518518518518517
}
```

---

## Running Tests

Run the test suite:

```bash
python -m pytest -q
```

The current test suite contains 22 passing tests covering the implemented project functionality.

---

## Current Scope and Limitations

BENCHIN is an early-stage MVP.

**Implemented:**
- Gnani Prisma v3.0 API integration.
- Gujarati-English code-mixed transcription configuration.
- Audio upload and transcription interface.
- Editable transcript output.
- Human-reference-based WER and CER evaluation.
- Substitution, deletion and insertion
