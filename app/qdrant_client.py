# app/qdrant_client.py
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from typing import List, Dict, Optional
import uuid
import time

class QdrantManager:
    def __init__(self):
        # Get connection details from environment variables
        host = os.getenv("QDRANT_HOST", "localhost")
        port = int(os.getenv("QDRANT_PORT", "6333"))
        
        print(f"Connecting to Qdrant at {host}:{port}")
        
        # Initialize client with retry logic
        max_retries = 5
        for i in range(max_retries):
            try:
                self.client = QdrantClient(host=host, port=port)
                # Test connection
                self.client.get_collections()
                print("Successfully connected to Qdrant")
                break
            except Exception as e:
                if i < max_retries - 1:
                    print(f"Connection failed, retrying... ({i+1}/{max_retries})")
                    time.sleep(5)
                else:
                    raise Exception(f"Failed to connect to Qdrant after {max_retries} attempts: {e}")
        
        self.collection_name = "research_papers"
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Create collection if not exists"""
        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=384,
                        distance=Distance.COSINE
                    )
                )
                print(f"Collection '{self.collection_name}' created successfully")
            else:
                print(f"Collection '{self.collection_name}' already exists")
                
        except Exception as e:
            print(f"Error ensuring collection: {e}")
            raise
    
    def add_paper(self, embedding: List[float], metadata: Dict) -> str:
        """Add paper to Qdrant"""
        paper_id = str(uuid.uuid4())
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=paper_id,
                    vector=embedding,
                    payload=metadata
                )
            ]
        )
        return paper_id
    
    def search_papers(self, query_embedding: List[float], limit: int = 10, 
                     filter_category: Optional[str] = None) -> List[Dict]:
        """Search papers with optional filtering"""
        
        search_filter = None
        if filter_category:
            search_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="categories",
                        match=models.MatchValue(value=filter_category)
                    )
                ]
            )
        
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            query_filter=search_filter,
            limit=limit
        )
        
        formatted_results = []
        for result in search_results:
            formatted_results.append({
                "id": result.id,
                "score": result.score,
                "title": result.payload.get("title", ""),
                "abstract": result.payload.get("abstract", ""),
                "authors": result.payload.get("authors", []),
                "categories": result.payload.get("categories", [])
            })
        
        return formatted_results
    
    def find_similar_papers(self, paper_id: str, limit: int = 5) -> List[Dict]:
        """Find similar papers using vector similarity"""
        try:
            search_results = self.client.recommend(
                collection_name=self.collection_name,
                positive=[paper_id],
                limit=limit
            )
            
            formatted_results = []
            for result in search_results:
                formatted_results.append({
                    "id": result.id,
                    "score": result.score,
                    "title": result.payload.get("title", ""),
                    "abstract": result.payload.get("abstract", ""),
                })
            
            return formatted_results
        except Exception as e:
            print(f"Error finding similar papers: {e}")
            return []