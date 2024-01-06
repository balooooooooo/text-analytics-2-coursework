# Docker-compose

## DockerStreamlit

```docker
docker buildx build . -t ta_streamlit --file DockerfileStreamlit
docker run -p 8501:8501 ta_streamlit
```

## FastAPI

```docker
docker buildx build . -t ta_fastapi --file DockerfileFastAPI
docker run -p 8501:8501 ta_fastapi
```