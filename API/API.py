from crypt import methods
from datetime import datetime
from locale import format_string
from unicodedata import name
from urllib.request import url2pathname
from flask import Flask, jsonify, redirect, render_template, request, session, url_for, abort
from sqlalchemy import cast, String
from flask_sqlalchemy import SQLAlchemy
from mysqlx import Session
from flask_session import Session
from html5lib import serialize
from itsdangerous import Serializer
from marshmallow import Schema, fields
from datetime import datetime, timedelta
from sqlalchemy.sql import func
from sqlalchemy import and_, desc
from flask_migrate import Migrate
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
import threading
import json
import requests
import time

app = Flask(__name__)

# database user:password@hostname/database name

app.config["SESSION_PERMANENT"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://james:foxtrot09er@localhost/penzi'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes = 30)
app.config["SECRET_KEY"] = 'jisungparkfromdeep'
app.config["SESSION_TYPE"] = 'sqlalchemy'


db = SQLAlchemy(app)
admin = Admin(app, name="Admin Portal", template_mode="bootstrap3")


app.config["SESSION_TYPE"] = db
sess = Session()


migrate = Migrate(app, db)


class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        
        else:
            abort(403)

class NotificationsViews(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/notify.html")

class LogoutViews(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/logout.html")

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    number = db.Column(db.String(13), unique = True, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    county = db.Column(db.String(60), nullable=False)
    town = db.Column(db.String(60), nullable=False)
    education_level = db.Column(db.String(50), nullable=True)
    profession = db.Column(db.String(60), nullable=True)
    marital_status = db.Column(db.String(50), nullable=True)
    religion = db.Column(db.String(50), nullable=True)
    tribe = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=True)
    time_of_registry = db.Column(db.DateTime(timezone=True),
                         nullable=False, server_default=func.now())


    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_age(cls, age):
        return cls.query.filter_by(age=age).first()

    @classmethod
    def get_by_number(cls, number):
        return cls.query.filter_by(number=number).first()

    @classmethod
    def filter_by_age(cls, age, county):
        return cls.query.filter_by()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    age = fields.Integer()
    gender = fields.String()
    county = fields.String()
    town = fields.String()
    education_level = fields.String()
    profession = fields.String()
    marital_status = fields.String()
    religion = fields.String()
    tribe = fields.String()
    description = fields.String()
    number = fields.Integer()
    status = fields.String()
    time_of_registry = fields.DateTime()


class Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sender_number = db.Column(db.String(13), nullable=False)
    message = db.Column(db.String(160), nullable=True)
    message_details = db.Column(db.String(160), nullable=True)
    message_myself = db.Column(db.String(160), nullable=True)
    receiver_shortcode = db.Column(db.Integer(), nullable=False)
    match_message = db.Column(db.String(160), nullable=True)
    delivery_time = db.Column(db.DateTime(timezone=True),
                         nullable=False, server_default=func.now())

    def __repr__(self):
        return self.sender_number

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_sender_number(cls, sender_number):
        return cls.query.order_by(desc(sender_number=sender_number)).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def last_inserted_row(self):
        db.session.add(self)
        db.session.flush(self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class MessageSchema(Schema):
    id = fields.Integer()
    sender_number = fields.Integer()
    message = fields.String()
    message_details = fields.String()
    message_myself = fields.String()
    receiver_shortcode = fields.Integer()
    match_message = fields.String()
    delivery_time = fields.DateTime()


class Penzi(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    shortcode = db.Column(db.Integer(), nullable=False)
    datetime = db.Column(db.DateTime(timezone=True),
                         nullable=False, server_default=func.now())

    def __repr__(self):
        return self.shortcode

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class PenziSchema(Schema):
    id = fields.Integer()
    message = fields.String()
    shortcode = fields.Integer()
    datetime = fields.DateTime()


admin.add_view(SecureModelView(User, db.session))
admin.add_view(SecureModelView(Message, db.session))
admin.add_view(NotificationsViews(name='Notifications', endpoint='notify'))
admin.add_view(LogoutViews(name='Logout', endpoint='logout'))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("email") == "james@admin.com" and request.form.get("password") == "admin":
            session['logged_in'] = True
            return redirect("/admin")
        else:
            return render_template("login.html", failed = True)
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
   
    

@app.route("/get_users", methods=["GET"])
def get_all_users():

    recipes = User.get_all()
    serializer = UserSchema(many=True)
    data = serializer.dump(recipes)

    return jsonify(
        data
    )


@app.route("/post", methods=["POST"])
def create_user():
    user_data = request.get_json()
    message_data = request.get_json()

    message_m = Message(

        header=message_data.get("header"),
        sender_number=message_data.get("sender_number"),
        message=message_data.get("message"),
        receiver_shortcode=message_data.get("receiver_shortcode")

    )

    message_m.save()
    serializer = MessageSchema()
    message_data = serializer.dump(message_m)

    user_u = User(

        name=user_data.get("name"),
        age=user_data.get("age"),
        gender=user_data.get("gender"),
        county=user_data.get("county"),
        town=user_data.get("town"),
        education_level=user_data.get("education_level"),
        profession=user_data.get("profession"),
        marital_status=user_data.get("marital_status"),
        religion=user_data.get("religion"),
        tribe=user_data.get("tribe"),
        number=user_data.get("number"),
        description=user_data.get("description")

    )

    user_u.save()
    serializer = UserSchema()
    user_data = serializer.dump(user_u)

    return jsonify(message_data) and jsonify(user_data), 201


@app.route("/post_penzi", methods=["POST"])
def post_penzi():
    penzi_data = request.get_json()

    penzi_m = Penzi(


        shortcode=penzi_data.get("shortcode"),
        message=penzi_data.get("message")

    )

    penzi_m.save()
    serializer = PenziSchema()
    penzi_data = serializer.dump(penzi_m)

    return jsonify(penzi_data), 201


@app.route("/post_start", methods=["POST"])
def post_start():
    message_data = request.get_json()

    message_m = Message(


        sender_number=message_data.get("sender_number"),
        message=message_data.get("message"),
        receiver_shortcode=message_data.get("receiver_shortcode")

    )

    message_m.save()
    serializer = MessageSchema()
    message_data = serializer.dump(message_m)
    return jsonify(message_data), 201


@app.route("/update/<int:id>", methods=["POST"])
def update_penzi(id):
    update_data = request.get_json(id)

    status_update = User(


        status=update_data.get("status")

    )

    status_update.save()
    serializer = PenziSchema()
    update_data = serializer.dump(status_update)

    return jsonify(update_data), 201


@app.route("/get_post_by_user/<int:id>", methods=["GET"])
def get_post_by_user(id):
    recipe = User.get_by_id(id)
    serializer = UserSchema()
    data = serializer.dump(recipe)

    return jsonify(data), 200


def sleep():
    time.sleep(5)


@app.route("/get_penzi_message_start/<int:id>", methods=["GET"])
def get_penzi_message_start(id):
    message_id = Penzi.get_by_id(id)
    Serializer = PenziSchema()
    data = Serializer.dump(message_id)

    sleep()

    return data.get("message"), 200


@app.route("/get_message_start/<string:sender_number>", methods=["GET"])
def get_message_start(sender_number):
    serial_query = Message.query.filter(Message.sender_number.like(''+sender_number+'')).order_by(Message.id.desc()).first()
    Serializer = MessageSchema()
    data = Serializer.dump(serial_query)

    return data.get("message"), 200


@app.route("/get_message_details/<string:sender_number>", methods=["GET"])
def get_message_details(sender_number):
    serial_query = Message.query.filter(Message.sender_number.like(''+sender_number+'')).order_by(Message.id.desc()).first()
    Serializer = MessageSchema()
    data = Serializer.dump(serial_query)
    

    return data.get("message_details"), 200


@app.route("/get_message_myself/<string:sender_number>", methods=["GET"])
def get_message_myself(sender_number):
    serial_query = Message.query.filter(Message.sender_number.like(''+sender_number+'')).order_by(Message.id.desc()).first()
    Serializer = MessageSchema()
    data = Serializer.dump(serial_query)

    return data.get("message_myself"), 200


@app.route("/get_message_match/<string:sender_number>", methods=["GET"])
def get_message_match(sender_number):
    serial_query = Message.query.filter(Message.sender_number.like(''+sender_number+'')).order_by(Message.id.desc()).first()
    Serializer = MessageSchema()
    data = Serializer.dump(serial_query)

    return data.get("match_message"), 200


@app.route("/get_gender/<string:number>", methods=["GET"])
def get_age(number):
    serial_query = User.get_by_number(number)
    Serializer = UserSchema()
    data = Serializer.dump(serial_query)

    return data.get("gender"), 200

@app.route("/get_number_type/<string:number>", methods=["GET"])
def get_number_type(number):
    serial_query = User.get_by_number(number)
    Serializer = UserSchema()
    data = Serializer.dump(serial_query)

    return data.get("number"), 200


@app.route("/get_search_result/<string:county>", methods=["GET"])
def search(county):
    search_result = User.query.filter(User.county.like('%'+county+'%')).first()
    Serializer = UserSchema()
    data = Serializer.dump(search_result)

    return jsonify(data), 200


@app.route("/search_test/<string:county>", methods=["GET"])
def search_test(county):
    search_result = User.query.filter(User.county.like('%'+county+'%')).all()
    Serializer = UserSchema(many=True)
    data = Serializer.dump(search_result)

    return jsonify(data)


@app.route("/search_test2/<string:county>", methods=["GET"])
def search_test2(county):
    search_result = User.query.filter(User.county.like('%'+county+'%')).count()
    # Serializer = UserSchema(many = True)
    # data = Serializer.dump(search_result)

    return str(search_result)


@app.route("/search_test3", methods=["GET"])
def search_test3():
    search_result = User.query.filter(User.county == "mombasa").first()
    Serializer = UserSchema()
    data = Serializer.dump(search_result)

    return data


@app.route("/search_test4", methods=["GET"])
def search_test4():
    search_result = User.query.filter(User.county == "nairobi").limit(2).all()
    Serializer = UserSchema(many=True)
    data = Serializer.dump(search_result)

    return jsonify(data)


@app.route("/search_test5/<string:county>/<int:age>", methods=["GET"])
def search_test5(county, age):
    search_result = User.query.filter(
        User.county.like('%'+county+'%'), User.age == age)
    Serializer = UserSchema(many=True)
    data = Serializer.dump(search_result)

    return jsonify(data)


@app.route("/search_test6/<int:age1>/<int:age2>", methods=["GET"])
def search_test6(age1, age2):
    recipe = User.query.filter(and_(User.age >= age1), (User.age) <= age2)
    serializer = UserSchema(many=True)
    data = serializer.dump(recipe)

    return jsonify(data)


@app.route("/search_test7/<int:age1>/<int:age2>/<string:county>", methods=["GET"])
def search_test7(age1, age2, county):
    recipe = User.query.filter(
        and_(User.age >= age1), (User.age) <= age2, (User.county.like('%'+county+'%')))
    serializer = UserSchema(many=True)
    data = serializer.dump(recipe)

    return jsonify(data)


@app.route("/search_test_number/<int:age1>/<int:age2>/<string:county>/<string:gender>", methods=["GET"])
def search_test_number(age1, age2, county, gender):
    data = User.query.filter(and_(User.age >= age1), (User.age) <= age2, (User.county.like(
        '%'+county+'%')), (User.gender.like(''+gender+''))).count()
    # serializer = UserSchema(many = True)
    # data = serializer.dump(recipe)

    # return jsonify(data)
    return str(data)


@app.route("/search_query/<int:age1>/<int:age2>/<string:county>/<string:gender>", methods=["GET"])
def search_query(age1, age2, county, gender):
    data = User.query.filter(and_(User.age >= age1), (User.age) <= age2, (User.county.like(
        '%'+county+'%')), (User.gender.like(''+gender+'')))
    serializer = UserSchema(many=True)
    data = serializer.dump(data)

    return jsonify(data)


@app.route("/search_test_new1/<int:age1>/<int:age2>/<string:county>", methods=["GET"])
def search_test_new1(age1, age2, county):
    recipe = User.query.filter(and_(User.age >= age1), (User.age) <= age2, (User.county.like(
        '%'+county+'%')), (User.gender.like("male")))
    serializer = UserSchema(many=True)
    data = serializer.dump(recipe)

    return jsonify(data)

    # return jsonify(data[0]["name"], data[0]["number"])


@app.route("/search_test_new2/<int:age1>/<int:age2>/<string:county>", methods=["GET"])
def search_test_new2(age1, age2, county):
    recipe = User.query.filter(and_(User.age >= age1), (User.age) <= age2, (User.county.like(
        '%'+county+'%')), (User.gender.like("female")))
    serializer = UserSchema(many=True)
    data = serializer.dump(recipe)
    d1 = data[0]["name"]

    return jsonify(d1)


@app.route("/search_test8/<int:age1>/<int:age2>/<string:county>", methods=["GET"])
def search_test8(age1, age2, county):
    recipe = User.query.filter(and_(
        User.age >= age1), (User.age) <= age2, (User.county.like('%'+county+'%'))).count()

    return str(recipe)


@app.route("/describe_by_number/<string:number>", methods=["GET"])
def describe_by_number(number):
    query = User.get_by_number(number)
    serializer = UserSchema()
    data = serializer.dump(query)

    return jsonify(data)


@app.route("/get_post_by_user1/<int:id>", methods=["GET"])
def get_post_by_user1(id):
    recipe = User.query.get(id)
    serializer = UserSchema()
    data = serializer.dump(recipe)

    return jsonify(data), 200


@app.route("/get_null/<int:id>", methods=["GET"])
def get_null(id):
    result = Message.get_by_id(id)
    serializer = MessageSchema()
    data = serializer.dump(result)
    none = "Empty"

    if data.get("details") == None:
        return none


@app.route("/post_start_user", methods=["POST"])
def post_start_user():
    user_data = request.get_json()
    user_m = User(


        name=user_data.get("name"),
        age=user_data.get("age"),
        gender=user_data.get("gender"),
        county=user_data.get("county"),
        town=user_data.get("town"),
        number=user_data.get("number")

    )

    user_m.save()
    serializer = UserSchema()
    user_data = serializer.dump(user_m)
    return jsonify(user_data), 201


@app.route("/patch_user_details/<string:number>", methods=["PUT"])
def update_user_details(number):
    user_to_update = User.get_by_number(number)

    data = request.get_json()

    user_to_update.education_level = data.get("education_level")
    user_to_update.profession = data.get("profession")
    user_to_update.marital_status = data.get("marital_status")
    user_to_update.religion = data.get("religion")
    user_to_update.tribe = data.get("tribe")

    db.session.commit()

    Serializer = UserSchema()

    recipe_data = Serializer.dump(user_to_update)

    return jsonify(recipe_data), 200


@app.route("/patch_user_myself/<string:number>", methods=["PUT"])
def update_user_myself(number):
    user_to_update = User.get_by_number(number)

    data = request.get_json()

    user_to_update.description = data.get("description")

    db.session.commit()

    Serializer = UserSchema()

    recipe_data = Serializer.dump(user_to_update)

    return jsonify(recipe_data), 200


@app.route("/post_message_details", methods=["POST"])
def post_message_details():
    details_message = request.get_json()

    message_m = Message(

        sender_number = details_message.get("sender_number"),
        message_details = details_message.get("message_details"),
        receiver_shortcode = details_message.get("receiver_shortcode")


    )

    message_m.save()
    serializer = MessageSchema()
    details_message = serializer.dump(message_m)

    return jsonify(details_message), 200


@app.route("/post_message_myself", methods=["POST"])
def post_message_myself():
    myself_message = request.get_json()

    message_m = Message(

        sender_number = myself_message.get("sender_number"),
        message_myself = myself_message.get("message_myself"),
        receiver_shortcode = myself_message.get("receiver_shortcode")


    )

    message_m.save()
    serializer = MessageSchema()
    myself_message = serializer.dump(message_m)

    return jsonify(myself_message), 200

@app.route("/post_message_match", methods=["POST"])
def post_message_match():
    match_message = request.get_json()

    message_m = Message(

        sender_number = match_message.get("sender_number"),
        match_message = match_message.get("match_message"),
        receiver_shortcode = match_message.get("receiver_shortcode")


    )

    message_m.save()
    serializer = MessageSchema()
    match_message = serializer.dump(message_m)

    return jsonify(match_message), 200


@app.route("/update_status/<string:number>", methods=["PUT"])
def update_status(number):
    user_to_update = User.get_by_number(number)

    data = request.get_json()

    user_to_update.status = data.get("status")

    db.session.commit()

    Serializer = UserSchema()

    recipe_data = Serializer.dump(user_to_update)

    return jsonify(recipe_data), 200


@app.route("/patch/<int:id>", methods=["PATCH"])
def update_user(id):
    penzi_data = request.get_json()

    penzi_m = User(


        status=penzi_data.get("shortcode"),

    )

    penzi_m.save()
    serializer = UserSchema()
    penzi_data = serializer.dump(penzi_m)

    return jsonify(penzi_data), 201


@app.route("/recipe/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    recipe_to_delete = User.get_by_id(id)

    recipe_to_delete.delete()

    return jsonify({"message": "Deleted"}), 204


@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Resource not found"}), 404


@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message": "Problem at local server"}), 500


if __name__ == "__main__":
    db.create_all()
    app.run(port=8007, debug=True)
