FROM python:3.10-slim
COPY hmm.py /app/hmm.py
CMD ["python", "/app/hmm.py"]