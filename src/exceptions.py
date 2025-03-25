from starlette import status
from starlette.exceptions import HTTPException


class PerevalNotFoundError(HTTPException):
    def __init__(self, pereval_id: int):
        super(PerevalNotFoundError, self).__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Pereval not found by id = "{pereval_id}"',
        )


class PerevalUpdateError(HTTPException):
    def __init__(self, ex):
        super(PerevalUpdateError, self).__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex),
        )


class UserNotFoundByEmailError(HTTPException):
    def __init__(self, user_email: str):
        super(UserNotFoundByEmailError, self).__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User not found by email = "{user_email}"',
        )
