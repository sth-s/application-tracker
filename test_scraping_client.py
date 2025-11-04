#!/usr/bin/env python3
"""Test script for ScrapingClient."""

import json
import os
from datetime import datetime
from app.clients.scraping_client import ScrapingClient


def test_scraping_client():
    """Test ScrapingClient with a sample URL."""
    
    # Create output directory
    output_dir = "scraping_test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize client
    client = ScrapingClient(timeout=30000, headless=True)
    
    # Test URL - you can change this
    test_url = "https://job.deloitte.com/job-werkstudent-data-quality-inhouse-mwd-_41801?utm_source=linkedin&utm_medium=jobad&utm_campaign=1&utm_content=ad::1220067__k::1__p::LI-MS__b::1__j::41801__ex::65670__pid::auto_c57_j41801_d20240419&src=JB-12762"  # Example job URL
    # Or try a simpler one:
    # test_url = "https://example.com"
    
    print(f"Testing scraping client with URL: {test_url}")
    
    try:
        # Get page data
        result = client.get_page_data(test_url)
        
        # Generate timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save PDF content
        pdf_file = f"{output_dir}/page_{timestamp}.pdf"
        with open(pdf_file, 'wb') as f:
            f.write(result["pdf_content"])
        print(f"PDF saved to: {pdf_file}")
        
        # Save text content as JSON
        json_file = f"{output_dir}/page_{timestamp}.json"
        json_data = {
            "url": result["url"],
            "text_content": result["text_content"],
            "pdf_size_bytes": len(result["pdf_content"]),
            "text_length": len(result["text_content"]),
            "timestamp": timestamp
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        print(f"JSON data saved to: {json_file}")
        
        # Print summary
        print(f"\n--- Summary ---")
        print(f"URL: {result['url']}")
        print(f"PDF size: {len(result['pdf_content'])} bytes")
        print(f"Text length: {len(result['text_content'])} characters")
        print(f"First 200 chars of text:\n{result['text_content'][:200]}...")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_scraping_client()