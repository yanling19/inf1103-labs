FROM python:3.11-slim
WORKDIR /app
COPY object_auditor.py .
CMD ["python", "object_auditor.py"]