from src.postgres import Base, engine
from src.postgres.models.my_model import MyModel


def init_db():
    Base.metadata.create_all(engine)
