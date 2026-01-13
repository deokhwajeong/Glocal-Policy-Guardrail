"""FastAPI server for CI/CD integration of Policy Guardrail."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from guardrail.rule_engine import RuleEngine, ValidationStatus


app = FastAPI(
    title="Glocal Policy Guardrail API",
    description="Policy-as-Code engine for Smart TV/OTT content compliance",
    version="0.1.0"
)


class ContentMetadata(BaseModel):
    """Content metadata for validation."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Example Movie",
                "description": "An exciting adventure film",
                "categories": ["action", "adventure"],
                "tags": ["family-friendly", "international"],
                "rating": "PG13",
                "duration_minutes": 120,
                "subtitle_languages": ["en", "ko", "ar"],
                "audio_languages": ["en", "ko"],
                "ad_breaks": [
                    {"timestamp_seconds": 600, "duration_seconds": 30},
                    {"timestamp_seconds": 1800, "duration_seconds": 45}
                ]
            }
        }
    )
    
    title: str = Field(..., description="Content title")
    description: Optional[str] = Field(None, description="Content description")
    categories: List[str] = Field(default_factory=list, description="Content categories")
    tags: List[str] = Field(default_factory=list, description="Content tags")
    rating: Optional[str] = Field(None, description="Content rating")
    duration_minutes: Optional[int] = Field(None, description="Content duration in minutes")
    subtitle_languages: List[str] = Field(default_factory=list, description="Available subtitle languages")
    audio_languages: List[str] = Field(default_factory=list, description="Available audio languages")
    ad_breaks: List[Dict[str, Any]] = Field(default_factory=list, description="Advertisement break configurations")


class ValidationRequest(BaseModel):
    """Request model for content validation."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "content": {
                    "title": "Example Movie",
                    "description": "An exciting adventure film",
                    "categories": ["action"],
                    "rating": "PG13",
                    "duration_minutes": 120,
                    "subtitle_languages": ["en", "ko"],
                    "audio_languages": ["en"]
                },
                "country": "korea"
            }
        }
    )
    
    content: ContentMetadata = Field(..., description="Content to validate")
    country: str = Field(..., description="Target country code (e.g., 'korea', 'saudi_arabia')")


class ValidationResponse(BaseModel):
    """Response model for validation results."""
    status: str = Field(..., description="Validation status: PASS or REJECT")
    country: str = Field(..., description="Country validated against")
    violations: List[str] = Field(..., description="List of policy violations")
    warnings: List[str] = Field(..., description="List of warnings")
    message: str = Field(..., description="Human-readable message")


# Initialize rule engine
rule_engine = RuleEngine()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Glocal Policy Guardrail",
        "version": "0.1.0",
        "description": "Policy-as-Code engine for Smart TV/OTT content compliance",
        "endpoints": {
            "validate": "/validate",
            "health": "/health",
            "policies": "/policies"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "Glocal Policy Guardrail"
    }


@app.get("/policies")
async def list_policies():
    """List available country policies."""
    policies_dir = Path(__file__).parent.parent / "policies"
    
    if not policies_dir.exists():
        return {"available_policies": [], "count": 0}
    
    policy_files = list(policies_dir.glob("*.yaml"))
    policies = [f.stem for f in policy_files]
    
    return {
        "available_policies": policies,
        "count": len(policies)
    }


@app.post("/validate", response_model=ValidationResponse)
async def validate_content(request: ValidationRequest):
    """
    Validate content against country-specific policies.
    
    Returns PASS or REJECT status based on policy compliance.
    """
    try:
        # Convert content to dict
        content_dict = request.content.model_dump()
        
        # Validate against country policy
        result = rule_engine.validate_content(
            content=content_dict,
            country=request.country
        )
        
        # Generate message
        if result.status == ValidationStatus.PASS:
            message = f"Content approved for deployment in {request.country}"
            if result.warnings:
                message += f" with {len(result.warnings)} warning(s)"
        else:
            message = f"Content rejected for {request.country}: {len(result.violations)} violation(s) found"
        
        return ValidationResponse(
            status=result.status.value,
            country=result.country,
            violations=result.violations,
            warnings=result.warnings,
            message=message
        )
    
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Policy not found: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Validation error: {str(e)}"
        )


@app.post("/validate/batch")
async def validate_content_batch(
    request: ContentMetadata,
    countries: List[str] = Query(...)
):
    """
    Validate content against multiple country policies.
    
    Returns validation results for each country.
    """
    results = {}
    
    for country in countries:
        try:
            result = rule_engine.validate_content(
                content=request.model_dump(),
                country=country
            )
            results[country] = result.to_dict()
        except FileNotFoundError:
            results[country] = {
                "status": "ERROR",
                "error": f"Policy not found for {country}"
            }
        except Exception as e:
            results[country] = {
                "status": "ERROR",
                "error": str(e)
            }
    
    return {
        "results": results,
        "summary": {
            "total": len(countries),
            "passed": sum(1 for r in results.values() if r.get("status") == "PASS"),
            "rejected": sum(1 for r in results.values() if r.get("status") == "REJECT"),
            "errors": sum(1 for r in results.values() if r.get("status") == "ERROR")
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
