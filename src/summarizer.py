from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def clean_texts(text_list):
    # remove empty or very small messages
    return [t.strip() for t in text_list if t and len(t.strip()) > 3]

def summarize(text_list, top_k=3):
    text_list = clean_texts(text_list)

    # fallback if nothing valid
    if len(text_list) == 0:
        return ""

    if len(text_list) <= top_k:
        return " ".join(text_list)

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        X = vectorizer.fit_transform(text_list)

        scores = np.sum(X.toarray(), axis=1)
        ranked = np.argsort(scores)[::-1]

        selected = [text_list[i] for i in ranked[:top_k]]
        return " ".join(selected)

    except Exception:
        # fallback if TF-IDF fails
        return " ".join(text_list[:top_k])