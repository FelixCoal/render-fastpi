from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from services.sectioned_article_gen import generate_sectioned_article

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

class SectionedArticleRequest(BaseModel):
    outline: List[dict]
    #style_anchors: List[str]
    model: str | None = "gpt-4.1-nano"
    model_summary: str | None = "gpt-4.1-nano"
    targetAudience: str | None = "general public"
    articleIntent: str | None = "informative"
    writingTone: str | None = "neutral"
    writersPersona: str | None = "expert in the field"


@app.post("/generate-sectioned-article")
def generate_sectioned_article_endpoint(request: SectionedArticleRequest):
    article = generate_sectioned_article(
        outline=request.outline,
        #style_anchors=request.style_anchors#,
        model=request.model,
        model_summary=request.model_summary,
        targetAudience=request.targetAudience,
        articleIntent=request.articleIntent,
        writingTone=request.writingTone,
        writersPersona=request.writersPersona
    )
    return {"article": article}
