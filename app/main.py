from fastapi import FastAPI

from app.routers import (coverage, documents, merge, policies, shipments,
                         vessels)

from .database import Base, engine

PREFIX = '/api'

app = FastAPI(title='Cargo Seal – Marine Insurance Tracker')

Base.metadata.create_all(bind=engine)

app.include_router(coverage.router, prefix=PREFIX)
app.include_router(documents.router, prefix=PREFIX)
app.include_router(merge.router, prefix=PREFIX)
app.include_router(policies.router, prefix=PREFIX)
app.include_router(shipments.router, prefix=PREFIX)
app.include_router(vessels.router, prefix=PREFIX)
