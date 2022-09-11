import pytest,sys
from flask import g
from flask import session

# from flaskr.db import get_db

# def test_login_logout(client):
#     """Make sure login and logout works."""
#
#     rv = login(client, flaskr.app.config['USERNAME'], flaskr.app.config['PASSWORD'])
#     assert b'You were logged in' in rv.data
#
#     rv = logout(client)
#     assert b'You were logged out' in rv.data
#
#     rv = login(client, flaskr.app.config['USERNAME'] + 'x', flaskr.app.config['PASSWORD'])
#     assert b'Invalid username' in rv.data
#
#     rv = login(client, flaskr.app.config['USERNAME'], flaskr.app.config['PASSWORD'] + 'x')
#     assert b'Invalid password' in rv.data


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("a", "", b"Password is required."),
        ("test", "test", b"already registered"),
    ),
)
def test_register(client, username, password):
    # test that viewing the page renders without template errors
    # assert client.get("/auth/signup").status_code == 200

    # test that successful registration redirects to the login page
    response = client.post("/auth/signup", data={"username": "a", "password": "a"})
    # assert "http://localhost/auth/login" == response.headers["Location"]
    print(response)
    # test that the user was inserted into the database
    # with app.app_context():
    #     assert (
    #             get_db().execute("select * from user where username = 'a'").fetchone()
    #             is not None
    #     )

# def login(client, username, password):
#     return client.post('/auth/login', data=dict(
#         username=username,
#         password=password
#     ), follow_redirects=True)

# def test_empty_db(client):
#     """Start with a blank database."""

#     rv = client.get('/')
#     assert b'No entries here so far' in rv.data

if __name__ == '__main__':
    pytest.main([sys.argv[0], '-vvv',])
    exit(0)