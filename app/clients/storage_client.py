"""Client for AWS S3 storage interactions."""

import aioboto3
import os
import uuid
from .. import models
from ..errors import ApplicationError

class StorageClient:
    """Client for interacting with AWS S3 storage."""

    def __init__(self):
        self.bucket_name = os.environ["S3_BUCKET_NAME"]
        self.session = aioboto3.Session()

    async def save_pdf(self, pdf_bytes: bytes, application_id: str) -> str:
        """Save PDF bytes to S3 and return the S3 key.

        Args:
            pdf_bytes: The PDF content in bytes.
            application_id: The ID of the application for naming the file.

        Returns:
            The S3 key of the saved PDF file.
        """
        try:
              
            s3_key = f"applications/{application_id}/snapshot-{uuid.uuid4()}.pdf"

            async with self.session.client("s3") as s3_client:
                await s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                    Body=pdf_bytes,
                    ContentType="application/pdf"
                )
                return s3_key

        except Exception as e:
            print(f"Error saving PDF to S3: {e}")
            raise ApplicationError("Failed to save PDF to S3")