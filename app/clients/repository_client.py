"""Client for interacting with the data repository (DynamoDB)."""

import aioboto3
import os
from enum import Enum
from .. import models

class RepositoryClient:
    """Client for interacting with the data repository (DynamoDB)."""

    def __init__(self):
        self.table_name = os.environ["DYNAMODB_TABLE_NAME"]
        self.session = aioboto3.Session()

    async def create_application_record(self, application: models.Application):
        """Create a new application record in the repository.

        Args:
            application: Application model instance to save.
        """
        async with self.session.resource('dynamodb') as dynamodb:
            try:
                table = await dynamodb.Table(self.table_name)
                item = application.model_dump(exclude_none=True)
                await table.put_item(Item=item)
            except Exception as e:
                print(f"Error creating application record: {e}")
                raise e
    
    async def get_application_by_id(self, application_id: str) -> models.Application | None:
        """Retrieve an application record by its ID.

        Args:
            application_id: The ID of the application to retrieve.

        Returns:
            Application model instance if found, None otherwise.
        """
        async with self.session.resource('dynamodb') as dynamodb:
            try:
                table = await dynamodb.Table(self.table_name)
                response = await table.get_item(Key={"application_id": application_id})
                item = response.get("Item")
                if item:
                    return models.Application.model_validate(item)
                return None
            except Exception as e:
                print(f"Error retrieving application record: {e}")
                raise e


    async def update_application_record(self, application_id: str, updates: dict):
        """Update an existing application record.

        Args:
            application_id: The ID of the application to update.
            updates: A dictionary of fields to update with their new values.
        """
        async with self.session.resource('dynamodb') as dynamodb:
            try:
                table = await dynamodb.Table(self.table_name)

                clean_updates = {}
                for k, v in updates.items():
                    if isinstance(v, Enum):
                        clean_updates[k] = v.value
                    else:
                        clean_updates[k] = v

                update_expression = "SET " + ", ".join(f"{k}= :{k}" for k in clean_updates.keys())
                expression_attribute_values = {f":{k}": v for k, v in clean_updates.items()}

                await table.update_item(
                    Key={"application_id": application_id},
                    UpdateExpression=update_expression,
                    ExpressionAttributeValues=expression_attribute_values
                )
            except Exception as e:
                print(f"Error updating application record: {e}")
                raise e

