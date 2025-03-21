import logging.handlers

import uvicorn
from fastapi import HTTPException, Request, status
from starlette.responses import JSONResponse

from src.app import app
from src.core.config import uvicorn_options

logger = logging.getLogger('pereval')


@app.middleware('http')
async def error_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as exc:
        logger.exception(exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'status': exc.status_code,
                'message': exc.detail,
                'id': None,
            },
        )
    except Exception as e:
        logger.exception(f'{request.url} | Error in application: {e}')
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e),
                'id': None,
            },
        )


if __name__ == '__main__':
    logger.info(uvicorn_options)
    uvicorn.run(
        'main:app',
        **uvicorn_options,
    )
