from fastapi import FastAPI

from app.routers import coverage, documents, merge, policies, vessels

from .database import Base, engine

app = FastAPI(title='Cargo Seal – Marine Insurance Tracker')

Base.metadata.create_all(bind=engine)

# Register all routers
app.include_router(coverage.router, prefix='/api')
app.include_router(documents.router, prefix='/api')
app.include_router(merge.router, prefix='/api')
app.include_router(policies.router, prefix='/api')
app.include_router(vessels.router, prefix='/api')
