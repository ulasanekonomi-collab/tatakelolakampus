from fastapi import FastAPI
from pydantic import BaseModel

from analyze_interaction import analyze_interaction


app = FastAPI(
    title="TatakelolaKampus AI Engine",
    description="Organizational Sensemaking API",
    version="0.1"
)


class InteractionInput(BaseModel):
    narrative: str


@app.get("/")
def root():
    return {
        "message": "TatakelolaKampus AI Engine is running"
    }


@app.post("/analyze")
def analyze(data: InteractionInput):

    interaction_data = {
        "narrative": data.narrative
    }

    result = analyze_interaction(interaction_data)

    return {
        "status": "success",
        "analysis": result
    }
