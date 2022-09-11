import pytest
import sys
import os
myDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.split(myDir)[0]
if(sys.path.__contains__(parentDir)):
    print('parent already in path')
    pass
else:
    print('parent directory added')
    sys.path.append(parentDir)

from app import create_app, create_db
from app import db

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here
    with app.app_context():
        db.create_all()

    yield app

    # clean up / reset resources here
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

if __name__ == '__main__':
    pytest.main([sys.argv[0], '-vvv',])
    exit(0)