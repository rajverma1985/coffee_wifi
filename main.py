import json
import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe db TABLE Configuration

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != "_sa_instance_state"}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=['GET', 'POST'])
def random_cafes():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes).to_dict()
    return random_cafe


# HTTP GET - Read Record
@app.route("/all", methods=['GET'])
def get_all_cafes():
    all_cafes = db.session.query(Cafe).all()
    return jsonify({"cafe": [cafe.to_dict() for cafe in all_cafes]})


@app.route("/search", methods=['GET'])
def search_cafes():
    query_location = request.args.get("location")
    cafe = db.session.query(Cafe).filter_by(location=query_location).all()
    return jsonify({"cafe": [c.to_dict() for c in cafe]})


# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
