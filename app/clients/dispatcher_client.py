"""Client for invoking AWS Lambda functions."""

import boto3
import json
import os

class DispatcherClient:
    """Client for invoking AWS Lambda functions."""

    def __init__(self):
        self.lambda_client = boto3.client('lambda')
        self.worker_lambda_name = os.environ["WORKER_LAMBDA_NAME"]

    def invoke_worker_lambda(self, payload: dict) -> None:
        """Invoke the worker Lambda function with the given payload.

        Args:
            payload: The payload to send to the worker Lambda.
        """
        self.lambda_client.invoke(
            FunctionName=self.worker_lambda_name,
            InvocationType='Event',
            Payload=json.dumps(payload)
        )