from pydantic import BaseModel, Field


class ActivitySchema(BaseModel):
    id: int = Field(description='ID деятельности')
    name: str = Field(description='Название деятельности')
    parent_id: int = Field(description='ID родительской деятельности')
