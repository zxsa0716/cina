# CINA — reproducible runtime image
# Usage:
#   docker build -t cina .
#   docker run --rm -v $(pwd):/work cina python -m src.run_all --skip-rgat
#   docker run --rm cina python -m src.stage1_extract.llm_smoke_test --offline

FROM python:3.11-slim

LABEL org.opencontainers.image.title="CINA"
LABEL org.opencontainers.image.description="Climate Issue-Network Analysis — multi-axis LLM stance extraction + heterogeneous R-GAT + graph-grounded briefing"
LABEL org.opencontainers.image.authors="Heedo Choi <zxsa0716@kookmin.ac.kr>"
LABEL org.opencontainers.image.url="https://github.com/zxsa0716/cina"
LABEL org.opencontainers.image.source="https://github.com/zxsa0716/cina"
LABEL org.opencontainers.image.version="3.0.0"
LABEL org.opencontainers.image.licenses="MIT"

# Use a non-root user
RUN useradd -m -u 1000 cina

WORKDIR /work

# Install system deps minimal
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       git \
       curl \
       ca-certificates \
       libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r /tmp/requirements.txt

# Copy project
COPY . /work
RUN chown -R cina:cina /work

USER cina

# Default: show help
CMD ["python", "-c", "print('CINA v3.0.0 — try: python -m src.run_all  /  python -m src.stage1_extract.llm_smoke_test --offline')"]
