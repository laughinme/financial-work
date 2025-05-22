FROM python:3.13-slim

WORKDIR /app

COPY req.txt .
RUN pip install --no-cache-dir -r req.txt


COPY src ./src 
COPY entry.sh .

ENV PYTHONPATH=/app/src

RUN chmod +x entry.sh

EXPOSE 8080

ENTRYPOINT ["./entry.sh"]