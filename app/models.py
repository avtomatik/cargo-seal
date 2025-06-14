from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Entity(Base):
    __tablename__ = 'entities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(128), index=True)
    address = Column(String(255), default='Unknown')


class Vessel(Base):
    __tablename__ = 'vessels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    imo = Column(Integer, unique=True, nullable=False)
    date_built = Column(Date, nullable=False)


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


class BillOfLading(Base):
    __tablename__ = 'bills_of_lading'

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey('shipments.id'))
    number = Column(String(64), nullable=False)
    date = Column(Date, nullable=False)
    grade = Column(String(128), nullable=False)
    quantity = Column(Float, nullable=False)
    value = Column(Float, nullable=False)


class Shipment(Base):
    __tablename__ = 'shipments'

    id = Column(Integer, primary_key=True, index=True)
    deal_number = Column(Integer, unique=True, nullable=False)
    insured = Column(String(255), nullable=False)
    vessel_id = Column(Integer, ForeignKey('vessels.id'))
    loadport_locality = Column(String(128), nullable=False)
    loadport_country = Column(String(128), nullable=False)
    disport_locality = Column(String(128), nullable=False)
    disport_country = Column(String(128), nullable=False)
    subject_matter_insured = Column(String(255), nullable=False)
    weight_metric = Column(Float, nullable=False)
    sum_insured = Column(Float, nullable=False)
    ccy = Column(String(10), default='USD')
    operator = Column(String(255), nullable=False)
    volume_bbl = Column(Float, default=0.0)
    basis_of_valuation = Column(Float, default=0.0)
    disport_eta = Column(Date)

    vessel = relationship('Vessel', backref='shipments')
    bills_of_lading = relationship('BillOfLading', backref='shipment')
