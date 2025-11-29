from datetime import datetime, timedelta
from sqlalchemy import (
    Column, Integer, 
    String, 
    DateTime, Text, 
    ForeignKey,
    Boolean,
    func
)
from sqlalchemy.orm import relationship
from .db import Base



# Author model
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    books = relationship("Book", back_populates="author")


# Book model
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id', ondelete='CASCADE'))

    published_year = Column(Integer)
    isbn = Column(String(13), unique=True, nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    author = relationship("Author", back_populates="books")
    borrows = relationship("Borrow", back_populates="book")


# Student model
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    grade = Column(String(20), nullable=True)
    registered_at = Column(DateTime, default=datetime.now)

    borrows = relationship("Borrow", back_populates="student")


# Borrow model
class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    
    borrowed_at = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime, default=lambda: datetime.now() + timedelta(days=14))

    returned_at = Column(DateTime, nullable=True)

    student = relationship("Student", back_populates="borrows")
    book = relationship("Book", back_populates="borrows")