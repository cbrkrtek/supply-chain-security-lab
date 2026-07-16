FROM python:3.11-slim AS builder
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
RUN apt-get update && \
    apt-get purge -y --allow-remove-essential perl-base perl-modules-* && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -u 1000 -m appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY app/ /app
WORKDIR /app
USER 1000
ENV PATH=/home/appuser/.local/bin:$PATH
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
