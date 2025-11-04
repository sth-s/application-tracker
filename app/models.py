"""Pydantic models for request/response validation."""

import datetime
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    """Application status enumeration."""
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    IN_PROGRESS = "In Progress"  
    INTERVIEW_SCHEDULED = "Interview Scheduled"
    INTERVIEW_COMPLETED = "Interview Completed"
    OFFER_RECEIVED = "Offer Received"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"
    ACCEPTED = "Accepted"


class JobGrade(str, Enum):
    """Job level enumeration."""
    INTERNSHIP = "Internship"
    WERKSTUDENT = "Werkstudent"
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
    LEAD = "Lead"
    PRINCIPAL = "Principal"
    OTHER = "Other"


class ExtractionStatus(str, Enum):
    """Extraction status enumeration."""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class VacancyProcessRequest(BaseModel):
    """Request model for processing vacancy URL."""
    url: str


class VacancyProcessResponse(BaseModel):
    """Initial response model for vacancy processing."""
    application_id: str = Field(description="Unique application identifier")
    vacancy_url: str = Field(description="Original vacancy URL")
    extraction_status: ExtractionStatus = ExtractionStatus.PENDING
    application_status: ApplicationStatus = ApplicationStatus.DRAFT

class VacancyLLMResponse(BaseModel):
    """Response model with extracted vacancy data from LLM."""
    company_name: str
    role_title: str
    job_grade: Optional[JobGrade] = Field(None, description="Job level")
    expected_salary: Optional[str] = Field(None, description="Expected salary range")
    contact_person: Optional[str] = Field(None, description="Recruiter or contact person name or email")
    requirements: Optional[List[str]] = Field(None, description="List of job requirements")


class Application(BaseModel):
    """Full application model matching DynamoDB schema."""
    application_id: str = Field(description="Unique application identifier")
    vacancy_url: str = Field(description="Original vacancy URL")
    
    extraction_status: ExtractionStatus = Field(ExtractionStatus.PENDING, description="Extraction status of the vacancy data")
    application_status: ApplicationStatus = Field(ApplicationStatus.DRAFT, description="Application status")
    
    created_at: str = Field(default_factory=lambda: datetime.now(datetime.timezone.utc).isoformat(), description="Creation date in ISO 8601 format")
    last_update_date: str = Field(default_factory=lambda: datetime.now(datetime.timezone.utc).isoformat(), description="Last update date in ISO 8601 format")

    company_name: Optional[str] = Field(None, description="Company name")
    role_title: Optional[str] = Field(None, description="Job role title")
    job_grade: Optional[JobGrade] = Field(None, description="Job level")
    expected_salary: Optional[str] = Field(None, description="Expected salary range")
    requirements: Optional[List[str]] = Field(None, description="List of job requirements")
    contact_person: Optional[str] = Field(None, description="Recruiter or contact person name")

    submission_date: Optional[str] = Field(None, description="Application submission date in ISO 8601 format")
    rejection_reason: Optional[str] = Field(None, description="Reason for rejection if applicable")
    comment: Optional[str] = Field(None, description="Additional comments or notes")
    cv_s3_key: Optional[str] = Field(None, description="S3 key for CV file")
    cl_s3_key: Optional[str] = Field(None, description="S3 key for Cover Letter file")
    vacancy_snapshot_s3_key: Optional[str] = Field(None, description="S3 key for vacancy HTML snapshot")