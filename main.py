from sqlmodel import SQLModel, Field, create_engine, Session, select

class Book(SQLModel, table=True):
    id: int |  None = Field(default=None, primary_key=True)
    title: str
    zanr: str
    no_pages: int = Field(default=0)
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



list_books()
# create_book(title="Rat i mir", zanr="classik", no_pages=1200, rating=4.7, in_stock=True)

