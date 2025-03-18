from geoalchemy2 import WKTElement
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.config import AsyncSession
from app.database.model import Activity, Building, Organization, PhoneNumber


async def fill_db():
    async with AsyncSession() as session:
        _data_in_db_query = await session.execute(
           select(Activity)
        )
        data_in_db = _data_in_db_query.fetchone()
        if not data_in_db:
            # верхне-уровневые разделы
            food = Activity(name="Еда")
            cars = Activity(name="Автомобили")

            # дочерние разделы
            meat = Activity(name="Мясная продукция", parent=food)
            dairy = Activity(name="Молочная продукция", parent=food)
            trucks = Activity(name="Грузовые", parent=cars)
            passenger = Activity(name="Легковые", parent=cars)

            # дочерние разделы
            parts = Activity(name="Запчасти", parent=passenger)
            accessories = Activity(name="Аксессуары", parent=passenger)
            wheels = Activity(name="Аксессуары", parent=trucks)

            # дочерние разделы
            milk = Activity(name="Молоко", parent=dairy)
            yogurt = Activity(name="Йогурт", parent=dairy)

            # дочерние разделы
            danissimo = Activity(name='Danissimo', parent=yogurt)
            prosto_moloko = Activity(name='Prosto Moloko', parent=milk)

            activities_data = [food, cars, meat, dairy, trucks, passenger, parts, accessories, wheels, meat, yogurt, danissimo, prosto_moloko]
            session.add_all(activities_data)
            await session.commit()

            location_1 = WKTElement(f'POINT({55.775803} {37.596929})', srid=4326)
            building_1 = Building(
                city='Москва',
                street='Фадеева',
                house_number='10',
                number_premises='3a',
                location=location_1
            )

            location_2 = WKTElement(f'POINT({55.752602} { 37.599750})', srid=4326)
            building_2 = Building(
                city='Москва',
                street='Новый арбат',
                house_number='1/2',
                number_premises='10',
                location=location_2
            )

            location_3 = WKTElement(f'POINT({55.753727} {37.600082})', srid=4326)
            building_3 = Building(
                city='Москва',
                street='Никитинский бульвар',
                house_number='7',
                number_premises='1',
                location=location_3
            )
            location_4 = WKTElement(f'POINT({55.812871} {49.108344})', srid=4326)
            building_4 = Building(
                city='Казань',
                street='Чаша',
                house_number='7',
                number_premises='1',
                location=location_4
            )

            building_data = [building_1, building_2, building_3, building_4]
            session.add_all(building_data)
            await session.commit()

            org_1 = Organization(
                name='Рога и копыта',
                building_id=building_1.id
            )
            org_1.activities.extend([food, meat, dairy, milk, yogurt, prosto_moloko, danissimo])

            org_2 = Organization(
                name='Ford',
                building_id=building_1.id
            )
            org_2.activities.extend([cars, trucks, parts])

            org_3 = Organization(
                name='Ferrari',
                building_id=building_2.id
            )
            org_3.activities.extend([cars, passenger, accessories])

            org_4 = Organization(
                name='Cordian',
                building_id=building_3.id
            )
            org_4.activities.extend([cars, trucks, wheels])

            org_5 = Organization(
                name='ЗАГС',
                building_id=building_4.id
            )
            org_5.activities.extend([cars, trucks, wheels])

            org_6 = Organization(
                name='TEST',
                building_id=building_3.id
            )
            org_6.activities.extend([danissimo])

            organization_data = [org_1, org_2, org_3, org_4, org_5, org_6]
            session.add_all(organization_data)
            await session.commit()

            phone_1 = PhoneNumber(phone='89175553535', organization_id=org_1.id)
            phone_2 = PhoneNumber(phone='8917111111', organization_id=org_2.id)
            phone_3 = PhoneNumber(phone='8917222222', organization_id=org_3.id)
            phone_4 = PhoneNumber(phone='8917333333', organization_id=org_4.id)
            phone_5 = PhoneNumber(phone='8917444444', organization_id=org_4.id)

            phone_data = [phone_1, phone_2, phone_3, phone_4, phone_5]
            session.add_all(phone_data)
            await session.commit()
