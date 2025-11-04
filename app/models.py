"""Pydantic models for request/response validation."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    """Application status enumeration."""
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


class VacancyProcessRequest(BaseModel):
    """Request model for processing vacancy URL."""
    url: str

class VacancyLLMResponse(BaseModel):
    """Response model with extracted vacancy data from LLM."""
    company_name: str
    role_title: str
    job_grade: Optional[JobGrade] = Field(None, description="Job level")
    expected_salary: Optional[str] = Field(None, description="Expected salary range")
    contact_person: Optional[str] = Field(None, description="Recruiter or contact person name")
    requirements: Optional[List[str]] = Field(None, description="List of job requirements")

class VacancyProcessResponse(BaseModel):
    """Response model with extracted vacancy data."""
    company_name: str
    role_title: str
    vacancy_url: str
    job_grade: Optional[JobGrade] = Field(None, description="Job level")
    expected_salary: Optional[str] = Field(None, description="Expected salary range")
    contact_person: Optional[str] = Field(None, description="Recruiter or contact person name")
    vacancy_snapshot_s3_key: Optional[str] = Field(None, description="S3 key for vacancy HTML snapshot")


class ApplicationSubmitRequest(BaseModel):
    """Request model for submitting job application."""
    company_name: str
    role_title: str
    vacancy_url: str
    status: ApplicationStatus = Field(default=ApplicationStatus.SUBMITTED, description="Application status")
    job_grade: Optional[JobGrade] = Field(None, description="Job level")
    expected_salary: Optional[str] = Field(None, description="Expected salary range")
    contact_person: Optional[str] = Field(None, description="Recruiter or contact person name")
    rejection_reason: Optional[str] = Field(None, description="Reason for rejection if applicable")
    comment: Optional[str] = Field(None, description="Additional comments or notes")


class ApplicationResponse(BaseModel):
    """Response model for application submission."""
    application_id: str = Field(description="Unique application identifier")
    message: Optional[str] = Field(None, description="Additional status message")


class Application(BaseModel):
    """Full application model matching DynamoDB schema."""
    application_id: str = Field(description="Unique application identifier")
    company_name: str = Field(description="Company name")
    role_title: str = Field(description="Job role title")
    vacancy_url: str = Field(description="Original vacancy URL")
    status: ApplicationStatus = Field(description="Application status")
    submission_date: str = Field(description="Application submission date in ISO 8601 format")
    last_update_date: str = Field(description="Last update date in ISO 8601 format")
    job_grade: Optional[JobGrade] = Field(None, description="Job level")
    expected_salary: Optional[str] = Field(None, description="Expected salary range")
    contact_person: Optional[str] = Field(None, description="Recruiter or contact person name")
    rejection_reason: Optional[str] = Field(None, description="Reason for rejection if applicable")
    comment: Optional[str] = Field(None, description="Additional comments or notes")
    cv_s3_key: Optional[str] = Field(None, description="S3 key for CV file")
    cl_s3_key: Optional[str] = Field(None, description="S3 key for Cover Letter file")
    vacancy_snapshot_s3_key: Optional[str] = Field(None, description="S3 key for vacancy HTML snapshot")


