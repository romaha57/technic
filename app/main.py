import asyncio

import uvicorn
from fastapi import FastAPI

from app.organizations.endpoints import router as organization_router
from app.scripts import fill_db

app = FastAPI()
app.include_router(organization_router, prefix='/organization')


app.add_event_handler('startup', fill_db)


if __name__ == '__main__':
    uvicorn.run(app="app.main:app", reload=True, port=8000)
