"""AWS clients for S3 and DynamoDB operations."""

from datetime import datetime
from urllib.parse import urlparse


def save_html_to_s3_stub(html_content: str, url: str) -> str:
    """Save HTML content to S3 (stub implementation).
    
    Args:
        html_content: Full HTML content to save.
        url: Original URL of the vacancy.
        
    Returns:
        S3 key where the HTML would be stored.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('.', '-')
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    
    return f"vacancy-snapshots/{domain}/{timestamp}.html"