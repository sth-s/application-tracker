"""LLM client for extracting structured information from vacancy text."""

import os
import json
import time
from typing import Union, Dict, Any
from ..models import VacancyLLMResponse
from ..errors import LLMClientError, LLMValidationError, LLMRateLimitError
from groq import AsyncGroq, RateLimitError, APIConnectionError, APITimeoutError
from pydantic import ValidationError


class LLMClient:
    """Client for interacting with LLM API to extract vacancy information."""
    
    def __init__(self, api_key: str, model: str = "meta-llama/llama-4-maverick-17b-128e-instruct", temperature: float = 0.2, max_tokens: int = 1000):
        """Initialize LLM client.
        
        Args:Configure your API key as an environment variable. This approach streamlines your API usage by eliminating the need to include your API key in each request. Moreover, it enhances security by minimizing the risk of inadvertently including your API key in your codebase.
            api_key: API key for LLM service.
            model: Model name to use.
        """
        if not api_key:
            raise ValueError("API key for LLM service must be provided.")
        
        self.client = AsyncGroq(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_prompt = """
            ### System
            You are an expert AI assistant. Your task is to extract key information from a job vacancy text 
            by returning a JSON object that adheres to the provided JSON Schema.

            ### Instructions
            You MUST follow these rules when populating the tool arguments:

            1.  **company_name:** Find the employer company name.
                * IMPORTANT: Always prioritize the employer brand (e.g., "BMW Group" from "unser Team bei der BMW Group") 
                over the legal entity (e.g., "BMW AG" from "Unternehmensbereich:").

            2.  **role_title:** Find the exact, specific job title.
                * CRITICAL HINT: The text is "dirty" and contains navigation links (e.g., 'Internships', 'Register', 'Sign in') 
                and section headers (e.g., 'Description', 'Project Description', 'Requirements', 'About Us', 'Task Teaser', 'Admission').
                * YOU MUST IGNORE ALL of these navigation links and section headers. They are NOT the job title.
                * The `role_title` is the *specific name of the project or position* the page is describing. 
                It is almost always located *after* the navigation noise but *before* the first 'Description' or 'Project Description' block.
                * EXAMPLE: For a text starting with "JetBrains Internship Application Internships Register Sign in Analytics of ML Features Usage in IDEs Description...", 
                the correct `role_title` is "Analytics of ML Features Usage in IDEs".

            3.  **grade:** Determine the job grade from the tool's Enum list.
                * RULE: "Praktikant" or "Intern" = "Internship".
                * RULE: "Werkstudent" or "Working Student" = "Werkstudent".
                * RULE: If the grade is not specified or unclear, use "Other".

            4.  **expected_salary:** Find the specified salary.
                * RULE: If the salary is not mentioned as numbers or a range (e.g., "attractive salary"), 
                you MUST pass `null`.

            5.  **contact_person:** Find the recruiter's name or contact person.
                * RULE: If a name (e.g., Anna Schmidt) or email is not explicitly mentioned, 
                you MUST pass `null`.
        """
    
    async def extract_vacancy_info(self, text_content: str, include_stats: bool = False) -> Union[VacancyLLMResponse, Dict[str, Any]]:
        """Extract structured information from vacancy text using LLM.
        
        Args:
            text_content: Clean text content from vacancy page.
            include_stats: If True, return stats with response.
            
        Returns:
            VacancyLLMResponse or dict with response and stats if include_stats=True.
            
            When include_stats=True, returns dict with:
            - response: VacancyLLMResponse with extracted vacancy data
            - stats: dict with usage (tokens), model, timing, and API metadata
            
        Raises:
            Exception: If LLM extraction fails with wrapped original error.
        """

        start_time = time.time()
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt,
                    },
                    {
                        "role": "user",
                        "content": f"""Here is the vacancy text:\n\n{text_content}""",
                    }
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "VacancyLLMResponse",
                        "schema": VacancyLLMResponse.model_json_schema()
                    }
                },
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=30
            )

            if not response or not response.choices:
                raise ValueError("Empty response from LLM API")
            
            if len(response.choices) == 0:
                raise ValueError("No choices returned from LLM API")
            
            message_content = response.choices[0].message.content
            if not message_content or message_content.strip() == "":
                raise ValueError("Empty message content from LLM API")

            try:
                parsed_content = json.loads(message_content)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON response from LLM: {str(e)}")

            vacancy_llm_response = VacancyLLMResponse.model_validate(parsed_content)

            if include_stats:
                end_time = time.time()
                execution_time = end_time - start_time
                
                stats = {
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
                        "completion_tokens": response.usage.completion_tokens if response.usage else None,
                        "total_tokens": response.usage.total_tokens if response.usage else None
                    },
                    "timing": {
                        "execution_time_seconds": round(execution_time, 3),
                        "start_time": start_time,
                        "end_time": end_time
                    },
                    "model": response.model,
                    "created": response.created,
                    "id": response.id,
                    "system_fingerprint": getattr(response, 'system_fingerprint', None)
                }
                return {
                    "response": vacancy_llm_response,
                    "stats": stats
                }

            return vacancy_llm_response
        
        except ValidationError as e:
            raise LLMValidationError(f"LLM response validation failed: {str(e)}")
        
        except RateLimitError as e:
            raise LLMRateLimitError(f"LLM rate limit exceeded - please wait before retrying: {str(e)}")
        
        except APITimeoutError as e:
            raise LLMClientError(f"LLM request timed out: {str(e)}")
        
        except APIConnectionError as e:
            raise LLMClientError(f"LLM API connection failed: {str(e)}")
        
        except ValueError as e:
            raise LLMValidationError(f"LLM response validation failed: {str(e)}")
        
        except json.JSONDecodeError as e:
            raise LLMValidationError(f"LLM returned invalid JSON: {str(e)}")
        
        except Exception as e:
            error_type = type(e).__name__
            raise LLMClientError(f"LLM extraction failed ({error_type}): {str(e)}")