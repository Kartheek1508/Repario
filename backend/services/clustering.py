from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import normalize
import numpy as np

def cluster_segments(embedded_segments, similarity_threshold=0.75):

    embeddings = np.array([seg["embedding"] for seg in embedded_segments])

    embeddings = normalize(embeddings)

    clustering = AgglomerativeClustering(
        n_clusters=None,
        metric="cosine",
        linkage="average",
        distance_threshold=1 - similarity_threshold
    )

    labels = clustering.fit_predict(embeddings)

    clusters = {}

    for label, segment in zip(labels, embedded_segments):
        clusters.setdefault(label, []).append(segment)

    return [
        {"cluster_id": int(label), "segments": segments}
        for label, segments in clusters.items()
    ]

