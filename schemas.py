from pydantic import BaseModel, HttpUrl
from typing import Optional

# Schema for the input data required to create a new short URL
class URLCreate(BaseModel):
    # Validates that the input is a proper URL starting with http or https
    original_url: HttpUrl  
    
    # Optional custom alias for the short link
    custom_code: Optional[str] = None 

# Schema for the data returned in the API response
class URLResponse(BaseModel):
    short_url: str
    original_url: str
    short_code: str
    clicks: int

    # Allows Pydantic to read data directly from SQLAlchemy models
    class Config:
        from_attributes = True