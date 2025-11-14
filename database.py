"""
Database connection and utilities for AgriFlow
Supports PostgreSQL and SQLite for development
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./agriflow.db"  # Default to SQLite for development
)

# SQLAlchemy engine
try:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info(f"Database connected: {DATABASE_URL}")
except Exception as e:
    logger.error(f"Database connection failed: {e}")
    raise

# Database dependency
def get_db():
    """Get database session for FastAPI dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ORM Models
class Farmer(Base):
    """Farmer profile model"""
    __tablename__ = "farmers"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    district = Column(String)
    land_size_ha = Column(Float)
    soil_health = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Assessment(Base):
    """Credit risk assessment model"""
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(String, index=True)
    dcs_score = Column(Float)  # Digital Credit Score (0-100)
    ndvi_score = Column(Float)  # Vegetation health (0-100)
    risk_level = Column(String)  # LOW, MEDIUM, HIGH
    recommended_amount = Column(Float)  # In INR
    assessment_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class Transaction(Base):
    """Transaction/Payout model"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(String, index=True)
    upi_id = Column(String)
    amount = Column(Float)  # In INR
    status = Column(String)  # PENDING, SUCCESS, FAILED
    razorpay_id = Column(String, nullable=True)
    triggered_by = Column(String)  # MANDI_SALE, MANUAL, SCHEDULER
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WhatsAppLog(Base):
    """WhatsApp interaction log"""
    __tablename__ = "whatsapp_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, index=True)
    message_in = Column(String)
    message_out = Column(String)
    interaction_type = Column(String)  # QUERY, ASSESSMENT, PAYMENT
    created_at = Column(DateTime, default=datetime.utcnow)

# Create all tables
def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

if __name__ == "__main__":
    init_db()
