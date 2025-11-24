# app/models.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class PaperRequest(BaseModel):
    title: str
    abstract: str
    authors: List[str]
    publication_date: str
    categories: List[str]

class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    category_filter: Optional[str] = None

class SimilarPapersRequest(BaseModel):
    paper_id: str
    limit: int = 5