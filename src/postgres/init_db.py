from src.postgres import Base
from src.postgres import engine
from src.postgres.models.my_model import DailyTotalLoad
from src.postgres.models.my_model import MonthlyTotalLoad
from src.postgres.models.my_model import TotalLoad
from src.postgres.models.my_model import WeeklyTotalLoad


def init_db():
    Base.metadata.create_all(engine)
