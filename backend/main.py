
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.preprocess import preprocess
from services.segmentation import segment_text
from services.embedding import generate_embeddings
from services.clustering import cluster_segments
from services.labeler import label_cluster
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    import time
    start = time.time()

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Empty input text")

    text = request.text

    segments = segment_text(text)
    embedded_segments = generate_embeddings(segments)
    clusters = cluster_segments(embedded_segments)

    # Label clusters
    for cluster in clusters:
        cluster["label"] = label_cluster(cluster["segments"])

        # Remove embeddings from response
        for seg in cluster["segments"]:
            if "embedding" in seg:
                del seg["embedding"]

    end = time.time()
    processing_time = round(end - start, 3)

    clusters.sort(key=lambda c: len(c["segments"]), reverse=True)

    for idx, cluster in enumerate(clusters):
        cluster["cluster_id"] = idx

    return {
    "clusters": clusters,
    "processing_time": processing_time
}

