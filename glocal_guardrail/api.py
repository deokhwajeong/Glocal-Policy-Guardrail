"""
FastAPI interface for CI/CD pipeline integration
"""
import os
import logging
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional
from .governance import GovernanceEngine
from . import __version__

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Glocal Policy Guardrail API",
    description="Automated Policy-as-Code engine for Smart TV/OTT platforms",
    version=__version__
)

# Initialize governance engine
governance = GovernanceEngine()


class ContentMetadata(BaseModel):
    """Content/App metadata model"""
    title: str = Field(..., description="Content/app title")
    description: str = Field(default="", description="Content description")
    content_rating: Optional[str] = Field(default=None, description="Content rating (e.g., PG, FSK_12)")
    minimum_age: int = Field(default=0, description="Minimum age requirement")
    tags: List[str] = Field(default_factory=list, description="Content tags")
    keywords: List[str] = Field(default_factory=list, description="Content keywords")
    features: List[str] = Field(default_factory=list, description="App features")
    ad_duration_minutes: int = Field(default=0, description="Ad duration in minutes")
    ad_schedule: List[str] = Field(default_factory=list, description="Ad schedule times (HH:MM format)")
    youth_access_times: List[str] = Field(default_factory=list, description="Youth access times (HH:MM format)")
    local_content_percentage: int = Field(default=0, description="Percentage of local content")
    real_name_verification_enabled: bool = Field(default=False, description="Real name verification enabled")
    gdpr_compliant: bool = Field(default=False, description="GDPR compliant")
    data_stored_locally: bool = Field(default=False, description="Data stored locally")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "My Streaming App",
                "description": "A family-friendly streaming service",
                "content_rating": "PG",
                "minimum_age": 7,
                "tags": ["family", "entertainment"],
                "keywords": ["streaming", "video"],
                "features": ["parental_controls", "gdpr_compliance"],
                "ad_duration_minutes": 2,
                "ad_schedule": ["10:00", "14:00"],
                "local_content_percentage": 25,
                "gdpr_compliant": True
            }
        }
    )


class ValidationRequest(BaseModel):
    """Validation request model"""
    metadata: Dict[str, Any] = Field(..., description="Content/app metadata")
    target_countries: List[str] = Field(..., description="List of target country codes (e.g., ['SA', 'KR', 'DE'])")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "metadata": {
                    "title": "My Streaming App",
                    "description": "Entertainment platform",
                    "features": ["parental_controls", "gdpr_compliance"],
                    "gdpr_compliant": True
                },
                "target_countries": ["DE", "KR"]
            }
        }
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Glocal Policy Guardrail",
        "version": __version__,
        "description": "Automated Policy-as-Code engine for Smart TV/OTT platforms"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": __version__}


@app.get("/policies")
async def list_policies():
    """List available policy configurations"""
    available_policies = governance.policy_loader.list_available_policies()
    return {
        "available_countries": available_policies,
        "count": len(available_policies)
    }


@app.post("/validate")
async def validate_content(request: ValidationRequest):
    """
    Validate content/app metadata against specified country policies
    
    Returns PASS or REJECT status with detailed violation information
    """
    try:
        results = governance.check_compliance(
            request.metadata,
            request.target_countries
        )
        
        return {
            "results": {
                country: result.to_dict()
                for country, result in results.items()
            }
        }
    except Exception as e:
        logger.error(f"Validation error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during validation. Please check your request and try again."
        )


@app.post("/validate/{country_code}")
async def validate_single_country(country_code: str, metadata: Dict[str, Any]):
    """
    Validate content/app metadata against a single country policy
    
    Args:
        country_code: ISO country code (SA, KR, DE)
        metadata: Content/app metadata
    """
    country_code = country_code.upper()
    
    if country_code not in governance.policy_loader.list_available_policies():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy not found for country code: {country_code}"
        )
    
    try:
        result = governance.check_single_country(metadata, country_code)
        return result.to_dict()
    except Exception as e:
        logger.error(f"Validation error for country {country_code}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during validation. Please check your request and try again."
        )


@app.post("/deployment-check")
async def deployment_readiness_check(request: ValidationRequest):
    """
    Comprehensive pre-deployment readiness check
    
    Returns overall deployment status and per-country compliance results
    """
    try:
        report = governance.get_deployment_readiness(
            request.metadata,
            request.target_countries
        )
        return report
    except Exception as e:
        logger.error(f"Deployment check error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during deployment check. Please check your request and try again."
        )


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment variables with safe defaults
    host = os.getenv("GUARDRAIL_HOST", "127.0.0.1")
    port = int(os.getenv("GUARDRAIL_PORT", "8000"))
    
    logger.info(f"Starting Glocal Policy Guardrail API on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
