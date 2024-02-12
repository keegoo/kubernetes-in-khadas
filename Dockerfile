FROM python:3.10-slim

WORKDIR /app
COPY app/ /app
RUN pip install -r requirements.txt

ENV DDNS_API_KEY=${DDNS_API_KEY}
CMD ["python", "update_ip.py"]