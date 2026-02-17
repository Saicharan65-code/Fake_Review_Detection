FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY config.py /app/
COPY detector/fake_review_api.py /app/
COPY utils/ /app/utils/

CMD ["uvicorn", "fake_review_api:app", "--host", "0.0.0.0", "--port", "8000"]
