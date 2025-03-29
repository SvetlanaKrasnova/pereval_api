from typing import List

from fastapi import APIRouter, Query, status
from starlette.responses import JSONResponse

from src.db_dependency import db_dependency
from src.exceptions import IncorrectPerevalStatus, PerevalNotFoundError, PerevalUpdateError, UserNotFoundByEmailError
from src.models import StatusEnum
from src.schemas import PerevalAddSchema, PerevalReplaceSchema, PerevalShowSchema
from src.services.pereval import Pereval

pereval_router = APIRouter(prefix='/submitData', tags=['perevals'])
db = Pereval()


@pereval_router.post('/')
async def add_pereval(pereval: PerevalAddSchema, session: db_dependency) -> JSONResponse:
    pereval_id = await db.add_pereval(pereval=pereval, session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'status': status.HTTP_200_OK,
            'id': pereval_id,
            'message': None,
        },
    )


@pereval_router.get('/{pereval_id}')
async def get_pereval_by_id(pereval_id: int, session: db_dependency) -> PerevalShowSchema:
    if not (db_pereval := await db.get_pereval_by_id(pereval_id, session)):
        raise PerevalNotFoundError(pereval_id)
    return await db.get_info_pereval(db_pereval, session)


@pereval_router.get('/')
async def get_perevals_by_user_email(
    session: db_dependency,
    user__email: str = Query(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
) -> List[PerevalShowSchema]:
    if not (user := await db.get_user_by_email(user__email, session)):
        raise UserNotFoundByEmailError(user__email)
    return await db.get_perevals_by_user_id(user.id, session)


@pereval_router.patch('/{pereval_id}')
async def update_pereval_by_id(
    pereval_id: int,
    data_to_update: PerevalReplaceSchema,
    session: db_dependency,
) -> JSONResponse:
    try:
        if not (db_pereval := await db.get_pereval_by_id(pereval_id, session)):
            raise PerevalNotFoundError(pereval_id)

        if db_pereval.status.value != StatusEnum.new.value:
            raise IncorrectPerevalStatus(db_pereval.status.value)
        await db.update_pereval(db_pereval, data_to_update, session)
    except (PerevalNotFoundError, PerevalUpdateError, IncorrectPerevalStatus) as e:
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
