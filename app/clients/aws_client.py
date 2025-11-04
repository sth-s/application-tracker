"""AWS client for S3 and DynamoDB operations."""

from datetime import datetime
from urllib.parse import urlparse


def save_pdf_to_s3_stub(pdf_content: bytes, url: str) -> str:
    """Save PDF content to S3 (stub implementation).
    
    Args:
        pdf_content: PDF bytes content to save.
        url: Original URL of the vacancy.
        
    Returns:
        S3 key where the PDF would be stored.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('.', '-')
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    
    return f"vacancy-snapshots/{domain}/{timestamp}.pdf"