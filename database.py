from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Yinka31344555_@localhost/TodoApplicationDatabase"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Yinka31344555_@127.0.0.1:5000/todoapp"
SQLALCHEMY_DATABASE_URL = "postgresql://ljzwhizw:7cTRkzBbq2bMZtUXPlSwmrtn3IldZZN-@kashin.db.elephantsql.com/ljzwhizw" #elephantsql

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()