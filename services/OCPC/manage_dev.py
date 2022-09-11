from flask.cli import FlaskGroup, with_appcontext

from app import create_app, db
import sys
import click

my_app = create_app(None)
application = my_app
cli = FlaskGroup(create_app=create_app)

@my_app.cli.command("create_db")
@with_appcontext
def create_db():
    print("CREATING DB")
    db.drop_all()
    db.create_all()
    db.session.commit()

# @cli.command("seed_db")
# def seed_db():
#     db.session.add(User(email="michael@mherman.org"))
#     db.session.commit()

if __name__ == "__main__":
    cli()
