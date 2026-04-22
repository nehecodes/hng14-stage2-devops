FROM python:3.11-slim as builder
RUN pip install --no-cache-dir --upgrade pip==24.3.1 && \
pip install --no-cache-dir uv==0.11.7
WORKDIR /app
COPY pyproject.toml uv.lock /app/
RUN uv sync --no-cache

FROM python:3.11-slim
RUN apt-get update && apt-get -y install curl=8.19.0-3 --no-install-recommends && \
rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY main.py config.py  /app/
RUN useradd -m app && chown -R app:app /app
USER app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD [ "curl", "--fail", "http://127.0.0.1:8000/health" ]
ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]