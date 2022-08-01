from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, not_

db = SQLAlchemy()


class Authors(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "Authors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)


class Books(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "Books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    authors = db.Column(db.String(250), nullable=False)
    edition = db.Column(db.Integer(), nullable=False)
    publication_year = db.Column(db.SmallInteger(), nullable=False)


def get_all_authors(page):
    per_page = 100

    authors_query = Authors.query.paginate(page=page, per_page=per_page, error_out=False)
    all_authors = authors_query.items
    total_pages = authors_query.pages
    total_results = authors_query.total

    if total_pages == 0:
        total_pages = 1

    result = {'pages': {'current_page': page, 'max_authors_per_page': per_page,
                        'total_pages': total_pages, 'total_authors': total_results},
              'authors': all_authors}

    return result


def get_single_author(name):
    author = Authors.query.filter_by(name=name).first()
    return author


def get_author_by_id(author_id):
    author = db.session.query(Authors).get(author_id)
    if author:
        return author.name


def get_all_books(page):
    per_page = 100

    books_query = Books.query.paginate(page=page, per_page=100, error_out=False)
    all_books = books_query.items
    total_books = books_query.total
    total_pages = books_query.pages

    if total_pages == 0:
        total_pages = 1

    result = {'pages': {'current_page': page, 'max_books_per_page': per_page,
                        'total_pages': total_pages, 'total_books': total_books},
              'books': all_books}

    return result


def get_book_by_arg(book_name='', book_authors='', book_edition=None, book_year=None):

    all_args = {
        'name': book_name.title(),
        'author': book_authors,
        'year': book_year,
        'edition': book_edition
    }

    all_queries = {
        'name': Books.name == book_name,
        'author': Books.authors.contains(book_authors),
        'year': Books.publication_year == book_year,
        'edition': Books.edition == book_edition
    }

    valid_args = {arg: value for arg,value in all_args.items() if value}
    valid_queries = {arg:query for arg, query in all_queries.items() if arg in valid_args.keys()}
    filters = [valid_queries[k] for k, v in valid_queries.items()]


    results = db.session.query(Books).filter(and_(*filters)).all()

    return results


def get_book_by_id(book_id):
    book = db.session.query(Authors).get(book_id)
    if book:
        return book

