from pydantic import BaseModel, Field

from app.activities.schemas import ActivitySchema
from app.buildings.schemas import BuildingSchema


class OrganizationSchema(BaseModel):
    id: int = Field(description='ID организации')
    name: str = Field(description='Название организации')


class Coordinates(BaseModel):
    latitude: float = Field(description='Широта')
    longitude: float = Field(description='Долгота')


class RadiusFilter(BaseModel):
    center: Coordinates
    radius_m: float = Field(description='Радиус от центра в метрах')


class RectangleFilter(BaseModel):
    top_left: Coordinates = Field(description='Координаты верхнего левого угла прямоугольника')
    bottom_right: Coordinates = Field(description='Координаты нижнего правого угла прямоугольника')


class OrganizationsByCoordinatesSchema(BaseModel):
    circle: RadiusFilter = Field(default=None, description='Поиск по кругу')
    rectangle: RectangleFilter = Field(default=None, description='Поиск по прямоугольнику')


class OrganizationsByCoordinatesResponseSchema(BaseModel):
    organizations: list[OrganizationSchema] = Field(description='Список организаций')
    buildings: list[BuildingSchema] = Field(description='Список зданий')


class OrganizationFullInfoResponseSchema(OrganizationSchema):
    building: list[BuildingSchema] = Field(description='Данные по зданию')
    phone_numbers: list[str] = Field(description='Номера телефонов')
    activities: list[ActivitySchema] = Field(description='Список деятельностей организации')
