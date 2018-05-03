import pytest, requests
from app import create_app


@pytest.fixture(scope='module')
def app():
    app = create_app()
    # app.run()
    return app
