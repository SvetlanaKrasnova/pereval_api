from typing import List, Optional

from fastapi import APIRouter, Query, status
from starlette.responses import JSONResponse

from src.db_dependency import db_dependency
from src.exceptions import PerevalNotFoundError, PerevalUpdateError, UserNotFoundByEmailError
from src.models import PerevalAdded, StatusEnum
from src.schemas import PerevalReplaceSchema, PerevalSchema
from src.services.pereval import Pereval

pereval_router = APIRouter(prefix='/submitData', tags=['perevals'])
db = Pereval()


@pereval_router.post('/')
async def submit_data(pereval: PerevalSchema, session: db_dependency) -> JSONResponse:
    pereval_id = await db.add_pereval(pereval=pereval, session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'status': status.HTTP_200_OK,
            'id': pereval_id,
            'message': None,
        },
    )


@pereval_router.get('/{id}')
async def get_pereval(pereval_id: int, session: db_dependency) -> PerevalSchema:
    if pereval := await db.get_info_pereval_by_id(pereval_id, session):
        return pereval
    raise PerevalNotFoundError(pereval_id)


@pereval_router.get('/')
async def get_perevals_by_user_email(
    user__email: Query(pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'),
    session: db_dependency,
) -> Optional[List[PerevalAdded]]:
    if not (user := await db.get_user_by_email(user__email, session)):
        raise UserNotFoundByEmailError(user__email)
    return await db.get_perevals_by_user_id(user.id, session)


@pereval_router.patch('/{id}')
async def update_pereval(pereval_id: int, pereval: PerevalReplaceSchema, session: db_dependency) -> JSONResponse:
    try:
        if not (db_pereval := await db.get_pereval_by_id(pereval_id, session)):
            raise PerevalNotFoundError(pereval_id)

        if await db_pereval.status != StatusEnum.new:
            await db.update_pereval(db_pereval, pereval, session)
    except (PerevalNotFoundError, PerevalUpdateError) as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                'state': 0,
                'message': e.detail,
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'state': 0,
                'message': str(e),
            },
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'state': 1,
            'message': None,
        },
    )
