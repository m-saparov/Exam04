# test.py
from datetime import date
from library.services import (
    create_author, get_author_by_id, get_all_authors, update_author, delete_author,
    create_book, get_book_by_id, get_all_books, search_books_by_title, delete_book,
    create_student, get_student_by_id, get_all_students, update_student_grade,
    Base, engine
)


def init_db():
    Base.metadata.create_all(engine)


# Ma'lumotlar bazasini bir marta ishga tushirish (jadval yaratish)
print("Ma'lumotlar bazasi ishga tushirilmoqda...")

init_db()

print("Jadvallar muvaffaqiyatli yaratildi!\n")

print()
print("1. YANGI MUALLIF QO'SHISH")
print()
create_author(name="Alisher Navoiy", bio="Buyuk o'zbek shoiri va mutafakkiri")
create_author(name="Chingiz Aytmatov", bio="Qirg'iz yozuvchisi, 'Jamila' asari muallifi")
create_author(name="Abdulla Qodiriy", bio="O'zbek adabiyotining asoschilaridan")
print("3 ta muallif qo'shildi.\n")

print()
print("2. BARCHA MUALLIFLARNI KO'RSATISH")
print()
authors = get_all_authors()
for author in authors:
    print(f"ID: {author.id} | Ism: {author.name} | Bio: {author.bio}")
print(f"Jami mualliflar soni: {len(authors)}\n")

print()
print("3. MUALLIF MA'LUMOTLARINI YANGILASH (ID=2)")
print()
update_author(author_id=2, name="Chingiz Aytmatov (yangilandi)", bio="Qirg'izistonlik mashhur yozuvchi")
updated_author = get_author_by_id(2)
print(f"Yangilangan muallif → {updated_author}\n")


print()
print("4. YANGI KITOBLAR QO'SHISH")
print()
create_book(title="O'tkan kunlar", author_id=3, published_year=1925, isbn="978-9943-12-345-6")
create_book(title="Jamila", author_id=2, published_year=1960, isbn="978-5-17-098765-4")
create_book(title="Alpomish", author_id=1, published_year=2020, isbn="978-9943-88-123-4")
create_book(title="Mehrobdan chayon", author_id=3, published_year=1936, isbn="978-9943-45-678-9")
print("4 ta kitob muvaffaqiyatli qo'shildi.\n")

print()
print("5. BITTA KITOBNI ID BO'YICHA OLISH (ID=1)")
print()
book = get_book_by_id(book_id=1)
if book:
    print(f"Topildi → ID: {book.id} | Sarlavha: {book.title} | Muallif ID: {book.author_id} | Yil: {book.published_year}")
else:
    print("Kitob topilmadi!\n")

print()
print("6. BARCHA KITOBLAR RO'YXATI")
print()
books = get_all_books()
for b in books:
    print(f"ID: {b.id} | {b.title} | Muallif ID: {b.author_id} | {b.published_year} | ISBN: {b.isbn}")
print(f"Jami kitoblar soni: {len(books)}\n")

print()
print("7. SARLAVHA BO'YICHA QIDIRISH ('kun' so'zi bor kitoblar)")
print()
searched = search_books_by_title(title="kun")
for b in searched:
    print(f"→ {b.title} (ID: {b.id})")
print()


print()
print("8. YANGI TALABALAR QO'SHISH")
print()
create_student(full_name="Aliyev Vali", email="vali2005@mail.ru", grade="A")
create_student(full_name="Karimova Madina", email="madina.k@mail.ru", grade="B+")
create_student(full_name="Olimov Sardor", email="sardor_03@gmail.com")
print("3 ta talaba qo'shildi.\n")

students = get_all_students()
for s in students:
    print(f"ID: {s.id} | {s.full_name} | {s.email} | Baho: {s.grade or 'Hali baholanmagan'} | Ro'yxatdan o'tgan: {s.created_at}")
print()

# Talaba gradeni yangilash
update_student_grade(student_id=3, grade="A+")
updated_student = get_student_by_id(3)
print(f"Yangilangan talaba: {updated_student.full_name}, yangi baho: {updated_student.grade}\n")

print("\n\n")

# Kitob o'chirish - ID yo'q bo'lsa else ishlaydi)

# 1
if delete_book(book_id=99):
    print("Kitob o'chirildi")
else:
    print("Kitob topilmadi")

#2
if delete_book(book_id=4):
    print("Kitob muvaffaqiyatli o'chirildi\n")
else:
    print("Xatolik yuz berdi\n")

# Muallif o'chirish - Bunda agar muallifga kitob bog'langan Error berayabdi!
if delete_author(author_id=10):
    print("Muallif o'chirildi")
else:
    print("Bunday muallif yo'q yoki unga kitoblar bog'langan")


print("\n\nTugadi!")