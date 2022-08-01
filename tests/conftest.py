import pytest


@pytest.fixture(scope='module')
def app():
    """ Flask app instance """
    from flask_api import create_app
    app = create_app()
    app.config.from_object('config.TestConfig')

    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()