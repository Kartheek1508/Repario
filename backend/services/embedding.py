from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(segments):
    texts = [segment["text"] for segment in segments]

    vectors = model.encode(texts)

    embedded_segments = []

    for i, segment in enumerate(segments):
        embedded_segments.append({
            "id": segment["id"],
            "text": segment["text"],
            "embedding": vectors[i].tolist()
        })

    return embedded_segments

