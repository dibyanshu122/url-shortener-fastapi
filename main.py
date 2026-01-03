from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import RedirectResponse
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from starlette import status
import models, database, utils, schemas

app = FastAPI(title="Secure URL Shortener API")

# Initialize database tables
models.Base.metadata.create_all(bind=database.engine)

# --- SECURITY CONFIGURATION ---
API_KEY = "my_secret_token_123"
api_key_header = APIKeyHeader(name="X-API-KEY")

def validate_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Missing API Key"
        )
    return api_key

# --- DATABASE CONNECTION DEPENDENCY ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API ENDPOINTS ---

# 1. Create a Short URL (Protected by API Key)
@app.post("/shorten/", response_model=schemas.URLResponse)
def shorten_url(
    url_data: schemas.URLCreate, 
    db: Session = Depends(get_db), 
    current_api_key: str = Depends(validate_api_key)
):
    # Logic to handle Custom Short Codes
    if url_data.custom_code:
        # Check if the custom code is already taken in the database
        existing = db.query(models.URL).filter(models.URL.short_code == url_data.custom_code).first()
        if existing:
            raise HTTPException(status_code=400, detail="Custom code already taken!")
        code = url_data.custom_code
    else:
        # Generate a random 6-character short code
        code = utils.generate_short_code()
    
    # Create and save the new URL record
    new_url = models.URL(original_url=str(url_data.original_url), short_code=code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    
    # Construct the full short URL for the response
    new_url.short_url = f"http://localhost:8000/{code}"
    return new_url

# 2. Analytics Endpoint: Retrieve click statistics for a short code
@app.get("/stats/{short_code}")
def get_stats(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return {
        "original_url": db_url.original_url,
        "clicks": db_url.clicks
    }

# 3. Redirection Endpoint: Redirect short code to the original URL
@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    # Look up the short code in the database
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Increment the click counter
    db_url.clicks += 1
    db.commit()
    
    # Redirect the user's browser to the destination website
    return RedirectResponse(url=db_url.original_url)