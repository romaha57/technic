from pydantic import BaseModel, Field


class BuildingSchema(BaseModel):
    id: int = Field(description='ID здания')
    city: str = Field(description='Город')
    street: str = Field(description='Улица')
    house_number: str = Field(description='Номер дома')
    number_premises: str = Field(description='Номер помещения')
