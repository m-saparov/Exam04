from datetime import datetime
from sqlalchemy import or_, not_, and_
from .models import (
    Author, Book, Student, Borrow
)
from .db import get_db

def create_author(name: str, bio: str = None) -> Author:
    """Yangi muallif yaratish"""
    author = Author(
        name = name,
        bio = bio
    )

    with get_db() as session:
        session.add(author)
        session.commit()

    return author

def get_author_by_id(author_id: int) -> Author | None:
    """ID bo'yicha muallifni olish"""
    with get_db() as session:
        author = session.query(Author).get(id)
    
    return author

def get_all_authors() -> list[Author]:
    """Barcha mualliflar ro'yxatini olish"""
    with get_db() as session:
        authors = session.query(Author).all()

    return authors

def update_author(author_id: int, name: str = None, bio: str = None) -> Author | None:
    """Muallif ma'lumotlarini yangilash"""
    author = get_author_by_id(author_id)

    if author:
        with get_db() as session:
            author.name = name if name else author.name
            author.bio = bio if name else author.bio

            session.add(author)
            session.commit()
    
    return author

def delete_author(author_id: int) -> bool:
    """Muallifni o'chirish (faqat kitoblari bo'lmagan holda)"""
    author = get_author_by_id(author_id)
    result = False

    if author:
        with get_db() as session:
            session.delete(author)
            session.commit()
        
        result = True

    return result