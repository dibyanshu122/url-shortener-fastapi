from sqlalchemy import Column, Integer, String
from database import Base

class URL(Base):
    # Name of the table in the database
    __tablename__ = "urls"

    # Unique identifier for each record
    id = Column(Integer, primary_key=True, index=True)
    
    # The original long URL provided by the user
    original_url = Column(String, nullable=False) 
    
    # The unique short code assigned to the URL (e.g., 'abc123')
    short_code = Column(String, unique=True, index=True) 
    
    # Counter to track how many times the short link has been clicked
    clicks = Column(Integer, default=0)