FROM debian:bookworm-slim

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Set up user and working directory
RUN useradd -m -s /bin/bash ubuntu

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    nodejs \
    npm \
    postgresql-client \
    git \
    curl \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 (LTS)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Python development tools globally
RUN pip3 install --no-cache-dir --break-system-packages \
    pip-tools \
    pytest \
    pytest-xdist \
    black \
    ruff \
    mypy

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Switch to ubuntu user
USER ubuntu
WORKDIR /home/ubuntu

# Set environment variables
ENV PATH="/home/ubuntu/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

