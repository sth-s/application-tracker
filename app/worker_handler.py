"""Worker handler for processing job application URLs."""

import asyncio
import logging
import os
import boto3
import datetime
from datetime import datetime, timezone
from .clients.repository_client import RepositoryClient
from .clients.storage_client import StorageClient
from .clients.scraping_client import ScrapingClient
from .clients.llm_client import LLMClient
from .errors import LLMRateLimitError, ScrapingClientError
from . import models

logger = logging.getLogger()
logger.setLevel("INFO")

def get_groq_key_from_aws() -> str:
    """Retrieve Groq API key from AWS SSM Parameter Store."""
    ssm = boto3.client("ssm", region_name=os.environ["AWS_REGION"])
    param = ssm.get_parameter(
        Name=os.environ["GROQ_API_KEY_SSM_PARAM"],
        WithDecryption=True
    )
    return param["Parameter"]["Value"]


GROQ_API_KEY = get_groq_key_from_aws()
repo_client_instance = RepositoryClient()
storage_client_instance = StorageClient()
scraper_instance = ScrapingClient()
llm_instance = LLMClient(api_key=GROQ_API_KEY)

logger.info("Initialized global client instances in worker_handler.")

async def process_application(application_id: str, vacancy_url: str):
    """Process a job application URL to extract information and save snapshot.

    Args:
        application_id: The ID of the job application.
        vacancy_url: The job application URL to process.

    Returns:
        A dictionary containing the processed application data.
    """
    try:
        await repo_client_instance.update_application_record(application_id, {

            "extraction_status": models.ExtractionStatus.PROCESSING,
            "last_update_date": datetime.now(timezone.utc).isoformat()
        })

        page_data = await scraper_instance.get_page_data(vacancy_url)

        vacancy_data = await llm_instance.extract_vacancy_info(page_data["text_content"])

        pdf_key = await storage_client_instance.save_pdf(page_data["pdf_content"], application_id)

        updates = {
            "extraction_status": models.ExtractionStatus.SUCCESS,
            "application_status": models.ApplicationStatus.DRAFT,
            "last_update_date": datetime.now(timezone.utc).isoformat(),
            "role_title": vacancy_data.role_title,
            "company_name": vacancy_data.company_name,
            "expected_salary": vacancy_data.expected_salary,
            "requirements": vacancy_data.requirements,
            "contact_person": vacancy_data.contact_person,
            "vacancy_snapshot_s3_key": pdf_key
            # "last_updated": 
        }

        await repo_client_instance.update_application_record(application_id, updates)

    except LLMRateLimitError as e:
        logger.error(f"{application_id} LLMRateLimitError: {e}")
        await repo_client_instance.update_application_record(application_id, {
            "extraction_status": models.ExtractionStatus.FAILED,
            "error_message": f"LLM rate limit exceeded: {e}"
        })
        raise e 
    
    except Exception as e:
        logger.critical(f"{application_id} Fatal error: {e}")
        await repo_client_instance.update_application_record(application_id, {
            "extraction_status": models.ExtractionStatus.FAILED,
            "error_message": f"Processing Fatal Failed: {e}"
        })
        raise e

def lambda_handler(event, context):
    """AWS Lambda handler.

    Args:
        event: The event data containing job application details.
        context: The runtime context of the Lambda function.
    """
    application_id = event["application_id"]
    vacancy_url = event["vacancy_url"]

    logger.info(f"Lambda invoked for application_id: {application_id}")

    if not application_id or not vacancy_url:
        logger.error("Missing application_id or url in event.")
        return {"statusCode": 400, "body": "Invalid event data."}

    asyncio.run(process_application(application_id, vacancy_url))

    return {"statusCode": 200, "body": "Processing started."}