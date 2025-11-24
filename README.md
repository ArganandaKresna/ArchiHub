# ArchiHub : Qdrant-Powered Intelligent Research Hub

## 🛠 Tech Stack:

- Vector DB: Qdrant (Cloud atau Docker)
- API Framework: FastAPI + Swagger UI
- Embedding: sentence-transformers + Hugging Face
- Frontend: Streamlit
- ML Ops: MLflow (optional)
- Deployment: Docker + Qdrant Cloud

## Struktur Proyek

```
ArchiHub/
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.frontend
├── requirements.txt
├── app/
│   ├── main.py
│   ├── models.py
│   ├── qdrant_client.py
│   └── __init__.py
├── embedding_service/
│   ├── encoder.py
│   └── __init__.py
├── frontend/
│   └── app.py
└── scripts/
    └── init_data.py
```

## Run Project

### 1. Run Service
```
# Build dan start semua services
docker-compose up -d --build

# Jalankan dengan sample data
docker-compose --profile init up -d
```

### 2. Cek Status Receive
```
docker-compose ps
```

### 3. Akses Service
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs
- Qdrant Dashboard: http://localhost:6333/dashboard

### 4. Stop Service
```
docker-compose down
```

### 5. Hapus Data Service
```
docker-compose down
```