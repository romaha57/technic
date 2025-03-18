from sqlalchemy import select, func, or_, distinct
from sqlalchemy.orm import joinedload

from app.base.service import BaseService
from app.database.model import Organization, organization_activity_association, Building, PhoneNumber, Activity
from app.organizations.schemas import OrganizationSchema


class OrganizationService(BaseService):

    async def get_by_id(self, org_id: int) -> Organization:
        query = (
            select(Organization)
            .options(
                joinedload(Organization.building),
                joinedload(Organization.activities),
                joinedload(Organization.phone_number)
            )
        ).where(
            Organization.id == org_id
        )

        result = await self.session.execute(query)
        organization = result.scalars().first()

        return organization

    async def get_by_buildings(self, building_id_list: list[int]) -> list[dict]:
        query = await self.session.execute(
            select(
                Organization.id, Organization.name
            ).where(
                Organization.building_id.in_(building_id_list)
            )
        )
        _organizations = query.mappings().all()
        organizations = self.convert_to_dict(_organizations, OrganizationSchema)

        return organizations

    async def get_by_activity(self, activity_id: int) -> list[dict]:
        query = await self.session.execute(
            select(
                Organization.id, Organization.name
            ).join(
                organization_activity_association, organization_activity_association.c.organization_id == Organization.id
            ).where(
                organization_activity_association.c.activity_id == activity_id
            )
        )
        _organizations = query.mappings().all()
        organizations = self.convert_to_dict(_organizations, OrganizationSchema)

        return organizations

    async def search_by_name(self, search: str) -> list[dict]:
        query = await self.session.execute(
            select(
                Organization.id, Organization.name
            ).where(
                or_(
                    Organization.name.like(f'%{search}%'),
                    Organization.name.like(f'%{search.lower()}%'),
                    Organization.name.like(f'%{search.upper()}%'),
                    Organization.name.like(f'%{search.capitalize()}%')
                )
            )
        )
        _organizations = query.mappings().all()
        organizations = self.convert_to_dict(_organizations, OrganizationSchema)

        return organizations

    async def search_by_activity(self, activity_id: int) -> list[dict]:
        cte = (
            select(Activity.id)
            .where(Activity.id == activity_id)  # Начинаем с корневой активности
            .cte(recursive=True)
        )

        # Рекурсивная часть CTE: выбираем дочерние элементы
        cte = cte.union_all(
            select(Activity.id)
            .join(cte, Activity.parent_id == cte.c.id)  # Ищем дочерние элементы
        )


        # Основной запрос: выбираем все активности, найденные в CTE
        query = select(
            distinct(Organization.id).label('id'), Organization.name
        ).join(
            organization_activity_association, organization_activity_association.c.organization_id == Organization.id
        ).where(
            organization_activity_association.c.activity_id.in_(select(cte))
        )

        query = await self.session.execute(query)
        _organizations = query.mappings().all()
        organizations = self.convert_to_dict(_organizations, OrganizationSchema)

        return organizations

