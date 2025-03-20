from datetime import datetime
from src.models.pereval import PerevalAdded
from src.dependencies import db_dependency
from sqlalchemy.future import select
from src.schemas.pereval import PerevalPostSchema
from typing import List
from src.models import Image, User, Coord, Level
from src.schemas import ImageSchema, UserSchema, CoordsSchema, LevelSchema
from typing import Optional


class Pereval:

    async def add_pereval(self, pereval: PerevalPostSchema, session: db_dependency) -> PerevalAdded:
        '''
        Добавление перевала
        :param db: сессия
        :param pereval: данные с post запроса
        :return:
        '''
        user_id = await self.add_user(pereval.user, session)
        coords_id = await self.add_coords(pereval.coords, session)
        level_id = await self.add_levels(pereval.level, session)
        db_pereval = PerevalAdded(
            beauty_title=pereval.beauty_title,
            title=pereval.title,
            other_titles=pereval.other_titles,
            connect=pereval.connect,
            add_time=datetime.strptime(pereval.add_time, "%Y-%m-%d %H:%M:%S"),
            user_id=user_id,
            coord_id=coords_id,
            level_id=level_id,
        )
        session.add(db_pereval)
        await session.commit()

        if pereval.images:
            await self.add_images(db_pereval.id, pereval.images, session)
        return db_pereval

    async def add_images(self, pereval_id: int, images: List[ImageSchema], session: db_dependency) -> None:
        list_img = [Image(**image.model_dump(), pereval_id=pereval_id) for image in images]
        session.add_all(list_img)
        await session.commit()

    async def add_coords(self, coords: CoordsSchema, session: db_dependency) -> int:
        coords_db = Coord(**coords.model_dump())
        session.add(coords_db)
        await session.commit()
        return coords_db.id

    async def add_user(self, user: UserSchema, session: db_dependency) -> int:
        if not (user_db := await self.get_user_by_email(user.email, session)):
            user_db = User(**user.model_dump())
            session.add(user_db)
            await session.commit()
        return user_db.id

    async def get_user_by_email(self, email: str, session: db_dependency) -> Optional[User]:
        if user := await session.execute(select(User).filter(User.email == email)):
            return user.scalars().first()
        return None

    async def add_levels(self, levels: LevelSchema, session: db_dependency) -> int:
        levels_db = Level(**levels.model_dump())
        session.add(levels_db)
        await session.commit()
        return levels_db.id
