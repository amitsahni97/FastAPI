from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://nfmgzdce:3TsMnU7oEqd-fjP6gIoArl1J2ec42eH5@john.db.elephantsql.com/nfmgzdce"
#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:mysql97@127.0.0.1:3306/todoapp"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base =declarative_base()