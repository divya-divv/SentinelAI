from database.database import engine, Base
from database.models import Event


def initialize_database():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    initialize_database()
    print("SentinelAI database initialized successfully.")