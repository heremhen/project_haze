from typing import TypeVar

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    PickleType,
    String,
    func,
)
from sqlalchemy.orm import Mapped, declarative_base, relationship

__all__ = (
    "Base",
    "UsersTable",
    "ProductsTable",
    "OrdersTable",
    "RegistryTable",
    "ModelsTable",
)

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class _Base:
    """Base class for all database models."""

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


Base = declarative_base(cls=_Base, metadata=meta)

ConcreteTable = TypeVar("ConcreteTable", bound=Base)


class UsersTable(Base):
    __tablename__ = "users"

    username: str = Column(String, nullable=False, unique=True)
    password: str = Column(String, nullable=False)
    email: str = Column(String, nullable=True, default=None, unique=True)
    full_name: str = Column(String, nullable=True, default=None)
    disabled: bool = Column(Boolean, nullable=True, default=None)


class ProductsTable(Base):
    __tablename__ = "products"

    name: str = Column(String, nullable=False)
    price: int = Column(Integer, nullable=False)


class OrdersTable(Base):
    __tablename__ = "orders"

    amount: int = Column(Integer, nullable=False, default=1)

    product_id: int = Column(ForeignKey(ProductsTable.id), nullable=False)
    user_id: int = Column(ForeignKey(UsersTable.id), nullable=False)

    user: "Mapped[UsersTable]" = relationship("UsersTable", uselist=False)
    product: "Mapped[ProductsTable]" = relationship(
        "ProductsTable", uselist=False
    )


class RegistryTable(Base):  # FilesTable
    __tablename__ = "registry"

    filename: str = Column(String, nullable=False)
    uuid: str = Column(String, nullable=False)
    extension: str = Column(String, nullable=False)
    type: str = Column(String, nullable=False)
    url: str = Column(String, nullable=False)
    user_id: int = Column(ForeignKey(UsersTable.id), nullable=False)

    user: "Mapped[UsersTable]" = relationship("UsersTable", uselist=False)


class ModelsTable(Base):
    __tablename__ = "models"

    name: str = Column(String, nullable=False, default="CH4NGE ME")
    description: str = Column(String, nullable=True)
    target_attribute: str = Column(String, nullable=False)
    test_size_threshold: float = Column(Float, nullable=False)
    time_budget: int = Column(Integer, nullable=False)
    pipeline_type: str = Column(String, nullable=False)
    pipeline_route: str = Column(String, nullable=True)
    css_background: str = Column(String, nullable=True)
    version: float = Column(Float, nullable=False, default=1.0)
    dropped_columns = Column(PickleType, nullable=True)
    prediction_input_fields: dict = Column()

    registry_id: int = Column(ForeignKey(RegistryTable.id), nullable=False)
    inherited_from_id: int = Column(
        ForeignKey(RegistryTable.id), nullable=True
    )
    user_id: int = Column(ForeignKey(UsersTable.id), nullable=False)

    registry: "Mapped[RegistryTable]" = relationship(
        "RegistryTable", foreign_keys=[registry_id], uselist=False
    )
    inheritance: "Mapped[RegistryTable]" = relationship(
        "RegistryTable", foreign_keys=[inherited_from_id], uselist=False
    )
    user: "Mapped[UsersTable]" = relationship(
        "UsersTable", foreign_keys=[user_id], uselist=False
    )
