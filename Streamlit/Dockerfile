FROM python:3.9-slim

# Set WD
WORKDIR /app
COPY app.py ./app.py

# Install apps
RUN pip install streamlit 

# Expose port
EXPOSE 8501

# Start streamlit app
ENTRYPOINT ["streamlit","run"]
CMD ["app.py"]