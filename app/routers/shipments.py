# =============================================================================
# import shutil
# import uuid
# from pathlib import Path
# from fastapi import BackgroundTasks
# =============================================================================

from fastapi import (APIRouter, Depends, File, HTTPException, Request,
                     UploadFile, status)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud, deps, schemas
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


# =============================================================================
# @router.post('/push', response_class=HTMLResponse)
# async def push_shipment(
#     request: Request,
#     background_tasks: BackgroundTasks,
#     file: UploadFile = File(...),
# ):
#     if not file:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='No file provided'
#         )
# 
#     temp_dir = Path('tmp/uploads')
#     temp_dir.mkdir(parents=True, exist_ok=True)
#     temp_file_path = temp_dir / f'{uuid.uuid4()}.xlsx'
# 
#     with temp_file_path.open('wb') as buffer:
#         shutil.copyfileobj(file.file, buffer)
# 
#     from app.tasks import process_shipment_task
#     process_shipment_task.delay(str(temp_file_path))
# 
#     return templates.TemplateResponse(
#         'shipment_result.html',
#         {
#             'request': request,
#             'message': (
#                 'Shipment processing started. '
#                 "You will be notified when it's done."
#             )
#         }
#     )
# =============================================================================


@router.get('/{shipment_id}', response_model=schemas.ShipmentRead)
def read_shipment_with_totals(
    shipment_id: int,
    db: Session = Depends(deps.get_db)
):
    result = crud.get_shipment_with_totals(db, shipment_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Shipment not found'
        )
    return result
