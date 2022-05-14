from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Boolean, Column, Float, String, Integer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = 'sqlite:///./sensor_data.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# A SQLAlchemny ORM Place
class DBItem(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    temp = Column(Float)
    hum = Column(Float)

Base.metadata.create_all(bind=engine)

# ip + root path
@app.get("/")
def read_root():
    return {"Message": "Hello"}

# cutom path
@app.get("/hello")
def read_root():
    return {"Message": "Hello"}

# path + path variable
@app.get("/items/{item_id}")
def randomname(item_id: int):
    return {"item_id": item_id}

# query parameter
@app.get("/items")
def read_item( q: Optional[str] = None, a: Optional[str] = None):
    return { "q": q, "a": a}

class Item(BaseModel):
    temp: float
    hum: float

    class Config:
        orm_mode = True

def create_item(db: Session, item: Item):
    db_item = DBItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

# post request
@app.post("/itemlist", response_model=Item)
def create_item_api(item: Item , db: Session = Depends(get_db)):
    db_item = create_item(db, item)
    return db_item

# query parameter
@app.get("/itemlist", response_model=List[Item])
def get_item(db: Session = Depends(get_db)):
    return db.query(DBItem).all()
