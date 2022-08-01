import click
from flask import Blueprint
from flask_api.models import db
import csv
from flask_api.models import Authors, Books


cli = Blueprint('db', __name__)


@cli.cli.command('create_db')
def create():
    """ Creates the database """
    db.create_all()
    print('Database created')


@cli.cli.command('reset_db')
def reset():
    """ Delete the current database and recreate """
    db.drop_all()
    db.session.commit()
    db.create_all()
    print('Database recreated')


@cli.cli.command('import_authors')
@click.argument('file')
def import_authors(file):
    """ Import csv file to database """
    with open(f'{file}', newline='') as f:
        reader = csv.reader(f)
        next(reader, None)
        data = [Authors(name=item[0].title()) for item in reader]

    if data:
        db.session.bulk_save_objects(data)
        db.session.commit()
        print(f'{len(data)} objects imported to database')
    else:
        print('Error, data to import is empty')




