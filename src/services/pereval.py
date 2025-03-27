import logging
from datetime import datetime
from typing import List, Optional, Sequence, Tuple

from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, select, update

from src import db_dependency
from src.exceptions import PerevalUpdateError
from src.models import Coord, Image, Level, PerevalAdded, User
from src.schemas import (
    CoordsSchema,
    ImageSchema,
    LevelSchema,
    PerevalAddSchema,
    PerevalReplaceSchema,
    PerevalShowSchema,
    UserSchema,
)


class Pereval:
    def __init__(self):
        self.logger = logging.getLogger('pereval')

    async def get_perevals_by_user_id(self, user_id: int, session: db_dependency) -> List[PerevalShowSchema]:
        _perevals = await session.execute(select(PerevalAdded).where(PerevalAdded.user_id == user_id))
        perevals = _perevals.scalars().all()
        return [await self.get_info_pereval(pereval, session) for pereval in perevals]

    async def get_info_pereval(self, pereval: PerevalAdded, session: db_dependency) -> PerevalShowSchema:
        user = await self._get_user_by_id(pereval.user_id, session)
        coord = await self._get_coord_by_id(pereval.coord_id, session)
        level = await self._get_level_by_id(pereval.level_id, session)
        images = await self._get_images_by_pereval_id(pereval.id, session)
        return PerevalShowSchema(
            beauty_title=pereval.beauty_title,
            title=pereval.title,
            other_titles=pereval.other_titles,
            connect=pereval.connect,
            add_time=str(pereval.add_time),
            user=UserSchema(**jsonable_encoder(user)),
            coords=CoordsSchema(**jsonable_encoder(coord)),
            level=LevelSchema(**jsonable_encoder(level)),
            images=[ImageSchema(**jsonable_encoder(image)) for image in images],
            status=pereval.status,
        )

    async def _get_user_by_id(self, user_id: int, session: db_dependency) -> User:
        user = await session.execute(select(User).where(User.id == user_id))
        return user.scalar()

    async def _get_coord_by_id(self, coords_id: int, session: db_dependency) -> Coord:
        coord = await session.execute(select(Coord).where(Coord.id == coords_id))
        return coord.scalar()

    async def _get_level_by_id(self, level_id: int, session: db_dependency) -> Level:
        level = await session.execute(select(Level).where(Level.id == level_id))
        return level.scalar()

    async def _get_images_by_pereval_id(self, pereval_id: int, session: db_dependency) -> List[Image]:
        images = await session.execute(select(Image).where(Image.pereval_id == pereval_id))
        return images.scalars().all()

    async def get_pereval_by_id(self, pereval_id: int, session: db_dependency) -> Optional[PerevalAdded]:
        pereval = await session.execute(select(PerevalAdded).where(PerevalAdded.id == pereval_id))
        return pereval.scalar_one_or_none()

    async def add_pereval(
        self,
        pereval: Sequence[Tuple[PerevalAddSchema, PerevalShowSchema]],
        session: db_dependency,
    ) -> int:
        """
        Добавление перевала
        :param db: сессия
        :param pereval: данные с post запроса
        :return: id записи
        """
        user_id = await self._add_user(pereval.user, session)
        coords_id = await self._add_coords(pereval.coords, session)
        level_id = await self._add_levels(pereval.level, session)
        db_pereval = PerevalAdded(
            beauty_title=pereval.beauty_title,
            title=pereval.title,
            other_titles=pereval.other_titles,
            connect=pereval.connect,
            add_time=datetime.strptime(pereval.add_time, '%Y-%m-%d %H:%M:%S'),
            user_id=user_id,
            coord_id=coords_id,
            level_id=level_id,
        )
        session.add(db_pereval)
        await session.commit()

        if pereval.images:
            await self._add_images(db_pereval.id, pereval.images, session)
        return db_pereval.id

    async def _add_images(self, pereval_id: int, images: List[ImageSchema], session: db_dependency) -> None:
        list_img = [Image(**image.model_dump(), pereval_id=pereval_id) for image in images]
        session.add_all(list_img)
        await session.commit()

    async def _add_coords(self, coords: CoordsSchema, session: db_dependency) -> int:
        coords_db = Coord(**coords.model_dump())
        session.add(coords_db)
        await session.commit()
        return coords_db.id

    async def _add_user(self, user: UserSchema, session: db_dependency) -> int:
        if not (user_db := await self.get_user_by_email(user.email, session)):
            user_db = User(**user.model_dump())
            session.add(user_db)
            await session.commit()
        return user_db.id

    async def get_user_by_email(self, email: str, session: db_dependency) -> Optional[User]:
        user = await session.execute(select(User).filter(User.email == email))
        return user.scalar_one_or_none()

    async def _add_levels(self, levels: LevelSchema, session: db_dependency) -> int:
        levels_db = Level(**levels.model_dump())
        session.add(levels_db)
        await session.commit()
        return levels_db.id

    async def update_pereval(
        self,
        db_pereval: PerevalAdded,
        data_update: PerevalReplaceSchema,
        session: db_dependency,
    ) -> bool:
        pereval_data = data_update.model_dump()
        try:
            pereval_data['add_time'] = datetime.strptime(data_update.add_time, '%Y-%m-%d %H:%M:%S')
            coords = pereval_data.pop('coords')
            level = pereval_data.pop('level')
            pereval_data.pop('images')
            await session.execute(update(Coord).where(Coord.id == db_pereval.coord_id).values(coords))
            await session.execute(update(Level).where(Level.id == db_pereval.level_id).values(level))
            await session.execute(delete(Image).where(Image.pereval_id == db_pereval.id))
            if data_update.images:
                await self._add_images(db_pereval.id, data_update.images, session)
            else:
                await session.execute(delete(Image).where(Image.pereval_id == db_pereval.id))
            await session.execute(update(PerevalAdded).where(PerevalAdded.id == db_pereval.id).values(pereval_data))
            await session.commit()
        except Exception as e:
            # Перезаписываем на первоначальное значение
            self.logger.warning(f'Error the update pereval "{db_pereval.id}". Delete data')
            info_pereval = await self.get_info_pereval(db_pereval, session)
            await self._delete_pereval(db_pereval, session)
            await self.add_pereval(info_pereval, session)
            self.logger.warning('Adding the original pereval. Success')
            raise PerevalUpdateError(e)
        return True

    async def _delete_pereval(self, pereval: PerevalAdded, session: db_dependency) -> None:
        await session.execute(delete(Image).where(Image.pereval_id == pereval.id))
        await session.execute(delete(PerevalAdded).where(PerevalAdded.id == pereval.id))
        await session.execute(delete(Coord).where(Coord.id == pereval.coord_id))
        await session.execute(delete(Level).where(Level.id == pereval.level_id))
        await session.commit()
