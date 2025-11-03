"""
Template: FastAPI Endpoint
Usage: Copy pattern for new endpoints

Replace:
- ENDPOINT_NAME: Function name (e.g., create_webhook)
- PATH: URL path (e.g., /webhooks)
- METHOD: HTTP method (get, post, put, delete)
- RequestModel: Pydantic request model
- ResponseData: Response data type
"""

from typing import Dict, Any
from datetime import datetime, timezone
from fastapi import HTTPException
from pydantic import BaseModel, Field, ValidationError
import logging

logger = logging.getLogger(__name__)


class RequestModel(BaseModel):
    """Request validation model."""

    field1: str = Field(..., max_length=100, description="Field description")
    field2: int = Field(..., gt=0, description="Field description")


@app.METHOD("/PATH")
async def ENDPOINT_NAME(
    request: RequestModel,
    # Add dependencies here (e.g., current_user: User = Depends(get_current_user))
) -> Dict[str, Any]:
    """
    ENDPOINT_NAME description.

    Args:
        request: Request data

    Returns:
        Standardized response with status, data, message, timestamp

    Raises:
        HTTPException: 400 for validation errors, 500 for server errors
    """
    try:
        logger.info("Processing ENDPOINT_NAME request")

        # TODO: Implement business logic here
        result = await some_service.process(request)

        return {
            "status": "success",
            "data": result,
            "message": "Operation completed successfully",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"ENDPOINT_NAME error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
