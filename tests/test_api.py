def test_db_create(runner):
    """ Test if database is creating """

    result = runner.invoke(args=["db", "create_db"])
    assert 'Database created' in result.output


def test_db_import(runner):
    """ Test if database is importing file.csv """

    result = runner.invoke(args=["db", "import_authors", "authors.csv"])
    assert 'objects imported to database' in result.output


def test_app_is_created(app):
    """ Test if app is created """
    assert app.name == 'flask_api'


def test_index(client):
    """ Test if index page is up """

    response = client.get("/")
    assert response.status == '200 OK'


def test_get_authors(client, app):
    """ Test if authors page is up """

    response = client.get("/authors")
    assert response.status == '200 OK'


def test_create_books(client, app):
    """ Test API book creating """

    book_data = {
        "name": 'Test Book',
        "edition": 1111,
        "publication_year": 1234,
        "authors": [1]
    }

    response = client.post('http://127.0.0.1:5000/books', json=book_data)
    assert response.status == '201 CREATED' and response.json == {"Success": "Book added"}


def test_read_books(client, app):
    """ Test API book reading """
    response = client.get("/books")
    assert response.status == '200 OK' and "Test Book" in response.text


def test_update_books(client, app):
    """ Test API book updating """

    book_id = 1
    new_data = {"edition": 2222}
    response = client.put(f'http://127.0.0.1:5000/books/{book_id}', json=new_data)

    assert response.status == '200 OK' and response.json == {"Success": "Book edited"}

def test_delete_books(client, app):
    """ Test API book delete """

    book_id = 1
    response = client.delete(f'http://127.0.0.1:5000/books/{book_id}')

    assert response.status == '200 OK' and response.json == {"Success": "Book deleted"}
