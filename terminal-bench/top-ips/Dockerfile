FROM ghcr.io/laude-institute/t-bench/ubuntu-24-04:latest

WORKDIR /app

# Deterministic data generation (fixed seed), so every run starts from the same file.
COPY make_log.py /tmp/make_log.py
RUN python3 /tmp/make_log.py /app/access.log && rm /tmp/make_log.py
