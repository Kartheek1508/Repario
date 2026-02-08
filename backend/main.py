
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.preprocess import preprocess
from services.segmentation import segment_text
from services.embedding import generate_embeddings
from services.clustering import cluster_segments

app = FastAPI()

class AnalyzeRequest(BaseModel):
    text: str

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        cleaned = preprocess(request.text)
        segments = segment_text(cleaned)
        embedded = generate_embeddings(segments)
        clusters = cluster_segments(embedded)

        return {
            "segments": clusters 
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

