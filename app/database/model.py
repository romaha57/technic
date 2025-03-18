from geoalchemy2 import Geography
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from app.database.config import Base

organization_activity_association = Table(
    'organization_activity', Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    building_id = Column(Integer, ForeignKey('buildings.id'))
    building = relationship("Building", back_populates="organizations")

    activities = relationship("Activity", secondary=organization_activity_association, back_populates="organizations")
    phone_number = relationship('PhoneNumber', back_populates='organization')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def __repr__(self):
        return f'Organization({self.id}/{self.name})'


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('activities.id'))

    children = relationship(
        'Activity',
        backref=backref('parent', remote_side=[id]),
        lazy='dynamic'
    )
    organizations = relationship("Organization", secondary=organization_activity_association,
                                 back_populates="activities")

    def __repr__(self):
        return f"Activity({self.id}/{self.name}, parent_id={self.parent_id})"


class Building(Base):
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key=True)
    city = Column(String(length=100))
    street = Column(String(length=255))
    house_number = Column(String(length=20))
    number_premises = Column(String(length=20))
    location = Column(Geography(geometry_type='POINT', srid=4326))

    # Связь с организациями
    organizations = relationship("Organization", back_populates="building")

    def __repr__(self):
        return f'Building({self.id}/{self.city}, {self.street}, {self.house_number}, {self.number_premises})'


class PhoneNumber(Base):
    __tablename__ = 'phone_numbers'

    id = Column(Integer, primary_key=True)
    phone = Column(String(length=30))
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    organization = relationship("Organization", back_populates="phone_number")

    def __repr__(self):
        return f'PhoneNumber ({self.id}/{self.phone})'
