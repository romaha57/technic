from sqlalchemy import select, func
from geoalchemy2 import functions, Geography, Geometry

from app.base.service import BaseService
from app.buildings.schemas import BuildingSchema
from app.database.model import Building


class BuildingService(BaseService):
    async def get_buildings_by_circle(self, center_lon: float, center_lat: float, radius_m: float) -> list[dict]:
        """
        Получение зданий в радиусе от центра
        """
        query = await self.session.execute(
            select(
                Building.id, Building.city, Building.street, Building.house_number, Building.number_premises
            ).where(
                functions.ST_DWithin(
                    Building.location,
                    functions.ST_SetSRID(functions.ST_MakePoint(center_lat, center_lon), 4326).cast(Geography),
                    radius_m
                )
            ))
        _building = query.mappings().all()
        building = self.convert_to_dict(_building, BuildingSchema)

        return building

    async def get_building_bt_rectangle(self, top_left_lon: float, top_left_lat: float,
                                        bottom_right_lon: float, bottom_right_lat: float):
        """
        Получение зданий в прямоугольнике по координатам
        """
        query = await self.session.execute(
            select(
                Building.id, Building.city, Building.street, Building.house_number, Building.number_premises
            ).where(
                func.ST_Within(
                    func.cast(Building.location, Geometry),
                    func.ST_MakeEnvelope(
                        bottom_right_lat, top_left_lon,
                        top_left_lat, bottom_right_lon,
                        4326
                    )
                )
            )
        )
        _building = query.mappings().all()
        building = self.convert_to_dict(_building, BuildingSchema)

        return building
