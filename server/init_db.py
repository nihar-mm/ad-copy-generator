#!/usr/bin/env python3
"""
Database initialization script
Creates tables and initializes the database
"""

import os
import sys
from pathlib import Path

# Add the server directory to Python path
server_dir = Path(__file__).parent
sys.path.insert(0, str(server_dir))

from app.db.session import engine
from app.db.models import Base
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize the database with all tables"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
        
        # Create local storage directory
        storage_dir = Path(settings.LOCAL_STORAGE_DIR)
        storage_dir.mkdir(exist_ok=True)
        logger.info(f"✅ Storage directory created: {storage_dir}")
        
        # Create uploads directory
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)
        logger.info(f"✅ Uploads directory created: {uploads_dir}")
        
        logger.info("🎉 Database initialization completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)

