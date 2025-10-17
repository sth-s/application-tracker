"""FastAPI application with job application tracking endpoints."""

from datetime import datetime
from fastapi import FastAPI, File, Form, UploadFile
from typing import List, Optional
import uuid

from .models import (
    VacancyProcessRequest,
    VacancyProcessResponse,
    ApplicationSubmitRequest,
    ApplicationResponse,
    Application,
    ApplicationStatus
)

app = FastAPI(title="Application Tracker API", version="1.0.0")


@app.post("/process-vacancy", response_model=VacancyProcessResponse)
async def process_vacancy(request: VacancyProcessRequest):
    """Extract job information from vacancy URL using LLM.
    
    TODO: Implement actual URL processing with Groq API.
    """
    # Mock response for now
    return VacancyProcessResponse(
        company_name="Example Corp",
        role_title="Software Engineer",
        vacancy_url=request.url,
        expected_salary="$80,000 - $120,000",
        contact_person="Jane Recruiter"
    )


@app.post("/submit-application", response_model=ApplicationResponse)
async def submit_application(request: ApplicationSubmitRequest):
    """Submit job application with extracted data and optional cover letter.
    
    TODO: Implement file upload to S3 and data storage to DynamoDB.
    """
    # Mock response for now
    application_id = str(uuid.uuid4())
    return ApplicationResponse(
        application_id=application_id,
        message="Application submitted successfully"
    )


@app.get("/applications", response_model=List[Application])
async def get_applications():
    """Retrieve all submitted job applications.
    
    TODO: Implement actual data retrieval from DynamoDB.
    """
    # Mock response for now
    mock_application = Application(
        application_id=str(uuid.uuid4()),
        company_name="Example Corp",
        role_title="Software Engineer",
        vacancy_url="https://example.com/job/123",
        status=ApplicationStatus.SUBMITTED,
        submission_date=datetime.now().isoformat(),
        last_update_date=datetime.now().isoformat(),
        expected_salary="$80,000 - $120,000",
        contact_person="Jane Recruiter"
    )
    
    return [mock_application]


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Application Tracker API is running"}