from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.metrics import setup_metrics
from app.core.logging import setup_logging, CorrelationIdMiddleware
from app.api.v1.endpoints import auth, products, orders

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

@app.get("/health", status_code=200)
def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

@app.get("/health", status_code=200)
def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(products.router, prefix=f"{settings.API_V1_STR}/products", tags=["products"])

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

@app.get("/health", status_code=200)
def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(products.router, prefix=f"{settings.API_V1_STR}/products", tags=["products"])
app.include_router(orders.router, prefix=f"{settings.API_V1_STR}/orders", tags=["orders"])


limiter = Limiter(key_func=get_remote_address, storage_uri=settings.REDIS_URL)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Initialize structured logging and correlation ID middleware
setup_logging()
app.add_middleware(CorrelationIdMiddleware)

# Initialize Prometheus instrumentation
setup_metrics(app)

@app.get("/health", status_code=200)
@limiter.limit("60/minute")
def health_check(request: Request):
    return {"status": "healthy", "service": settings.PROJECT_NAME}

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(products.router, prefix=f"{settings.API_V1_STR}/products", tags=["products"])
app.include_router(orders.router, prefix=f"{settings.API_V1_STR}/orders", tags=["orders"])