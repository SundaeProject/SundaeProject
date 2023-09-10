from . import Base
from sqlalchemy import Column, Integer, String


class TestModel(Base):
    __tablename__ = "test_model"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<TestModel: {self.name}>"
