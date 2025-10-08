try:
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.middleware.trustedhost import TrustedHostMiddleware
    from fastapi.staticfiles import StaticFiles
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Please run: pip install -r requirements.txt")
    exit(1)
from app.config import settings
from app.pipeline.context.manager import ContextManager
from app.routes import health, jobs, admin, auth
from app.db.session import engine
from app.db.models import Base
from app.middleware.error_handler import setup_error_handlers, log_request_exceptions
from app.exceptions import raise_internal_error
from app.auth import add_security_headers
import logging, os, time

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Rate limiting (only if not using inline mode)
if settings.QUEUE_MODE != "inline":
    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri=settings.REDIS_URL
    )
else:
    # Simple in-memory rate limiting for inline mode
    limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Ad Copy Regenerator", 
    version="1.0", 
    root_path="",
    docs_url="/docs" if settings.APP_ENV == "dev" else None,
    redoc_url="/redoc" if settings.APP_ENV == "dev" else None
)

# Setup error handlers
setup_error_handlers(app)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Trusted hosts (production security)
if settings.APP_ENV == "prod":
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["localhost", "127.0.0.1", "yourdomain.com"]  # Configure with your actual domains
    )

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve local uploads when using local storage
if settings.STORAGE_BACKEND == "local":
    os.makedirs(settings.LOCAL_STORAGE_DIR, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=settings.LOCAL_STORAGE_DIR), name="uploads")

# Include routers (under /api for frontend proxy)
api = FastAPI()
api.include_router(auth.router, prefix="/auth", tags=["authentication"])
api.include_router(health.router, prefix="/health", tags=["health"])
api.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api.include_router(admin.router, tags=["admin"])
app.mount("/api", api)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    logging.info(f"Ad Copy Regenerator started in {settings.APP_ENV} mode")
    
    # Create local storage directory if using local storage
    if settings.STORAGE_BACKEND == "local":
        os.makedirs(settings.LOCAL_STORAGE_DIR, exist_ok=True)
        logging.info(f"Local storage directory created: {settings.LOCAL_STORAGE_DIR}")
    
    # Preload context store
    try:
        if settings.CONTEXT_PRELOAD_ON_STARTUP:
            app.state.context_manager = ContextManager(
                data_dir=settings.CONTEXT_DATA_DIR,
                persist_dir=settings.CHROMA_PERSIST_DIR,
                embedding_model=settings.EMBEDDING_MODEL
            )
            app.state.context_manager.load_or_ingest()
            logging.info("Context store ready")
    except Exception as e:
        logging.exception(f"Failed to preload context: {e}")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for monitoring with error handling and security headers"""
    start_time = time.time()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"{request.method} {request.url.path}")
        response = await call_next(request)
        
        # Add security headers
        response = add_security_headers(response)
        
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - {response.status_code} ({process_time:.3f}s)")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"{request.method} {request.url.path} - ERROR after {process_time:.3f}s: {str(e)}")
        raise
