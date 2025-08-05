from enum import Enum as PyEnum

from sqlalchemy import (Column, Date, Enum, Float, ForeignKey, Integer,
                        Numeric, String)
from sqlalchemy.orm import relationship

from .database import Base


class BillOfLading(Base):
    __tablename__ = 'bills_of_lading'

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey('shipments.id'), nullable=False)
    number = Column(String(64), nullable=False)
    date = Column(Date, nullable=False)
    product = Column(String(128), nullable=False)
    quantity_mt = Column(Float, nullable=False)
    quantity_bbl = Column(Float, nullable=True)
    value = Column(Float, nullable=False)
    ccy = Column(String(3), default='USD', nullable=False)

    shipment = relationship('Shipment', back_populates='bills_of_lading')


class Coverage(Base):
    __tablename__ = 'coverages'

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey('shipments.id'), nullable=False)
    policy_id = Column(Integer, ForeignKey('policies.id'), nullable=True)
    value_margin = Column(Float, nullable=False)

    debit_note = Column(String(255), default='#')
    ordinary_risks_rate = Column(Numeric(5, 4), default=0.0)
    war_risks_rate = Column(Numeric(5, 4), default=0.0)
    date = Column(Date)

    shipment = relationship('Shipment', back_populates='coverages')
    policy = relationship('Policy', backref='coverages')


class DocumentCategory(PyEnum):
    CLASS_CERTIFICATE = 'Class Certificate'
    CLASS_REPORT = 'Class Report'
    HM_POLICY = 'H M Policy'
    PI_POLICY = 'P I Policy'
    Q88 = 'Q88'


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255), nullable=True)
    category = Column(Enum(DocumentCategory), nullable=False)

    vessel_id = Column(Integer, ForeignKey('vessels.id'), nullable=False)
    provider_id = Column(Integer, ForeignKey('entities.id'), nullable=True)
    number = Column(String(64), nullable=True)
    date = Column(Date, nullable=False)

    vessel = relationship('Vessel', backref='documents')
    provider = relationship('Entity', backref='documents')

    def __repr__(self):
        return (
            f"<Document(filename='{self.filename}', "
            f"category='{self.category.name}', "
            f"vessel_id={self.vessel_id}, provider_id={self.provider_id}, "
            f"number='{self.number}', date={self.date})>"
        )


class Entity(Base):
    __tablename__ = 'entities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(128), index=True)
    address = Column(String(255), default='Unknown')


class Operator(Base):
    __tablename__ = 'operators'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)


class Policy(Base):
    __tablename__ = 'policies'

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey('entities.id'))
    insured_id = Column(Integer, ForeignKey('entities.id'))
    number = Column(String(255), nullable=False)
    inception = Column(Date, nullable=False)
    expiry = Column(Date, nullable=True)

    provider = relationship('Entity', foreign_keys=[provider_id])
    insured = relationship('Entity', foreign_keys=[insured_id])


class Port(Base):
    __tablename__ = 'ports'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    country = Column(String(64), nullable=False)
    region = Column(String(64), nullable=True)

    loadport_shipments = relationship(
        'Shipment',
        foreign_keys='Shipment.loadport_id',
        back_populates='loadport'
    )
    disport_shipments = relationship(
        'Shipment',
        foreign_keys='Shipment.disport_id',
        back_populates='disport'
    )

    @property
    def location(self):
        return f'{self.name}, {self.country}'


class Shipment(Base):
    __tablename__ = 'shipments'

    id = Column(Integer, primary_key=True, index=True)
    deal_number = Column(Integer, nullable=False)
    insured_id = Column(Integer, ForeignKey('entities.id'), nullable=False)
    vessel_id = Column(Integer, ForeignKey('vessels.id'))
    loadport_id = Column(Integer, ForeignKey('ports.id'), nullable=False)
    disport_id = Column(Integer, ForeignKey('ports.id'), nullable=False)
    operator_id = Column(Integer, ForeignKey('operators.id'), nullable=False)

    insured = relationship('Entity', backref='shipments_as_insured')
    vessel = relationship('Vessel', backref='shipments')
    bills_of_lading = relationship('BillOfLading', back_populates='shipment')

    loadport = relationship(
        'Port',
        foreign_keys=[loadport_id],
        back_populates='loadport_shipments'
    )
    disport = relationship(
        'Port',
        foreign_keys=[disport_id],
        back_populates='disport_shipments'
    )
    operator = relationship('Operator', backref='shipments')

    coverages = relationship('Coverage', back_populates='shipment')


class Vessel(Base):
    __tablename__ = 'vessels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    imo = Column(Integer, unique=True, index=True, nullable=False)
    date_built = Column(Date, nullable=False)
