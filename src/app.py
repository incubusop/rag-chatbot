# src/app.py

import os
from flask import Flask, request, render_template

from preprocess import load_messages
from segmentation import segment_messages
from summarizer import summarize
from retrieval import Retriever
from persona import extract_persona


# =========================
# PATH SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "conversations.csv")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)


# =========================
# LOAD DATA
# =========================
messages = load_messages(DATA_PATH)

if not messages:
    messages = ["No valid messages found"]


# =========================
# SEGMENTATION
# =========================
segments = segment_messages(messages)

topic_data = []
segment_texts = []

def extract_topic_label(summary):
    words = summary.lower().split()
    keywords = [w for w in words if len(w) > 4]
    return " ".join(keywords[:2]) if keywords else "general"

for idx, (s, e) in enumerate(segments):
    segment_msgs = messages[s:e+1]

    summary = summarize(segment_msgs, top_k=2) or "No meaningful content"
    label = extract_topic_label(summary)

    topic_data.append({
        "topic_id": idx + 1,
        "start": s,
        "end": e,
        "summary": summary,
        "label": label
    })

    segment_texts.append(summary)


# =========================
# 100 MESSAGE CHECKPOINTS
# =========================
chunk_data = []
chunk_texts = []

for i in range(0, len(messages), 100):
    chunk = messages[i:i+100]

    summary = summarize(chunk, top_k=3) or "No meaningful content"

    chunk_data.append({
        "start": i,
        "end": min(i + 99, len(messages)-1),
        "summary": summary
    })

    chunk_texts.append(summary)


# =========================
# RAW CHUNKS (FOR BETTER ANSWERS)
# =========================
raw_chunks = []
for i in range(0, len(messages), 20):
    chunk = messages[i:i+20]
    raw_chunks.append(" ".join(chunk))


# =========================
# RETRIEVERS
# =========================
retriever = Retriever(segment_texts + chunk_texts)
raw_retriever = Retriever(raw_chunks)


# =========================
# PERSONA
# =========================
persona = extract_persona(messages)


# =========================
# ANSWER GENERATOR
# =========================
def generate_answer(query):
    summary_results = retriever.query(query, top_k=2)
    raw_results = raw_retriever.query(query, top_k=2)

    context = " ".join(summary_results + raw_results)

    sentences = context.split(".")

    filtered = [
        s.strip() for s in sentences
        if any(word in s.lower() for word in query.lower().split())
    ]

    if not filtered:
        filtered = sentences[:5]

    final_answer = ". ".join(filtered[:5])

    return final_answer if final_answer else "No clear answer found."


# =========================
# ROUTE
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip().lower()

        if not query:
            answer = "Enter a valid question."

        # ===== PERSONA =====
        elif "habit" in query:
            answer = "Habits:\n" + "\n".join(persona.get("habits", []))

        elif "person" in query:
            answer = "Personality:\n" + "\n".join(persona.get("personality", []))

        elif "talk" in query or "style" in query:
            answer = "Communication Style:\n" + "\n".join(persona.get("communication_style", []))

        elif "fact" in query:
            answer = "Personal Facts:\n" + "\n".join(persona.get("personal_facts", []))

        # ===== TOPIC LABELS (NEW FEATURE) =====
        
        elif "topics" in query:
            table_html = """
            <table border="1" style="width:100%; border-collapse: collapse; text-align:center;">
                <tr style="background-color:#333; color:white;">
                    <th>Topic ID</th>
                    <th>Range</th>
                    <th>Topic</th>
                </tr>
            """

            for t in topic_data:
                table_html += f"""
                <tr>
                    <td>{t['topic_id']}</td>
                    <td>{t['start']}-{t['end']}</td>
                    <td>{t['label']}</td>
                </tr>
                """

            table_html += "</table>"

            answer = table_html
        # ===== DEBUG =====
        elif "full topics" in query:
            answer = ""
            for t in topic_data:
                answer += f"Topic {t['topic_id']} ({t['start']}–{t['end']}):\n{t['summary']}\n\n"

        elif "chunks" in query:
            answer = ""
            for c in chunk_data:
                answer += f"Msgs {c['start']}–{c['end']}:\n{c['summary']}\n\n"

        # ===== RAG ANSWER =====
        else:
            answer = generate_answer(query)

    return render_template("index.html", answer=answer)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)