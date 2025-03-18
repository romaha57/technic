from app.database.model import Organization


def convert_org_data(org: Organization) -> dict:
    org_data = org.to_dict()
    org_data["building"] = {
        "id": org.building.id,
        "city": org.building.city,
        "street": org.building.street,
        "house_number": org.building.house_number,
        "number_premises": org.building.number_premises,
        "location": str(org.building.location)
    } if org.building else None

    org_data["activities"] = [
        {"id": act.id, "name": act.name, "parent_id": act.parent_id}
        for act in org.activities
    ]

    org_data["phone_numbers"] = [
        phone.phone
        for phone in org.phone_number
    ]

    return org_data
