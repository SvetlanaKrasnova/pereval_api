import pytest
from sqlalchemy.ext.asyncio import AsyncSession

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
async def test_add_pereval(dbsession: AsyncSession, pereval_request: PerevalSchema):
    pereval_id = await db.add_pereval(pereval=pereval_request, session=dbsession)
    result = await db.get_pereval_by_id(pereval_id, dbsession)
    assert result is not None


@pytest.mark.parametrize(
    argnames=('add_data', 'update_data'),
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
async def test_update_pereval(dbsession: AsyncSession, add_data, update_data):
    pereval_id = await db.add_pereval(pereval=add_data, session=dbsession)
    db_pereval = await db.get_pereval_by_id(pereval_id, dbsession)
    await db.update_pereval(db_pereval, update_data, dbsession)
    new_pereval = await db.get_pereval_by_id(pereval_id, dbsession)
    new_images = await db._get_images_by_pereval_id(new_pereval.id, dbsession)

    assert update_data.title == new_pereval.title
    if update_data.images:
        assert len(update_data.images) == len(new_images)
    else:
        assert len(new_images) == 0


@pytest.mark.parametrize(
    argnames=('add_data',),
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
async def test_get_info_pereval(dbsession: AsyncSession, add_data: PerevalSchema):
    pereval_id = await db.add_pereval(pereval=add_data, session=dbsession)
    info_pereval = await db.get_info_pereval_by_id(pereval_id, dbsession)
    assert add_data.title == info_pereval.title
    assert add_data.user.email == info_pereval.user.email
    assert add_data.coords.height == info_pereval.coords.height
    assert add_data.level.summer == info_pereval.level.summer
    assert len(add_data.images) == len(info_pereval.images)
    if add_data.images:
        add_data_title_images = ''.join([image.title for image in add_data.images])
        info_pereval_title_images = ''.join([image.title for image in info_pereval.images])
        assert add_data_title_images == info_pereval_title_images
