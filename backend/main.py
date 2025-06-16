from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Database Setup
DATABASE_URL = "sqlite:///./database.sql"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Security Setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SQLAlchemy Models
class StudentDB(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    cluster_points = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    min_cluster = Column(Float)
    expected_pay = Column(String)
    industries = Column(Text)
    skills_needed = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    cluster_points: float

class Token(BaseModel):
    access_token: str
    token_type: str

class CourseOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    min_cluster: float
    expected_pay: str
    industries: str
    skills_needed: str

    class Config:
        orm_mode = True

class CourseCreate(BaseModel):
    title: str
    description: Optional[str]
    min_cluster: float
    expected_pay: str
    industries: str
    skills_needed: str

# FastAPI App
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utils
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Auth
@app.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    logging.info(f"Attempting to register user: {user.email}")
    existing_user = db.query(StudentDB).filter(StudentDB.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = StudentDB(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        cluster_points=user.cluster_points
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"access_token": db_user.email, "token_type": "bearer"}

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(StudentDB).filter(StudentDB.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"access_token": user.email, "token_type": "bearer"}

@app.get("/courses", response_model=List[CourseOut])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@app.post("/courses")
def add_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(**course.dict())
    db.add(new_course)
    db.commit()
    return {"message": "Course added successfully"}

@app.get("/recommend/{email}", response_model=List[CourseOut])
def recommend(email: str, db: Session = Depends(get_db)):
    user = db.query(StudentDB).filter(StudentDB.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Student not found")
    return db.query(Course).filter(Course.min_cluster <= user.cluster_points).order_by(Course.min_cluster.desc()).limit(2).all()
