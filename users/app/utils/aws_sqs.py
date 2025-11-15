# app/utils/aws_sqs.py
import os
import json
import boto3
import uuid
from botocore.exceptions import ClientError


REGION = os.getenv("AWS_REGION", "us-east-1")
QUEUE_URL = os.getenv("SQS_QUEUE_URL")

sqs_client = boto3.client("sqs", region_name=REGION)

def send_message_to_sqs(message_body: dict):
    """
    Envía un mensaje a la cola SQS configurada.
    """
    if not QUEUE_URL:
        raise RuntimeError("SQS_QUEUE_URL no está configurada en las variables de entorno")
    print(f"Preparando mensaje para ser enviado a la SQS")
    message_id = str(uuid.uuid4())

    message_body["id"] = message_id

    try:
        response = sqs_client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message_body),
            MessageAttributes={
                "Id": {
                    "StringValue": message_id,
                    "DataType": "String"
                }
            }
        )
        print(f"✅ Mensaje enviado a SQS con id={message_id}")
        return response
    except ClientError as e:
        print(f"❌ Error enviando mensaje a SQS: {e}")
        raise