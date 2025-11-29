from datetime import datetime, timedelta
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
        author = session.query(Author).get(author_id)
    
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
            author.bio = bio if bio else author.bio

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

def create_book(title: str, author_id: int, published_year: int, isbn: str = None) -> Book:
    """Yangi kitob yaratish"""
    book = Book(
        title = title,
        author_id = author_id,
        published_year = published_year,
        isbn = isbn
    )

    with get_db() as session:
        session.add(book)
        session.commit()

    return book

def get_book_by_id(book_id: int) -> Book | None:
    """ID bo'yicha kitobni olish"""
    with get_db() as session:
        book = session.query(Book).get(book_id)

    return book

def get_all_books() -> list[Book]:
    """Barcha kitoblar ro'yxatini olish"""
    with get_db() as session:
        books = session.query(Book).all()
    
    return books

def search_books_by_title(title: str) -> list[Book]:
    """Kitoblarni sarlavha bo'yicha qidirish (partial match)"""
    with get_db() as session:
        books = session.query(Book).filter(
            Book.title.ilike(f"%{title}%")
        ).all()
    return books

def delete_book(book_id: int) -> bool:
    """Kitobni o'chirish"""
    book = get_book_by_id(book_id)
    result = False

    if book:
        with get_db() as session:
            session.delete(book)
            session.commit()
        result = True

    return result

def create_student(full_name: str, email: str, grade: str = None) -> Student:
    """Yangi talaba ro'yxatdan o'tkazish"""
    student = Student(
        full_name = full_name,
        email = email,
        grade = grade
    )

    with get_db() as session:
        session.add(student)
        session.commit()
    
    return student

def get_student_by_id(student_id: int) -> Student | None:
    """ID bo'yicha talabani olish"""
    with get_db() as session:
        student = session.query(Student).get(student_id)
    
    return student

def get_all_students() -> list[Student]:
    """Barcha talabalar ro'yxatini olish"""
    with get_db() as session:
        students = session.query(Student).all()
    
    return students

def update_student_grade(student_id: int, grade: str) -> Student | None:
    """Talaba sinfini yangilash"""
    student = get_student_by_id(student_id)
    result = False

    if student:
        with get_db() as session:
            grade = grade if grade else student.grade
            
            session.add(student)
            session.commit()
        result = True

    return result

def borrow_book(student_id: int, book_id: int) -> Borrow | None:
    """
    Talabaga kitob berish
    
    Quyidagilarni tekshirish kerak:
    1. Student va Book mavjudligini
    2. Kitobning is_available=True ekanligini
    3. Talabada 3 tadan ortiq qaytarilmagan kitob yo'qligini yani 3 tagacha kitob borrow qila oladi
    
    Transaction ichida:
    - Borrow yozuvi yaratish
    - Book.is_available = False qilish
    - due_date ni hisoblash (14 kun)
    
    Returns:
        Borrow object yoki None (xatolik bo'lsa)
    """
    with get_db() as session:
        student = session.query(Student).get(student_id)
        book = session.query(Book).get(book_id)
        
        # 1-shart
        if not student or not book:
            return None
        
        # 2-shart
        if not book.is_available:
            return None
        
        # 3-shart
        active_borrows = session.query(Borrow).filter(
                Borrow.student_id == student_id,
                Borrow.returned_at == None
            ).count()

        if active_borrows >= 3:
            return None
        
        # Barcha shartlardan o'tsa Borrow yaratamiz
        borrow = Borrow(
                student_id=student_id,
                book_id=book_id,
                borrowed_at=datetime.now(),
                due_date=datetime.now() + timedelta(days=14)
            )

        # Borrow qilinsa  u endi bizda yo'q False qilamiz
        book.is_available = False

        session.add(borrow)
        session.commit()

    return Borrow

def return_book(borrow_id: int) -> bool:
    """
    Kitobni qaytarish
    
    Transaction ichida:
    - Borrow.returned_at ni to'ldirish
    - Book.is_available = True qilish
    
    Returns:
        True (muvaffaqiyatli) yoki False (xatolik)
    """
    with get_db() as session:
        borrow = session.query(Borrow).get(borrow_id)
        # borrow chiqmasa false
        if not borrow:
            return False
        
        # book chiqmasa false
        book = session.query(Book).get(borrow.book_id)
        if not book:
            return False

        # ikkalasi ham true bo'ldi, available qilamiz
        borrow.returned_at = datetime.now()
        book.is_available = True

        session.commit()

    return True

def get_student_borrow_count(student_id: int) -> int:
    """Talabaning jami olgan kitoblari soni"""
    with get_db() as session:
        count = session.query(Borrow).filter(Borrow.student_id == student_id).count()
    return count

def get_currently_borrowed_books() -> list[tuple[Book, Student, datetime]]:
    """Hozirda band bo'lgan kitoblar va ularni olgan talabalar"""
    with get_db() as session:
        # hozirda band bo'lganligi uchun return None bo'lgalarini olamiz(ya'ni qaytarilmagan)
        borrows = session.query(Borrow).filter(Borrow.returned_at == None).all()
        result = []
        for b in borrows:
            book = session.query(Book).get(b.book_id)
            student = session.query(Student).get(b.student_id)
            result.append((book, student, b.borrowed_at))
    return result

def get_books_by_author(author_id: int) -> list[Book]:
    """Muayyan muallifning barcha kitoblari"""
    with get_db() as session:
        books = session.query(Book).filter(Book.author_id == author_id).all()

    return books

def get_overdue_borrows() -> list[tuple[Borrow, Student, Book, int]]:
    """
    Kechikkan kitoblar ro'yxati
    
    Returns:
        List of tuples: (Borrow, Student, Book, kechikkan_kunlar)
        faqat returned_at=NULL va due_date o'tgan yozuvlar
    """
    with get_db() as session:
        # shartlarni tekshiramiz: faqat returned_at=NULL(bu .py da NONE) va due_date o'tgan yozuvlar 
        borrows = session.query(Borrow).filter(
            Borrow.returned_at.is_(None),
            Borrow.due_date < datetime.now()
        ).all()

        result = []
        for b in borrows:
            student = session.query(Student).get(b.student_id)
            book = session.query(Book).get(b.book_id)
            over_due_days = (datetime.now() - b.due_date).days
            result.append((b, student, book, over_due_days))

    return result