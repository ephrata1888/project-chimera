FROM python:3.11-slim-bullseye

WORKDIR /workspace

# System dependencies
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        ca-certificates curl gnupg2 build-essential \
    ; \
    rm -rf /var/lib/apt/lists/*

# Node.js 20 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /workspace

# Node dependencies
RUN if [ -f package.json ]; then npm install --no-progress --no-audit; fi

# Python dependencies
RUN pip install --no-cache-dir -r tools/git_mcp/requirements.txt || true
RUN pip install --no-cache-dir -r tools/filesystem_mcp/requirements.txt || true

# Logs directory
RUN mkdir -p /workspace/logs

# Expose MCP ports
EXPOSE 8000 9000

# Start script
COPY start_mcp.sh /usr/local/bin/start_mcp.sh
RUN chmod +x /usr/local/bin/start_mcp.sh
CMD ["/usr/local/bin/start_mcp.sh"]
