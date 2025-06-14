from fastapi import FastAPI

from app.routers import coverage, documents, merge, policies, vessels

from .database import Base, engine

app = FastAPI(title='Marine Cargo API')

Base.metadata.create_all(bind=engine)

# Register all routers
app.include_router(coverage.router)
app.include_router(documents.router)
app.include_router(merge.router)
app.include_router(policies.router)
app.include_router(vessels.router)

# Run via: uvicorn app.main:app --reload
