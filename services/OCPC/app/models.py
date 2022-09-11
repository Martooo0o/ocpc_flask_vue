from . import db
# from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_serialize import FlaskSerialize

fs_mixin = FlaskSerialize(db)

class User(db.Model, fs_mixin):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    # name = db.Column(db.String(1000))
    logs = db.relationship('Log', backref='user', lazy=True)

    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            # flash('Please check your login details and try again.')
            print("No user found>")
            return None

        # if the above check passes, then we know the user has the right credentials
        # login_user(user, remember=True)
        return user

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    filename = db.Column(db.String(200))

    cubes = db.relationship('Cube', backref='log', lazy=True)

class Cube(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey('log.id'), nullable=False)
    name = db.Column(db.String(200))
    dimens = db.Column(db.String())  # this is a stringified dict of the form obj_type/event_tyoe: list_sel_dimens
    analyses = db.relationship('Analysis', backref='cube', lazy=True)
    freq_all = db.Column(db.String)
    freq_existence = db.Column(db.String)

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cube_id = db.Column(db.Integer, db.ForeignKey('cube.id'), nullable=False)
    name = db.Column(db.String(200))
    filters = db.Column(db.String())
    visualisations = db.Column(db.String())
    # type = db.Column(db.String())
    # the list contains id's of analyses which this comparison holds
    # list = db.Column(db.String())
