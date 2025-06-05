from typing import Optional
from typing import Optional, List

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
    outline: str
    style_anchors: List[str]
    model: str | None = "gpt-4.1-nano"


@app.post("/generate-sectioned-article")
def generate_sectioned_article_endpoint(request: SectionedArticleRequest):
    article = generate_sectioned_article(
        outline=request.outline,
        #style_anchors=request.style_anchors,
        model=request.model,
    )
    return {"article": article}