# 🧠 RAG Chatbot for KaStack Labs

⚡ A lightweight Retrieval-Augmented Generation (RAG) system built to analyze real conversation data, detect topic shifts, extract user persona, and answer queries intelligently.

---

## 🚀 Features

### 1. Topic-Based Checkpointing
- Processes conversations **chronologically**
- Detects **topic shifts dynamically**
- Generates summaries per topic segment

```
Topic 1 → messages 0–120 → summary
Topic 2 → messages 121–344 → summary
```

---

### 2. 100-Message Checkpoints
- Every 100 messages → independent summary
- Ensures coverage even if topic detection misses context

---

### 3. RAG Query System
- Retrieves:
  - Topic summaries
  - Message chunks
  - Raw conversation segments
- Combines them to generate meaningful answers

---

### 4. Persona Extraction
Extracts structured user insights:

```json
{
  "habits": [],
  "personality": [],
  "communication_style": [],
  "personal_facts": []
}
```

---

### 5. Interactive Chatbot UI
- Built using **Flask + HTML + CSS**
- Clean UI with table rendering
- Supports:
  - Topic exploration
  - Persona queries
  - Context-based Q&A

---

## 🧠 System Architecture

```
CSV Conversations
      ↓
Preprocessing
      ↓
Segmentation (Topic Detection)
      ↓
Summarization
      ↓
RAG Retrieval Layer
      ↓
Persona Extraction
      ↓
Flask Chatbot UI
```

---

## ⚙️ Tech Stack

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn (TF-IDF)
- HTML + CSS (UI)

---

## 🧩 How Topic Detection Works

- Converts messages into comparable representations
- Measures similarity between consecutive messages
- If similarity drops → **new topic checkpoint created**

---

## 🔍 How Retrieval Works

1. Query → converted into vector (TF-IDF)
2. Compared against:
   - Topic summaries
   - Chunk summaries
   - Raw message chunks
3. Top matches retrieved
4. Filtered + structured into final answer

---

## 👤 Persona Extraction Logic

Rule-based extraction from actual signals:

- Keywords (sleep, gym, exam, etc.)
- Tone indicators (lol, sorry, etc.)
- Message patterns (length, questions)

No hallucination. Only data-backed inference.

---

## 📂 Project Structure

```
rag-chatbot/
├── src/
│   ├── app.py
│   ├── preprocess.py
│   ├── segmentation.py
│   ├── summarizer.py
│   ├── retrieval.py
│   └── persona.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── data/
│   └── conversations.csv
│
├── requirements.txt
└── Procfile
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/rag-chatbot.git
cd rag-chatbot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/app.py
```

### Access the App
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🎯 Example Queries

- `topics`
- `what are his habits`
- `what kind of person is this`
- `what did he say about career`
- `summarize conversation`

---

## 🌐 Deployment

Deployed using cloud platform with:

```bash
gunicorn src.app:app
```

---

## 📌 Key Highlights

✔ No external APIs  
✔ Lightweight & efficient  
✔ Handles real-world noisy conversations  
✔ Structured memory system  
✔ End-to-end working product  

---

## 👨‍💻 Developed By

**Ashish**  
RAG Chatbot for KaStack Labs

---

