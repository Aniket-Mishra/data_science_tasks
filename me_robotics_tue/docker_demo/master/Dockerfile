FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY app.py .

EXPOSE 5010

CMD ["python3", "-u", "app.py"]
