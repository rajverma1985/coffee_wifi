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
@app.route("/cafes", methods=['GET'])
@app.route("/all", methods=['GET'])
def get_all_cafes():
    if request.args.get('id'):
        cafe_id = request.args.get('id')
        cafe = db.session.query(Cafe).get(cafe_id)
        if cafe:
            all_cafes = db.session.query(Cafe).filter_by(id=cafe_id).all()
            return jsonify({"cafe": [cafe.to_dict() for cafe in all_cafes]})
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        all_cafes = db.session.query(Cafe).all()
        return jsonify({"cafe": [cafe.to_dict() for cafe in all_cafes]})


@app.route("/search", methods=['GET'])
def search_cafes():
    query_location = request.args.get("location")
    cafe = db.session.query(Cafe).filter_by(location=query_location).all()
    return jsonify({"cafe": [c.to_dict() for c in cafe]})


# HTTP POST - Create Record
@app.route("/add", methods=['POST'])
def add_cafes():
    try:
        cafe = Cafe()
        for key in request.args.keys():
            if key in ['has_sockets', 'has_toilet', 'has_wifi', 'can_take_calls']:  # Test for boolean type attributes
                value = bool(value)
            else:
                value = request.args.get(key)
            cafe.__setattr__(key, value)
        db.session.add(cafe)
        db.session.commit()
    except Exception as error:
        return {"response": {"error": "{}".format(error)}}
    return {"response": {"success": "cafe added"}}


# HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    new_price = request.args.get('new_price')
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify({"success": "Successfully updated the price."})
    else:
        return jsonify({"error":
                            {"Not Found": "Sorry a cafe with that id was not found in the database."}})


# HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafe_id>')
def delete_cafe(cafe_id):
    api_key = request.args.get('api-key')
    if api_key == "TopSecretAPIKey":
        cafe = db.session.query(Cafe).get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403



if __name__ == '__main__':
    app.run(debug=True)
