"""
Central module for all clean business errors in the application.

This module contains the exception hierarchy for all domain errors.
Each error inherits from ApplicationError for unified handling.
"""


# Base errors
class ApplicationError(Exception):
    """Base exception for the entire application."""
    
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(message)


# LLM client errors
class LLMClientError(ApplicationError):
    """Base error for LLM client."""
    pass


class LLMValidationError(LLMClientError):
    """LLM response validation error (Pydantic ValidationError)."""
    pass


class LLMRateLimitError(LLMClientError):
    """LLM API rate limit exceeded error."""
    pass


class LLMConnectionError(LLMClientError):
    """LLM API connection error."""
    pass


class LLMTimeoutError(LLMClientError):
    """LLM API request timeout error."""
    pass


# Scraping errors
class ScrapingError(ApplicationError):
    """Base scraping error."""
    pass


class ScrapingBannedError(ScrapingError):
    """IP blocked or bot detection error."""
    pass


class ScrapingTimeoutError(ScrapingError):
    """Page load timeout error."""
    pass


class ScrapingContentError(ScrapingError):
    """Content extraction error."""
    pass


# AWS errors
class AWSError(ApplicationError):
    """Base AWS services error."""
    pass


class S3UploadError(AWSError):
    """S3 file upload error."""
    pass


# Data validation errors
class DataValidationError(ApplicationError):
    """Input data validation error."""
    pass


class InvalidURLError(DataValidationError):
    """Invalid URL error."""
    pass