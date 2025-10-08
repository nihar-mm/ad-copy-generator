from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from contextlib import contextmanager
from app.config import settings
import logging
import time

logger = logging.getLogger(__name__)

# Production-ready database configuration
def get_database_url():
    """Get database URL with proper connection pooling for production"""
    db_url = settings.DATABASE_URL
    
    # For SQLite (development)
    if db_url.startswith("sqlite"):
        return db_url
    
    # For PostgreSQL (production)
    if db_url.startswith("postgresql"):
        # Add connection pooling parameters
        if "?" not in db_url:
            db_url += "?"
        else:
            db_url += "&"
        
        # Production connection pool settings
        pool_params = [
            "pool_size=20",           # Number of connections to maintain
            "max_overflow=30",        # Additional connections beyond pool_size
            "pool_pre_ping=True",     # Validate connections before use
            "pool_recycle=3600",      # Recycle connections after 1 hour
            "pool_timeout=30"         # Timeout for getting connection from pool
        ]
        
        db_url += "&".join(pool_params)
        logger.info("Using PostgreSQL with connection pooling")
    
    return db_url

# Create engines
engine = create_engine(get_database_url(), pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async engine for async operations (future use)
async_engine = None
AsyncSessionLocal = None

if settings.DATABASE_URL.startswith("postgresql"):
    async_db_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    async_engine = create_async_engine(async_db_url, pool_pre_ping=True, echo=False)
    AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    """Dependency to get async database session"""
    if AsyncSessionLocal is None:
        raise RuntimeError("Async database not configured")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def check_database_health() -> dict:
    """Check database health and connectivity"""
    start_time = time.time()
    result = {
        "healthy": False,
        "response_time_ms": 0,
        "error": None,
        "database_type": "sqlite" if settings.DATABASE_URL.startswith("sqlite") else "postgresql"
    }
    
    try:
        db = SessionLocal()
        try:
            # Simple query to test connectivity
            db.execute(text("SELECT 1"))
            db.commit()
            result["healthy"] = True
            logger.info("Database health check passed")
        finally:
            db.close()
    except OperationalError as e:
        result["error"] = f"Database connection failed: {str(e)}"
        logger.error(result["error"])
    except SQLAlchemyError as e:
        result["error"] = f"Database error: {str(e)}"
        logger.error(result["error"])
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
        logger.error(result["error"])
    finally:
        result["response_time_ms"] = round((time.time() - start_time) * 1000, 2)
    
    return result


@contextmanager
def get_db_context():
    """Context manager for database sessions with automatic cleanup"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database transaction failed: {e}")
        raise
    finally:
        db.close()


def retry_on_db_error(func, max_retries=3, delay=1):
    """Retry decorator for database operations"""
    def wrapper(*args, **kwargs):
        retries = 0
        while retries < max_retries:
            try:
                return func(*args, **kwargs)
            except OperationalError as e:
                retries += 1
                if retries >= max_retries:
                    logger.error(f"Database operation failed after {max_retries} retries: {e}")
                    raise
                logger.warning(f"Database operation failed, retry {retries}/{max_retries}: {e}")
                time.sleep(delay * retries)  # Exponential backoff
            except Exception as e:
                logger.error(f"Non-retryable database error: {e}")
                raise
    return wrapper


def get_database_stats() -> dict:
    """Get database connection pool statistics"""
    stats = {
        "pool_size": engine.pool.size(),
        "checked_in_connections": engine.pool.checkedin(),
        "checked_out_connections": engine.pool.checkedout(),
        "overflow_connections": engine.pool.overflow(),
        "total_connections": engine.pool.size() + engine.pool.overflow()
    }
    return stats
