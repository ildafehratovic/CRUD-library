from sqlmodel import SQLModel, Field, create_engine, Session, select
# gt - >, ge - >=, lt- <, le- <=, max_lenght, min_lenght
class Book(SQLModel, table=True):
    id: int |  None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=30)
    zanr: str
    no_pages: int = Field(default=10, ge=0)
    rating: float = Field(default=5.0)#opcioni podatak
    in_stock: bool = Field(default=True)

engine = create_engine("sqlite:///books.db")
SQLModel.metadata.create_all(engine)

def create_book(title:str, zanr: str, no_pages:int, rating:float, in_stock:bool ):
    with Session(engine) as session:
        book = Book(title=title, zanr=zanr,no_pages=no_pages, rating=rating, in_stock= in_stock)
        session.add(book)
        session.commit()
        session.refresh(book)
        print(f"Created new book no{book.id} in database")

def list_books():
    with Session (engine) as session:
        statement = select(Book)
        books = session.exec(statement).all()
        if not books:
            print("No books")
        for book in books:
            print(f"{book.title}: \n{book.zanr},\n{book.no_pages}, \n{book.rating}, \n{book.in_stock} ")

def read_book(book_id: int):
    with Session(engine) as session:
        statement= select(Book).where(Book.id == book_id)
        book = session.exec(statement).first()
        print(f"{book.title}: \n{book.zanr},\n{book.no_pages}, \n{book.rating}, \n{book.in_stock} ")

def page_filter(num_pages:int):
    with Session (engine) as session:
        statement = select(Book).where(Book.no_pages < num_pages)
        books = session.exec(statement).all()
        return books

def delete_book(book_title: str):
    with Session(engine) as session:
        statement = select(Book).where(Book.title== book_title)
        book = session.exec(statement).first()
        if not book:
            print("No books")
            return
        session.delete(book)
        session.commit()
        print(f"Deleted book {book_title}")

def edit_book(title:str, new_no_pages:str|None=None, new_zanr: str|None=None, new_rating: float|None=None, new_in_stock: bool|None=None):
    with Session(engine) as session:
        statement = select(Book).where(Book.title==title)
        book=session.exec(statement).first()
        if book:
            if title!=None:
                print("Title is changed")
            if new_no_pages !=None:
                print("Number of pages is changed")
            if new_zanr != None:
                print("Zanr is changed")
            if new_rating !=None:
                print("Rating is changed")
            if new_in_stock != None:
                print("In stock is changed")
            session.add(book)
            session.commit()
            return book
        else:
            print("Book is not found!")

edit_book(title="Novi Naslov")

list_books()
# create_book(title="Rat i mir", zanr="classik", no_pages=1200, rating=4.7, in_stock=True)

