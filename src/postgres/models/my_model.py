from sqlalchemy import Column, Integer, String
from src.postgres import Base


class MyModel(Base):
    __tablename__ = 'my_model'
    id = Column(Integer, primary_key=True)
    int_field_1 = Column(Integer)
    int_field_2 = Column(Integer)
    text_field = Column(String)
