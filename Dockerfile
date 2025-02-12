FROM python:3.10

WORKDIR /app
COPY pi_service.py .
COPY shard_* .  
# Copy all shards
RUN pip install flask

CMD ["python", "pi_service.py"]
