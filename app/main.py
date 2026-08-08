from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import auth, products

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