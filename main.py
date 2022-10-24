from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from passlib.hash import argon2
from sqlalchemy import Date

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:10082009@localhost:3306/lab6'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


'''
///////////////////
///////////////////
/////User model////
///////////////////
///////////////////
'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    firstName = db.Column(db.String(120), nullable=False)
    lastName = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    calendar_id = db.Column(db.Integer, db.ForeignKey("calendar.id")),


    def add_to(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def user_list(cls):
        def to_json(user):
            return {
                'id': user.id,
                'username': user.username,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'password': user.password,
                'phone': user.phone
            }

        return {'users': [to_json(user) for user in User.query.all()]}

    @staticmethod
    def generate_hash(password):
        return argon2.hash(password)

    @staticmethod
    def verify_hash(password, hash_):
        return argon2.verify(password, hash_)




'''
///////////////////
///////////////////
//Calendar model///
///////////////////
///////////////////
'''
class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(Date, nullable=False)
    event = db.relationship("event")
    user = db.relationship("user", backref="calendar", uselist=False)

    def add_to(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


'''
///////////////////
///////////////////
/////AC table//////
///////////////////
///////////////////
'''
association_table = db.Table(
    "user_to_event",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("event_id", db.Integer, db.ForeignKey("event.id")),
)



'''
///////////////////
///////////////////
////Event model////
///////////////////
///////////////////
'''
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    calendar_id = db.Column(db.Integer, db.ForeignKey("calendar.id"))
    user = db.relationship("event",
                           secondary=association_table
                           )

    def add_to(self):
        db.session.add(self)
        db.session.commit()



'''
///////////////////
///////////////////
////First route////
///////////////////
///////////////////
'''
@app.route('/api/v1/hello-world-18/', methods=['GET'])
def index():
    return 'Hello World 18'



'''
///////////////////
///////////////////
example of create tb
///////////////////
///////////////////
'''
@app.before_request
def init_database():
    db.drop_all()
    db.create_all()
    db.session.commit()




'''
///////////////////
///////////////////
///////main////////
///////////////////
///////////////////
'''
if __name__ == '__main__':
    # serve(app, host='127.0.0.1', port=80)
    app.run()
