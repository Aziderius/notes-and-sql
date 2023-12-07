from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime 
from datetime import datetime
import os
from dotenv import load_dotenv


#Conexión con la base de datos postgreSQL 
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

#Clase Person y su tabla para almacenar la información del usuario
class Person(Base):
    __tablename__ = "person"

    person_id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"Hello! {self.username}"


#Clase Notes y su tabla para almacenar las notas de los usuarios en la base de datos
class Notes(Base):
    __tablename__ = "notes"

    note_id = Column(Integer(), primary_key=True)
    owner = Column(Integer, ForeignKey("person.person_id"))
    title = Column(String(50))
    note = Column(String(200))
    created_at = Column(DateTime(), default=datetime.now())

    def __init__(self, owner, title, note, created_at=None):
        self.owner = owner
        self.title = title
        self.note = note
        self.created_at = created_at if created_at is not None else datetime.now()

    def __repr__(self):
        return f"Your title is: {self.title}\n And the note is: {self.note}.\n Created at: {self.created_at} by {self.owner}"
    

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
