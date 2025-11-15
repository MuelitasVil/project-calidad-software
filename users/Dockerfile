FROM python:3.11-slim
WORKDIR /code
RUN apt-get update && apt-get install -y curl && apt-get clean
RUN curl https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem \
    -o /etc/ssl/certs/rds-combined-ca-bundle.pem
RUN pip install --upgrade pip
COPY . .
RUN pip install --no-cache-dir --upgrade -r app/requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
EXPOSE 8001