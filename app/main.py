"""FastAPI application with job application tracking endpoints."""

from fastapi import FastAPI, Depends, Request, HTTPException, status
from contextlib import asynccontextmanager
from . import models
from .services import ApplicationService
from .clients.repository_client import RepositoryClient
from .clients.dispatcher_client import DispatcherClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to initialize clients.
    """
    app.state.repo_client = RepositoryClient()
    app.state.dispatcher_client = DispatcherClient()


app = FastAPI(title="Application Tracker API", version="1.0.0")



def get_application_service(request: Request) -> ApplicationService:
    """Dependency to get ApplicationService instance.
    """
    return ApplicationService(
        repo=request.app.state.repo_client, 
        dispatcher=request.app.state.dispatcher_client
    )

@app.post("/process-vacancy",
            response_model=models.VacancyProcessResponse,
            status_code=status.HTTP_202_ACCEPTED
)
async def process_vacancy(
    request: models.VacancyProcessRequest,
    service: ApplicationService = Depends(get_application_service)
):
    """Process vacancy URL to extract information and save snapshot.
    """
    try:
        response_data = await service.create_new_application(request.url)
        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process vacancy: {str(e)}"
        )

@app.get(
    "/applications/{app_id}", 
    response_model=models.VacancyDBModel
)
async def get_application(
    app_id: str,
    service: ApplicationService = Depends(get_application_service)
):
    """Retrieve application details by application ID.
    """
    try:
        application = await service.get_application_by_id(app_id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {app_id} not found"
            )
        return application
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve application: {str(e)}"
        )


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Application Tracker API is running"}