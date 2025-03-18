import logging

from fastapi import APIRouter, Depends, Query, status, Body, HTTPException, Path
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.auth import verify_api_key
from app.buildings.service import BuildingService
from app.database.config import get_async_session
from app.organizations.schemas import OrganizationSchema, OrganizationsByCoordinatesSchema, \
    OrganizationsByCoordinatesResponseSchema, OrganizationFullInfoResponseSchema
from app.organizations.service import OrganizationService
from app.organizations.utils import convert_org_data

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    '/by_building',
    tags=['Organization'],
    response_model=list[OrganizationSchema]
)
async def get_organizations_by_building(
    building_id: int = Query(),
    session: AsyncSession = Depends(get_async_session),
    auth: str = Depends(verify_api_key)
):
    """
    ## Получение организаций по id здания
    **Пример запроса:**
    ```
    GET /organization/by_building_id/{building_id}
    ```
    """
    try:
        org_service = OrganizationService(session)
        organizations = await org_service.get_by_buildings([building_id])

        return JSONResponse(organizations, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)


@router.get(
    '/by_activity',
    tags=['Organization'],
    response_model=list[OrganizationSchema]
)
async def get_organizations_by_activity(
    activity_id: int = Query(),
    session: AsyncSession = Depends(get_async_session),
    auth: str = Depends(verify_api_key)
):
    """
    ## Получение организаций по id деятельности
    **Пример запроса:**
    ```
    GET /organization/by_activity/{activity_id}
    ```
    """

    try:
        org_service = OrganizationService(session)
        organizations = await org_service.get_by_activity(activity_id)

        return JSONResponse(organizations, status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(e)


@router.get(
    '/{org_id}',
    tags=['Organization'],
    response_model=OrganizationFullInfoResponseSchema
)
async def get_organizations_by_id(
    org_id: int = Path(),
    session: AsyncSession = Depends(get_async_session),
    auth: str = Depends(verify_api_key)
):
    """
    ## Получение организаций по id
    **Пример запроса:**
    ```
    GET /organization/{org_id}
    ```
    """

    try:
        org_service = OrganizationService(session)
        _organization = await org_service.get_by_id(org_id)
        organization = convert_org_data(_organization)

        return JSONResponse(organization, status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(e)


@router.post(
    '/by_coordinates',
    tags=['Organization'],
    response_model=OrganizationsByCoordinatesResponseSchema
)
async def get_organizations_by_coordinates(
    payload: OrganizationsByCoordinatesSchema = Body(),
    session: AsyncSession = Depends(get_async_session),
    auth: str = Depends(verify_api_key)
):
    """
    ## Получение организаций по id
    **Пример запроса:**

    POST /organization/by_coordinates

    **Тело запроса:**
    ```json
    {
      "circle": {
        "center": {
          "latitude": Широта центра,
          "longitude": Долгота центра
        },
        "radius_m": радиус поиска(в метрах)
      },
      "rectangle": {
        "top_left": {
          "latitude": Широта левого верхнего ушла,
          "longitude": Долгота левого верхнего ушла
        },
        "bottom_right": {
          "latitude": Широта правого нижнего угла,
          "longitude": Долгота правого нижнего угла
        }
      }
    }
    ```
    """

    try:
        b_service = BuildingService(session)
        o_service = OrganizationService(session)

        if payload.circle and payload.circle.radius_m:
            buildings = await b_service.get_buildings_by_circle(
                center_lat=payload.circle.center.latitude,
                center_lon=payload.circle.center.longitude,
                radius_m=payload.circle.radius_m
            )
            building_id_list = [b.get('id') for b in buildings]
            organizations = await o_service.get_by_buildings(
                building_id_list=building_id_list
            )
        elif payload.rectangle and payload.rectangle.top_left and payload.rectangle.bottom_right:
            buildings = await b_service.get_building_bt_rectangle(
                top_left_lon=payload.rectangle.top_left.longitude,
                top_left_lat=payload.rectangle.top_left.latitude,
                bottom_right_lat=payload.rectangle.bottom_right.latitude,
                bottom_right_lon=payload.rectangle.bottom_right.longitude
            )
            building_id_list = [b.get('id') for b in buildings]
            organizations = await o_service.get_by_buildings(
                building_id_list=building_id_list
            )
        else:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Filter data is invalid'
            )

        result = {
            'organizations': organizations,
            'buildings': buildings
        }

        return JSONResponse(result, status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(e)


@router.get(
    '/',
    tags=['Organization'],
    response_model=list[OrganizationSchema]
)
async def search_organizations_by_name(
    search: str = Query(),
    session: AsyncSession = Depends(get_async_session),
    auth: str = Depends(verify_api_key)
):
    """
    ## Поиск по названию организации
    **Пример запроса:**
    ```
    GET /organization/?search={search_string}

    """
    try:
        org_service = OrganizationService(session)
        organizations = await org_service.search_by_name(search)

        return JSONResponse(organizations, status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(e)


@router.get(
    '/by_activity/',
    tags=['Organization'],
    response_model=list[OrganizationSchema]
)
async def search_organizations_by_activity(
    activity_id: int = Query(),
    session: AsyncSession = Depends(get_async_session),
    auth: str = Depends(verify_api_key)
):
    """
    ## Поиск по activity_id (с учетом вложенности деятельностей)
    **Пример запроса:**
    ```
    GET /organization/by_activity/{activity_id}

    """
    try:
        org_service = OrganizationService(session)
        organizations = await org_service.search_by_activity(activity_id)

        return JSONResponse(organizations, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
