import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_distances

def cluster_segments(embedded_segments, distance_threshold = 0.7):
    embeddings = np.array([seg["embedding"] for seg in embedded_segments])

    distance_matrix = cosine_distances(embeddings)

    clustering = AgglomerativeClustering(
        metric = "precomputed",
        linkage = "average",
        distance_threshold=distance_threshold,
        n_clusters=None
    )

    labels = clustering.fit_predict(distance_matrix)

    clusters = {}
    for label,segment in zip(labels,embedded_segments):
        label = int(label)
        clusters.setdefault(label,[]).append(segment)

    return clusters