"""Business logic services for application processing."""

from typing import Dict, Any
from .clients import ScrapingClient, save_pdf_to_s3_stub


def process_vacancy_service(url: str) -> Dict[str, Any]:
    """Process vacancy URL by scraping content and saving PDF snapshot.
    
    Args:
        url: The URL of the vacancy page to process.
        
    Returns:
        Dictionary containing scraped data and S3 key for PDF snapshot.
    """
    scraping_client = ScrapingClient()
    page_data = scraping_client.get_page_data(url)
    
    s3_key = save_pdf_to_s3_stub(page_data["pdf_content"], url)
    
    return {
        "text_content": page_data["text_content"],
        "vacancy_snapshot_s3_key": s3_key,
        "url": url
    }
