FROM python:3.14-slim

# Avoid .pyc files and enable unbuffered logging (critical for Docker logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system-level dependencies for common SRE Python libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    python3-dev \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install SRE-focused libraries directly for your toolbox
RUN pip install --no-cache-dir \
    boto3 \
    requests \
    httpx \
    prometheus-client \
    kubernetes \
    pandas \
    paramiko \
    python-dotenv

# Copy your local scripts
COPY . .

# Default to an interactive shell so you can run scripts manually
CMD ["python3"]
