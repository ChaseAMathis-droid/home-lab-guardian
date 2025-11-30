FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 hlg && \
    mkdir -p /app && \
    chown -R hlg:hlg /app

WORKDIR /app

# Copy dependency files
COPY --chown=hlg:hlg pyproject.toml README.md ./

# Install dependencies
RUN pip install --no-cache-dir -e .

# Copy application code
COPY --chown=hlg:hlg src/ ./src/

# Switch to non-root user
USER hlg

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import hlg; print('healthy')" || exit 1

# Run the agent
ENTRYPOINT ["hlg"]
CMD ["run"]
