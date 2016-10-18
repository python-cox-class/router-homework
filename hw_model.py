import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Link(Base):
    __tablename__ = 'links'

    id = sa.Column(sa.Integer(), primary_key=True)
    netmask = sa.Column(sa.Text())

    interfaces = relationship('Interface', back_populates='link')


class Router(Base):
    __tablename__ = 'routers'

    id = sa.Column(sa.Integer(), primary_key=True)
    address = sa.Column(sa.Text())

    interfaces = relationship('Interface', back_populates='router')


class Interface(Base):
    __tablename__ = 'interfaces'

    id = sa.Column(sa.Integer(), primary_key=True)
    link_id = sa.Column(sa.ForeignKey('links.id'))
    router_id = sa.Column(sa.ForeignKey('routers.id'))

    router = relationship('Router', back_populates='interfaces')
    link = relationship('Link', back_populates='interfaces')
