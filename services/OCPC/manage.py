from flask.cli import FlaskGroup

# from app import db
from app import create_app
import sys



my_app = create_app(None)
application = my_app
from app import db
# my_app.application = app
cli = FlaskGroup(create_app=create_app)
sys.path.insert(0,"/usr/src/app/app")

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# @cli.command("seed_db")
# def seed_db():
#     db.session.add(User(email="michael@mherman.org"))
#     db.session.commit()

if __name__ == "__main__":
    cli()
