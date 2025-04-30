FROM python:3.11-slim

WORKDIR  /client/
COPY app .
COPY requirenments.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirenments.txt

ENTRYPOINT ["python3", "/client/runner.py"]