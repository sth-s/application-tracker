"""Scraping client for web content extraction."""

import re
from typing import Dict, Any
from playwright.sync_api import sync_playwright
from ..errors import ScrapingError, ScrapingTimeoutError, ScrapingContentError


class ScrapingClient:
    """Client for scraping web pages and extracting content."""
    
    def __init__(self, timeout: int = 30000, headless: bool = True):
        """Initialize scraping client.
        
        Args:
            timeout: Page load timeout in milliseconds.
            headless: Whether to run browser in headless mode.
        """
        self.timeout = timeout
        self.headless = headless
    
    def get_page_data(self, url: str) -> Dict[str, Any]:
        """Get PDF and text content from a web page.
        
        Args:
            url: The URL to scrape.
            
        Returns:
            Dictionary with PDF content and clean text content.
            
        Raises:
            Exception: If scraping fails with wrapped original error.
        """
        browser = None
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=self.headless, 
                    args=['--no-sandbox', '--disable-dev-shm-usage']
                )
                page = browser.new_page()
                
                page.set_extra_http_headers({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                })
                
                page.goto(url, timeout=self.timeout)
                page.wait_for_load_state("load", timeout=15000)
                
                # Wait a bit for dynamic content and cookie banners
                page.wait_for_timeout(2000)

                self._handle_cookie_consent(page)
                
                # Wait again in case there are delayed elements
                page.wait_for_timeout(1000)
                
                pdf_content = page.pdf(format='A4', print_background=True)
                text_content = self._extract_text(page)
                
                browser.close()
                
                return {
                    "pdf_content": pdf_content,
                    "text_content": text_content,
                    "url": url
                }
        except Exception as e:
            if browser:
                try:
                    browser.close()
                except:
                    pass
            
            error_msg = str(e).lower()
            
            if "timeout" in error_msg or "timed out" in error_msg:
                raise ScrapingTimeoutError(f"Scraping timeout for {url}: {str(e)}")
            elif "content" in error_msg or "extract" in error_msg:
                raise ScrapingContentError(f"Content extraction failed for {url}: {str(e)}")
            else:
                raise ScrapingError(f"Scraping failed for {url}: {str(e)}")
    
    def _extract_text(self, page) -> str:
        """Extract clean text from page.
        
        Args:
            page: Playwright page object.
            
        Returns:
            Clean text content.
        """
        title = page.title() or ""
        
        try:
            main_text = page.locator("main").first.inner_text()
        except:
            main_text = page.locator("body").inner_text()
        
        full_text = f"{title}\n\n{main_text}" if title else main_text
        return self._clean_text(full_text)
    
    def _clean_text(self, text: str) -> str:
        """Clean text content.
        
        Args:
            text: Raw text to clean.
            
        Returns:
            Cleaned text.
        """
        if not text:
            return ""
        
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)
        text = re.sub(r'[^\w\s\.,!?;:()\-\n\'"@#$%&+=<>/\\|`~\[\]{}]', ' ', text)
        text = re.sub(r' +', ' ', text)
        
        return text.strip()
    
    def _handle_cookie_consent(self, page):
        """Handle cookie consent banners by clicking accept buttons.
        
        Args:
            page: Playwright page object.
        """
        cookie_selectors = [
            # English accept button texts
            'button:has-text("Accept")',
            'button:has-text("Accept all")', 
            'button:has-text("Allow all")',
            'button:has-text("OK")',
            'button:has-text("I agree")',
            'button:has-text("Agree")',
            'button:has-text("Continue")',
            'button:has-text("Got it")',
            
            # German accept button texts
            'button:has-text("Akzeptieren")',
            'button:has-text("Alle akzeptieren")',
            'button:has-text("Alle Cookies akzeptieren")',
            'button:has-text("Einverstanden")',
            'button:has-text("Zustimmen")',
            'button:has-text("OK")',
            
            # French accept button texts  
            'button:has-text("Accepter")',
            'button:has-text("J\'accepte")',
            'button:has-text("Tout accepter")',
            
            # Common data attributes and IDs
            '[data-testid*="accept"]',
            '[data-testid*="consent"]',
            '[id*="accept"]',
            '[id*="consent"]',
            '[id*="cookie"]',
            
            # Common classes
            '[class*="accept"]',
            '[class*="consent"]',
            '[class*="cookie"]',
            'button[class*="primary"]',
            
            # Generic selectors in cookie containers
            '[class*="cookie"] button:first-child',
            '[class*="consent"] button:first-child', 
            '[id*="cookie"] button:first-child',
            '.cookie-banner button',
            '#cookie-banner button',
            
            # Fallback - any prominent button
            'button[type="submit"]'
        ]
        
        for selector in cookie_selectors:
            try:
                button = page.locator(selector).first
                if button.is_visible(timeout=2000):
                    button.click(timeout=2000)
                    page.wait_for_timeout(1000)
                    break
            except:
                continue