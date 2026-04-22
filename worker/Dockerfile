FROM python:3.11-slim as builder
RUN pip install --upgrade pip && \
pip install --no-cache-dir uv
WORKDIR /app
COPY pyproject.toml uv.lock /app/
RUN uv sync --no-cache

FROM python:3.11-slim
RUN apt-get update && apt-get -y install curl=8.19.0-3 --no-install-recommends && \
rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY worker.py /app
RUN useradd -m app && chown -R app:app /app
USER app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD [ "pgrep", "-x", "python3" ]
ENTRYPOINT [ "python3", "worker.py"]