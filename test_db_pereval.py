import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import List

from data_for_tests import *
from src.services.pereval import Pereval

pytestmark = pytest.mark.asyncio

db = Pereval()


@pytest.mark.parametrize(
    argnames=('pereval_request',),
    argvalues=[
        (ADD_PEREVAL_WITHOUT_IMAGES,),
        (ADD_PEREVAL_OTHER_USER,),
        (ADD_PEREVAL_WITH_IMAGES,),
    ],
    ids=(
        'add_pereval_without_images',
        'add_pereval_same_user',
        'add_pereval_with_images',
    ),
)
async def test_add_pereval(dbsession: AsyncSession, pereval_request: PerevalAddSchema):
    pereval_id = await db.add_pereval(pereval=pereval_request, session=dbsession)
    pereval = await db.get_pereval_by_id(pereval_id, dbsession)
    assert pereval is not None
    await db._delete_pereval(pereval=pereval, session=dbsession)


@pytest.mark.parametrize(
    argnames=('pereval_request', 'data_to_update'),
    argvalues=[
        (ADD_PEREVAL_WITHOUT_IMAGES, UPDATE_PEREVAL_WITHOUT_IMAGES),
        (ADD_PEREVAL_WITH_IMAGES, UPDATE_PEREVAL_WITH_IMAGES),
        (ADD_PEREVAL_WITHOUT_IMAGES, UPDATE_PEREVAL_WITH_IMAGES),
        (ADD_PEREVAL_WITH_IMAGES, UPDATE_PEREVAL_WITHOUT_IMAGES),
    ],
    ids=(
        'update_pereval_without_images',
        'update_pereval_other_images',
        'update_pereval_add_images',
        'update_pereval_delete_images',
    ),
)
async def test_update_pereval(
    dbsession: AsyncSession,
    pereval_request: PerevalAddSchema,
    data_to_update: PerevalReplaceSchema,
):
    pereval_id = await db.add_pereval(pereval=pereval_request, session=dbsession)
    db_pereval = await db.get_pereval_by_id(pereval_id, dbsession)
    await db.update_pereval(db_pereval, data_to_update, dbsession)
    new_pereval = await db.get_pereval_by_id(pereval_id, dbsession)
    new_images = await db._get_images_by_pereval_id(new_pereval.id, dbsession)

    assert data_to_update.title == new_pereval.title
    if data_to_update.images:
        assert len(data_to_update.images) == len(new_images)
    else:
        assert len(new_images) == 0
    await db._delete_pereval(pereval=db_pereval, session=dbsession)


@pytest.mark.parametrize(
    argnames=('pereval_request',),
    argvalues=[
        (ADD_PEREVAL_WITHOUT_IMAGES,),
        (ADD_PEREVAL_WITH_IMAGES,),
        (ADD_PEREVAL_OTHER_USER,),
    ],
    ids=(
        'get_info_pereval_without_images',
        'get_info_pereval_with_images',
        'get_info_pereval_other_user',
    ),
)
async def test_get_info_pereval(dbsession: AsyncSession, pereval_request: PerevalAddSchema):
    pereval_id = await db.add_pereval(pereval=pereval_request, session=dbsession)
    pereval = await db.get_pereval_by_id(pereval_id, dbsession)
    info_pereval = await db.get_info_pereval(pereval, dbsession)
    assert pereval_request.title == info_pereval.title
    assert pereval_request.user.email == info_pereval.user.email
    assert pereval_request.coords.height == info_pereval.coords.height
    assert pereval_request.level.summer == info_pereval.level.summer
    assert len(pereval_request.images) == len(info_pereval.images)
    if pereval_request.images:
        add_data_title_images = ''.join([image.title for image in pereval_request.images])
        info_pereval_title_images = ''.join([image.title for image in info_pereval.images])
        assert add_data_title_images == info_pereval_title_images
    await db._delete_pereval(pereval=pereval, session=dbsession)


@pytest.mark.parametrize(
    argnames=('input_data_perevals', 'user_object', 'col_user_perevals'),
    argvalues=[
        ([ADD_PEREVAL_WITHOUT_IMAGES, ADD_PEREVAL_OTHER_USER], OTHER_USER, 1),
        ([ADD_PEREVAL_WITH_IMAGES, ADD_PEREVAL_WITH_IMAGES], USER_CAT, 0),
        ([ADD_PEREVAL_OTHER_USER, ADD_PEREVAL_OTHER_USER], OTHER_USER, 3),
        ([ADD_PEREVAL_CAT_USER], USER_CAT, 1),
    ],
    ids=(
        'get_user_perevals_other_user_one_found',
        'get_user_perevals_cat_user_not_found',
        'get_user_perevals_other_user_all_found',
        'get_user_perevals_cat_user_one_found',
    ),
)
async def test_get_perevals_by_user_id(
    dbsession: AsyncSession,
    input_data_perevals: List,
    user_object: UserSchema,
    col_user_perevals: int,
):
    await db._add_user(user=user_object, session=dbsession)
    for pereval in input_data_perevals:
        await db.add_pereval(pereval=pereval, session=dbsession)
    user = await db.get_user_by_email(user_object.email, dbsession)
    user_perevals = await db.get_perevals_by_user_id(user.id, dbsession)
    assert len(user_perevals) == col_user_perevals
