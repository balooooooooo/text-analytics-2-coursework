# Docker-compose

## FastAPI

```docker
docker build -t backend -f FastAPI/Dockerfile .
docker run -p 8000:8000 backend
```

## Streamlit

```docker
docker build -t frontend -f Streamlit/Dockerfile Streamlit/
docker run -p 8501:8501 frontend
```