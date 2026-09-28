# Dockerfile for the delivery metrics simulator.
# NOTE: The lab manual's Jenkinsfile runs 'docker build -t delivery_metrics .' but does not provide
# a Dockerfile; this one containerizes delivery_metrics.py so that stage can actually run.
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir prometheus-client
COPY delivery_metrics.py .
EXPOSE 8000
CMD ["python", "-u", "delivery_metrics.py"]
