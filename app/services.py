"""Business logic services"""

import uuid
from . import models
from .clients.repository_client import RepositoryClient
from .clients.dispatcher_client import DispatcherClient


class ApplicationService:
    """Service for handling application processing logic.
    """

    def __init__(self, repo: RepositoryClient, dispatcher: DispatcherClient):
            self.repo = repo
            self.dispatcher = dispatcher

    async def create_new_application(self, vacancy_url: str) -> models.VacancyProcessResponse:
        """Create a new "Pending" application record and dispatch processing.

        Args:
            vacancy_url: The vacancy URL to process.

        Returns:
            The response from the vacancy processing.
        """
        application_id = str(uuid.uuid4())

        new_application = models.Application(
            application_id=application_id,
            vacancy_url=vacancy_url
        )
        await self.repo.create_application_record(new_application)
        self.dispatcher.invoke_worker_lambda({"application_id": application_id, "vacancy_url": url})
        return models.VacancyProcessResponse(
            application_id=application_id,
            vacancy_url=vacancy_url,
            extraction_status=models.ExtractionStatus.PENDING,
            application_status=models.ApplicationStatus.DRAFT
        )
    

    async def get_application_by_id(self, application_id: str) -> models.VacancyDBModel | None:
         """Retrieve application details by application ID.

         Args:
             application_id: The ID of the application to retrieve.

         Returns:
             The application details or None if not found.
         """
         return await self.repo.get_application_by_id(application_id)