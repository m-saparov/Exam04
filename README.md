# Python va Database - Final Exam

## Imtihon haqida umumiy ma'lumot

**Davomiyligi:** 6 soat  
**Maksimal ball:** 100  
**O'tish bali:** 60  
**Texnologiyalar:** Python 3.10+, SQLAlchemy 2.0+, PostgreSQL, psycopg2

---

## Imtihon maqsadi

Ushbu imtihonda siz kutubxona tizimini (Library Management System) SQLAlchemy ORM yordamida loyihalashtirish va amalga oshirishingiz kerak. Siz quyidagi ko'nikmalarni namoyish etishingiz talab qilinadi:

- Relational database modellarini loyihalash
- SQLAlchemy ORM orqali CRUD operatsiyalarini bajarish
- Foreign key va relationship'larni to'g'ri qo'llash
- Murakkab query'lar yozish

**Muhim:** CLI yoki xech qanday interfeys yaratish talab qilinmaydi. Barcha funksiyalar oddiy Python funksiyalari sifatida yozilishi kerak.

---

## Vazifa 1: Database Modellari (25 ball)

Quyidagi to'rtta model yaratishingiz kerak:

- Auther
- Book
- Student
- Borrow

### 1.1 Author modeli (6 ball)
- `id` - Integer, primary key, auto increment
- `name` - String(100), null bo'lmasligi shart
- `bio` - Text, ixtiyoriy (nullable)
- `created_at` - DateTime, avtomatik yaratilish vaqti

**Relationship:** Har bir muallif ko'plab kitoblarga ega bo'lishi mumkin (one-to-many)

### 1.2 Book modeli (7 ball)
- `id` - Integer, primary key, auto increment
- `title` - String(200), null bo'lmasligi shart
- `author_id` - Integer, foreign key (Author jadvaliga)
- `published_year` - Integer
- `isbn` - String(13), unique, ixtiyoriy
- `is_available` - Boolean, default=True
- `created_at` - DateTime, avtomatik yaratilish vaqti
- `updated_at` - DateTime, avtomatik yaratilish vaqti

**Relationship:** Har bir kitob bitta muallifga tegishli (many-to-one), ko'plab Borrow yozuvlariga ega bo'lishi mumkin (one-to-many)

### 1.3 Student modeli (6 ball)
- `id` - Integer, primary key, auto increment
- `full_name` - String(150), null bo'lmasligi shart
- `email` - String(100), unique, null bo'lmasligi shart
- `grade` - String(20), ixtiyoriy
- `registered_at` - DateTime, avtomatik ro'yxatdan o'tish vaqti

**Relationship:** Har bir talaba ko'plab Borrow yozuvlariga ega bo'lishi mumkin (one-to-many)

### 1.4 Borrow modeli (6 ball)
- `id` - Integer, primary key, auto increment
- `student_id` - Integer, foreign key (Student jadvaliga)
- `book_id` - Integer, foreign key (Book jadvaliga)
- `borrowed_at` - DateTime, kitob olingan vaqt avtomatik
- `due_date` - DateTime, qaytarish muddati (default: borrowed_at + 14 kun)
- `returned_at` - DateTime, nullable, kitob qaytarilgan vaqt

**Relationship:** Har bir Borrow yozuvi bitta talaba va bitta kitobga tegishli (many-to-one)

**Baholash mezoni:**
- Barcha fieldlar to'g'ri turda e'lon qilingan: 15 ball
- Foreign key'lar to'g'ri o'rnatilgan: 5 ball
- Relationship'lar to'g'ri konfiguratsiya qilingan: 5 ball

---

## Vazifa 2: CRUD Operatsiyalari (35 ball)

### 2.1 Author CRUD (10 ball)

Quyidagi funksiyalarni yozing:

```python
def create_author(name: str, bio: str = None) -> Author:
    """Yangi muallif yaratish"""
    pass

def get_author_by_id(author_id: int) -> Author | None:
    """ID bo'yicha muallifni olish"""
    pass

def get_all_authors() -> list[Author]:
    """Barcha mualliflar ro'yxatini olish"""
    pass

def update_author(author_id: int, name: str = None, bio: str = None) -> Author | None:
    """Muallif ma'lumotlarini yangilash"""
    pass

def delete_author(author_id: int) -> bool:
    """Muallifni o'chirish (faqat kitoblari bo'lmagan holda)"""
    pass
```

### 2.2 Book CRUD (10 ball)

