from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Short_url(Base):
    
    __tablename__ = "short_url"
    
    url = Column(String(280), nullable = False)
    id = Column(Integer, primary_key = True)
    
    

engine = create_engine("postgresql://USER:PASSWORD@localhost/DB_NAME")
Base.metadata.create_all(engine)