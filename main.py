from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
import random


app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model, SerializerMixin):
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


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random", methods=["GET"]) ## GET is actually allowed automatically on all routes, but just for study purposes..
def random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    print(random_cafe.name)
    return jsonify(
    id=random_cafe.id,
    name = random_cafe.name,
    map_url = random_cafe.map_url,
    img_url = random_cafe.img_url,
    location = random_cafe.location,
    seats = random_cafe.seats,
    has_toilet = random_cafe.has_toilet,
    has_wifi = random_cafe.has_wifi,
    has_sockets = random_cafe.has_sockets,
    can_take_calls = random_cafe.can_take_calls,
    coffee_price = random_cafe.coffee_price
    )

@app.route("/all", methods=["GET"])
def get_all_cafes():
    cafes = db.session.query(Cafe).all()

    #Creating a dictionary from all cafe data.
    all_cafes = [{'id': cafe.id,
        'name': cafe.name,
        'map_url': cafe.map_url,
        'img_url':cafe.img_url,
        'location': cafe.location,
        'seats': cafe.seats,
        'has_toilet': cafe.has_toilet,
        'has_wifi': cafe.has_wifi,
        'has_sockets': cafe.has_sockets,
        'can_take_calls': cafe.can_take_calls,
        'coffee_price': cafe.coffee_price}
                 for cafe in cafes]

    return jsonify(all_cafes)

@app.route("/search", methods=["GET"])
def search_location():
    loc = request.args.get('loc')
    cafe = db.session.query(Cafe).filter_by(location=loc).first()
    if cafe:
        cafe = {'id': cafe.id,
         'name': cafe.name,
         'map_url': cafe.map_url,
         'img_url': cafe.img_url,
         'location': cafe.location,
         'seats': cafe.seats,
         'has_toilet': cafe.has_toilet,
         'has_wifi': cafe.has_wifi,
         'has_sockets': cafe.has_sockets,
         'can_take_calls': cafe.can_take_calls,
         'coffee_price': cafe.coffee_price}

        return jsonify(cafe=cafe)
    return jsonify(error={'Not Found': f'We were unable to find a cafe in {loc}.for '})


@app.route("/add", methods=["POST", "GET"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    price = request.args.get('price')











## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
