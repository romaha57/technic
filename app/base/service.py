from typing import Sequence

from pydantic._internal._model_construction import ModelMetaclass
from sqlalchemy import Row, RowMapping

from app.database.config import AsyncSession


class BaseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def convert_to_dict(raw_data: Sequence[Row | RowMapping], schema: ModelMetaclass) -> list[dict]:
        """
        Преобразовывает sqlalchemy model -> dict
        """
        return [schema(**data).model_dump() for data in raw_data]
