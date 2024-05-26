# app/Dockerfile

FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . /app/.
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit/main.py", "--server.port=8501", "--server.address=0.0.0.0"]