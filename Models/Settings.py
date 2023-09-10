from . import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
import platform


class Settings(Base):
    __tablename__ = "base_settings"

    system_name = Column(
        String(50), primary_key=True, default=platform.node(), nullable=False
    )
    identifier = Column(String(50), nullable=False, unique=True)
