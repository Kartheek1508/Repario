
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.services.preprocess import preprocess
from backend.services.segmentation import segment_text

app = FastAPI()

class AnalyzeRequest(BaseModel):
    text: str

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        cleaned = preprocess(request.text)
        segments = segment_text(cleaned)

        return {
            "segments": segments
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

