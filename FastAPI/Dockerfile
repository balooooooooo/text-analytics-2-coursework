# FROM python:3.9-slim
FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-runtime

# Set WD
WORKDIR /app

# Install apps
RUN pip install fastapi uvicorn transformers

# Copy files to the container
COPY ./FastAPI/server.py ./app/server.py
COPY ./trained_gpt2_model_large/ ./app/trained_gpt2_model_large/

# Expose the port for FastAPI
EXPOSE 8000

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000" , "--reload"]