```python
def create_book(title: str, author_id: int, published_year: int, isbn: str = None) -> Book:
    """Yangi kitob yaratish"""
    pass

def get_book_by_id(book_id: int) -> Book | None:
    """ID bo'yicha kitobni olish"""
    pass

def get_all_books() -> list[Book]:
    """Barcha kitoblar ro'yxatini olish"""
    pass

def search_books_by_title(title: str) -> list[Book]:
    """Kitoblarni sarlavha bo'yicha qidirish (partial match)"""
    pass

def delete_book(book_id: int) -> bool:
    """Kitobni o'chirish"""
    pass
```

### 2.3 Student CRUD (8 ball)

```python
def create_student(full_name: str, email: str, grade: str = None) -> Student:
    """Yangi talaba ro'yxatdan o'tkazish"""
    pass

def get_student_by_id(student_id: int) -> Student | None:
    """ID bo'yicha talabani olish"""
    pass

def get_all_students() -> list[Student]:
    """Barcha talabalar ro'yxatini olish"""
    pass

def update_student_grade(student_id: int, grade: str) -> Student | None:
    """Talaba sinfini yangilash"""
    pass
```

### 2.4 Validation va Error Handling (7 ball)

Barcha CRUD funksiyalarda quyidagilar amalga oshirilishi kerak:
- Mavjud bo'lmagan ID'lar uchun None qaytarish
- Unique constraint buzilganda mos xatolik qaytarish

---

## Vazifa 3: Borrow/Return Logic (25 ball)

### 3.1 Kitob olish funksiyasi (13 ball)

```python
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
    pass
```

### 3.2 Kitob qaytarish funksiyasi (12 ball)

```python
def return_book(borrow_id: int) -> bool:
    """
    Kitobni qaytarish
    
    Transaction ichida:
    - Borrow.returned_at ni to'ldirish
    - Book.is_available = True qilish
    
    Returns:
        True (muvaffaqiyatli) yoki False (xatolik)
    """
    pass
```

---

## Vazifa 4: Qo'shimcha Query'lar (15 ball)

### 4.1 Statistika funksiyalari (8 ball)

```python
def get_student_borrow_count(student_id: int) -> int:
    """Talabaning jami olgan kitoblari soni"""
    pass

def get_currently_borrowed_books() -> list[tuple[Book, Student, datetime]]:
    """Hozirda band bo'lgan kitoblar va ularni olgan talabalar"""
    pass

def get_books_by_author(author_id: int) -> list[Book]:
    """Muayyan muallifning barcha kitoblari"""
    pass
```

### 4.2 Kechikkan kitoblar (7 ball)

```python
def get_overdue_borrows() -> list[tuple[Borrow, Student, Book, int]]:
    """
    Kechikkan kitoblar ro'yxati
    
    Returns:
        List of tuples: (Borrow, Student, Book, kechikkan_kunlar)
        faqat returned_at=NULL va due_date o'tgan yozuvlar
    """
    pass
```

---

## Topshirish formati

Quyidagi fayl strukturasini yarating:

```
library/
    __init__.py
    config.py      # env uchun
    db.py          # db settings uchun
    models.py      # modelslar uchun
    services.py    # barcha db services uchun
test.py # har bir db services ni test qilib koring
.gitignore
.env
.env.sample
requirements.txt
```

---

## Baholash mezonlari

| Bo'lim | Ball | Tavsif |
|--------|------|--------|
| Modellar | 25 | To'g'ri struktura, relationship'lar |
| CRUD | 35 | Barcha operatsiyalar to'liq va xatosiz |
| Borrow/Return | 25 | Transaction, validation, logic |
| Query'lar | 15 | Murakkab so'rovlar, optimization |
| **JAMI** | **100** | |

---

## Muhim eslatmalar

1. **Plagiarism:** Kodning 100% o'zingiz tomondan yozilganligi tekshiriladi
2. **Deadline:** Belgilangan vaqtdan oshib ketishga yo'l qo'yilmaydi
3. **Kod sifati:** Ishlayotgan kod yetarli emas, kod toza va tushunarli bo'lishi kerak
4. **Izohlar:** Murakkab logikalarni izohlab yozing

---

## Tavsiya etiladigan resurslar

- SQLAlchemy 2.0 Documentation
- Python Documentation
- Darslar davomidagi example lar

---

**Omad tilaymiz!**

*Savollar bo'lsa, imtihon boshlanishidan oldin so'rashingiz mumkin.*
