from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:cfQCDFibNuxVjEWubsrxGrBUaKYPBFdC@centerbeam.proxy.rlwy.net:28717/traffic_app"  
#not temporary! - ^^above^^ url is now complete.

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
