# Create the table if it doesn't exist
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import Env

env = Env()

# Create the engine to connect to the database
engine = create_engine(
    f'postgresql://'
    f'{env.DB_USER}:'
    f'{env.DB_PASSWORD}@'
    f'{env.DB_HOST}:'
    f'{env.DB_PORT}/'
    f'{env.DB_NAME}'
)

# Create a session factory
Session = sessionmaker(bind=engine)
# Create a base class for declarative models
Base = declarative_base()


# EXAMPLES
# Create a session and add a new record to the database
# session = Session()
# record = MyModel(int_field_1=1, int_field_2=2, text_field='example text')
# session.add(record)
# session.commit()

# Query the database for all records and print them
# records = session.query(MyModel).all()
# for record in records:
#     print(record.id, record.int_field_1, record.int_field_2, record.text_field)
#
# # Close the session
# session.close()
