from fastapi import (APIRouter, Depends, File, HTTPException, Request,
                     UploadFile, status)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import deps
from app.services import declaration as declaration_service

router = APIRouter(prefix='/shipments', tags=['shipments'])

templates = Jinja2Templates(directory='templates')


@router.post('/push', response_class=HTMLResponse)
async def push_shipment(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db)
):
    """
    Push Declaration to Database Handler (HTML view)
    """
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No file provided'
        )

    sheet_names, operator, vessel = declaration_service.process_declaration_file(
        file, db
    )

    return templates.TemplateResponse(
        'shipment_result.html',
        {
            'request': request,
            'sheet_names': sheet_names,
            'operator': operator,
            'vessel': vessel
        }
    )
