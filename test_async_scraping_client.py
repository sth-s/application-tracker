#!/usr/bin/env python3
"""Test script for async ScrapingClient."""

import asyncio
import os
import json
from datetime import datetime
from app.clients.scraping_client import ScrapingClient


async def test_async_scraping_client():
    """Test async ScrapingClient with sample URL."""
    
    output_dir = "scraping_test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    client = ScrapingClient()
    url = "https://job.deloitte.com/job-werkstudent-data-quality-inhouse-mwd-_41801?utm_source=linkedin&utm_medium=jobad&utm_campaign=1&utm_content=ad::1220067__k::1__p::LI-MS__b::1__j::41801__ex::65670__pid::auto_c57_j41801_d20240419&src=JB-12762"
    
    print(f"Testing async scraping client with URL: {url}")
    
    try:
        start_time = datetime.now()
        result = await client.get_page_data(url)
        end_time = datetime.now()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        pdf_filename = f"page_{timestamp}.pdf"
        json_filename = f"page_{timestamp}.json"
        
        pdf_path = os.path.join(output_dir, pdf_filename)
        json_path = os.path.join(output_dir, json_filename)
        
        with open(pdf_path, 'wb') as f:
            f.write(result["pdf_content"])
        
        json_data = {
            "url": result["url"],
            "text_content": result["text_content"],
            "text_length": len(result["text_content"]),
            "pdf_size_bytes": len(result["pdf_content"]),
            "scraping_time_ms": int((end_time - start_time).total_seconds() * 1000),
            "timestamp": timestamp
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"PDF saved to: {pdf_path}")
        print(f"JSON data saved to: {json_path}")
        print()
        print("--- Summary ---")
        print(f"URL: {result['url']}")
        print(f"PDF size: {len(result['pdf_content'])} bytes")
        print(f"Text length: {len(result['text_content'])} characters")
        print(f"Scraping time: {json_data['scraping_time_ms']} ms")
        print(f"First 200 chars of text:")
        print(result["text_content"][:200] + "...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")


if __name__ == "__main__":
    asyncio.run(test_async_scraping_client())