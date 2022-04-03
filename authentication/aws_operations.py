import json
from datetime import date
from uuid import uuid4

import boto3
from django.conf import settings


class SNSOperations:
    def __init__(self):
        """
        Initialize AWS SNS client
        """
        self.sns_client = boto3.client(
            "sns",
            region_name="us-east-1",
            aws_access_key_id=settings.AWS_SECRET_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def publish_message(self, subject: str, message: dict):
        """
        Publish message to AWS SNS Topic
        """
        self.sns_client.publish(
            TopicArn=settings.AWS_SNS_ARN,
            Subject=subject,
            Message=json.dumps(message),
            MessageDeduplicationId=str(uuid4()),
            MessageGroupId=f"group-{str(date.today())}",
        )
