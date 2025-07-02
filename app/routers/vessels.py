from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import deps
from app.services.vessel_check import check_vessel_documents

router = APIRouter(prefix='/vessels', tags=['vessels'])


@router.get('/{vessel_id}/check')
def check_vessel(vessel_id: int, db: Session = Depends(deps.get_db)):
    try:
        return check_vessel_documents(db, vessel_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
