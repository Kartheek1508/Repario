import re
from collections import Counter
def label_cluster(segments):
    texts = [seg["text"] for seg in segments]

    combined = " ".join(texts).lower()

    STOPWORDS = {
        "is", "was", "were", "the", "a", "an", "under", "when",
        "also", "and", "or", "to", "of", "in", "on", "at",
        "for", "with", "by", "vs"
    }

    words = re.findall(r'\b[a-zA-Z]+\b', combined)
    filtered = [w for w in words if w not in STOPWORDS]

    if not filtered:
        return "General Topic"

    freq = Counter(filtered)
    top_words = [word for word, _ in freq.most_common(2)]

    return " ".join(w.capitalize() for w in top_words)
