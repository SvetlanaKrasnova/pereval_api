from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from src.db_dependency import db_dependency
from src.schemas import PerevalPostSchema
from src.services.pereval import Pereval

pereval_router = APIRouter(tags=['perevals'])


@pereval_router.post('/submitData')
async def submit_data(pereval: PerevalPostSchema, session: db_dependency):
    pereval_db = await Pereval().add_pereval(pereval=pereval, session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'status': status.HTTP_200_OK,
            'id': pereval_db.id,
            'message': None,
        },
    )
