from datetime import datetime
from sqlalchemy import (
    Column, Integer, 
    String, 
    DateTime, Text, 
    ForeignKey,
    Boolean
)
from sqlalchemy.orm import relationship
from .db import Base



# Author model
class Author(Base):
    __tablename__ = 'authors'

    # auto increment -> primary_key=True 
    id = Column('id', Integer, primary_key=True, nullable=False)
    name = Column('name', String(length=100), nullable=False)
    bio = Column('bio', Text, nullable=True)
    created_at = Column('created_at', DateTime, default=datetime.now)

    books = relationship("Book", back_populates="author")


# Book model
class Book(Base):
    __tablename__ = 'books'

    id = Column('id', Integer, primary_key=True, nullable=False)
    title = Column('title', String(length=200), nullable=False)

    # foreign key uchun integer tur bo'lishi shart
    author_id = Column('author_id', Integer, ForeignKey('authors.id', ondelete='CASCADE'))

    published_year = Column('published_year', Integer)
    isbn = Column('isbn', String(length=13), unique=True, nullable=True)
    is_available = Column('is_available', Boolean, default=True)
    created_at = Column('created_at', DateTime, default=datetime.now)
    updated_at = Column('updated_at', DateTime, onupdate=datetime.now)

    author = relationship("Author", back_populates="books")
    borrows = relationship("Borrow", back_populates="book")


# Student model
class Student(Base):
    __tablename__ = 'students'

    id = Column('id', Integer, primary_key=True, nullable=False)
    full_name = Column('full_name', String(length=150), nullable=False)
    email = Column('email', String(length=100), unique=True, nullable=False)
    grade = Column('grade', String(length=20), nullable=True)
    registered_at = Column('registered_at', DateTime, default=datetime.now)

    borrows = relationship("Borrow", back_populates="student")


# Borrow model
class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    
    borrowed_at = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime)

    # returned_at — default None bo‘ladi
    returned_at = Column(DateTime, nullable=True)

    student = relationship("Student", back_populates="borrows")
    book = relationship("Book", back_populates="borrows")
