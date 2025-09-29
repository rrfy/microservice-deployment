FROM python:3.11-slim
WORKDIR /app
COPY hostmetrics.py /app/hostmetrics.py
EXPOSE 8080
CMD ["python3", "/app/hostmetrics.py"]
