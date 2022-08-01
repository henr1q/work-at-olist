from flask import Blueprint, request, redirect, url_for, render_template, jsonify, json, Response
from flask_api.models import Authors, Books, get_all_authors, get_single_author, get_all_books, db, get_author_by_id, \
    get_book_by_arg
from sqlalchemy.exc import IntegrityError


api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/', methods=['GET'])
def index():
    # TODO: fix this
    return {"Docs": "https://github.com/henr1q/work-at-olist"}


@api_bp.route('/authors', methods=['GET'])
def get_authors():
    """ Endpoint to get the authors data """

    # Get parameter args
    name = request.args.get('name')
    page = request.args.get('page', 1, type=int)  # if page is not passed then page = 1
    output_authors = {}

    try:
        data = get_all_authors(page)
    except:
        response = Response('{"Error": "No data found"}', 404, mimetype='application/json')
        return response

    # If paged is not valid, return a 404
    if page > data['pages']['total_pages'] or page <= 0:
        response = Response('{"Error": "Page not found"}', 404, mimetype='application/json')
        return response

    # If: name filter is passed, return the author query. Else: return all authors
    if name:
        name = name.title()
        try:
            author = get_single_author(name)
            response = {author.id: author.name}
            return response
        except:
            response = Response('{"Error": "Author not found"}', 404, mimetype='application/json')
            return response
    else:
        for author in data['authors']:
            output_authors[author.id] = author.name

        response = {"pages": data['pages'], "authors": output_authors}
        return response


@api_bp.route('/books', methods=['GET'])
def get_books():
    """ Endpoint to get all books data """

    # Get parameter args
    page = request.args.get('page', 1, type=int)
    data = get_all_books(page)
    output_books = []

    # Dict of all filters
    all_args = dict(book_name=request.args.get('name', '').strip('"').title(),
                       book_authors=request.args.get('author', '').strip('"').strip('[').strip(']').title(),
                       book_year=request.args.get('year'),
                       book_edition=request.args.get('edition'))

    # Dict of passed filters
    valid_args = {k: v for k, v in all_args.items() if v}

    # If filters: return the filtered books. Else: return all books
    if valid_args:
        result = get_book_by_arg(**valid_args)
        # If query is found: return the books result. Else: return 404
        if result:
            for book in result:
                book_info = {"id": book.id, "name": book.name, "edition": book.edition,
                             "publication_year": book.publication_year,
                             "authors": book.authors}

                output_books.append(book_info)

            response = {'books': output_books}
            return response
        else:
            response = Response('{"Error": "Books not found"}', 404, mimetype='application/json')
            return response

    # Check if page is valid
    if page > data['pages']['total_pages'] or page <= 0:
        response = Response('{"Error": "Page not found"}', 404, mimetype='application/json')
        return response

    # Get all books data
    for book in data['books']:
        book_info = {"id": book.id, "name": book.name, "edition": book.edition,
                     "publication_year": book.publication_year,
                     "authors": book.authors}

        output_books.append(book_info)

    # Return all books data if filters was not passed
    page_info = data['pages']
    response = {"pages": page_info, "books": output_books}
    return response


@api_bp.route('/books', methods=['POST'])
def add_books():
    """ Endpoint to add books to database. """

    request_data = request.get_json()
    try:
        # Get the authors by the ids passed in json POST.
        authors_name = [get_author_by_id(int(author_id)) for author_id in request_data['authors']]

        # Check if the authors IDs was valid ids
        if authors_name == [None]:
            response = Response('{"Error": "Author ID not found"}', 400, mimetype='application/json')
            return response

        # Insert book in the database
        authors_data = ', '.join(authors_name)
        new_book = Books(name=request_data['name'].title(), edition=request_data['edition'],
                         publication_year=request_data['publication_year'], authors=authors_data)
        db.session.add(new_book)
        db.session.commit()

        response = Response('{"Success": "Book added"}', 201, mimetype='application/json')
        return response
    except IntegrityError:
        response = Response('{"Error": "Book already in database"}', 400, mimetype='application/json')
        return response
    except:
        response = Response('{"Error": "Bad request"}', 400, mimetype='application/json')
        return response


@api_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_books(book_id):
    """ Endpoint to update books from database. """

    # Get the object to update from the URL id
    book = db.session.query(Books).get(book_id)
    request_data = request.get_json()

    # Check if book exists in database
    if not book:
        response = Response('{"Error": "Book not in database"}', 400, mimetype='application/json')
        return response

    # Get the authors by the ids passed, same as in the create function
    if request_data.get('authors'):
        authors_name = [get_author_by_id(int(author_id)) for author_id in request_data['authors']]
        authors_data = ', '.join(authors_name)
        request_data['authors'] = authors_data

    # Update the fields passed in the json
    for field, value in request_data.items():
        if value:
            setattr(book, field, value)

    db.session.commit()
    response = Response('{"Success": "Book edited"}', 200, mimetype='application/json')
    return response



@api_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_books(book_id):
    """ Endpoint to remove books from database. """

    # Get the object to update from the URL id
    book = db.session.query(Books).get(book_id)

    # Check if book exists in database
    if not book:
        response = Response('{"Error": "Book not in database"}', 400, mimetype='application/json')
        return response

    # Delete the book
    try:
        db.session.delete(book)
        db.session.commit()
        response = Response('{"Success": "Book deleted"}', 200, mimetype='application/json')
        return response
    except:
        response = Response('{"Error": "Book not deleted"}', 404, mimetype='application/json')
        return response







