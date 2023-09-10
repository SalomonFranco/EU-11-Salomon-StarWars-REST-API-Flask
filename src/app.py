"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite, Planet, People, Vehicle


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

#Sitemap with all the endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

### Planets
# GET ALL 
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets =  Planet.query.all()
    all_planets =  list(map(lambda x:x.serialize(), planets))
    return jsonify(all_planets)

# GET ONE 
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet =  Planet.query.get(planet_id)
    planet = planet.serialize()
    return jsonify(planet)


### people 
@app.route('/people', methods=['GET'])
def get_all_people():
    people =  People.query.all()
    all_peoples =  list(map(lambda x:x.serialize(), people))
    return jsonify(all_peoples)

# GET ONE 
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    people =  people.query.get(people_id)
    people = people.serialize()
    return jsonify(people)

### Vehicles
# GET ALL 
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicles =  Vehicle.query.all()
    all_vehicles =  list(map(lambda x:x.serialize(), vehicles))
    return jsonify(all_vehicles)

# GET ONE 
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle =  Vehicle.query.get(vehicle_id)
    vehicle = vehicle.serialize()
    return jsonify(vehicle)

### Users
# GET ALL 
@app.route('/users', methods=['GET'])
def get_users():
    users =  User.query.all()
    all_users =  list(map(lambda x:x.serialize(), users))
    return jsonify(all_users)

# GET ALL FAVORITES
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    current_user_id = 1
    user_favorites =  Favorite.query.filter_by(user_id = current_user_id)
    user_favorites_clean =  list(map(lambda x:x.serialize(), user_favorites))
    return jsonify(user_favorites_clean)


#ADD A NEW FAVORITE PLANET
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    current_user_id = 1
    print("planet_id from the URL", planet_id)
    
    favorite = Favorite.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()
    if favorite:
        return jsonify({"message": "Planet already in favorite"}), 400
    new_favorite = Favorite(user_id=current_user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message" : "Favorite added successfuly"})

#ADD A NEW FAVORITE people
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_people(people_id):
    current_user_id = 1
    print("people_id from the URL", people_id)
    
    favorite = Favorite.query.filter_by(user_id=current_user_id, people_id=people_id).first()
    if favorite:
        return jsonify({"message": "people already in favorite"}), 400
    new_favorite = Favorite(user_id=current_user_id, people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message" : "Favorite added successfuly"})

#ADD A NEW VEHICLE
@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_fav_vehicle(vehicle_id):
    current_user_id = 1
    print("vehicle_id from the URL", vehicle_id)
    
    # Check if User already has this planet as Favorite
    favorite = Favorite.query.filter_by(user_id=current_user_id, vehicle_id=vehicle_id).first()
    if favorite:
        return jsonify({"message": "Vehicle already in favorite"}), 400
    new_favorite = Favorite(user_id=current_user_id, vehicle_id=vehicle_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message" : "Favorite added successfuly"})

# DELETE
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_fav_planet(planet_id):
    current_user_id = 1
    favorite = Favorite.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"message": "Planet not in favorites"}), 400
    print("Favorite to be removed", favorite)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message" : "Favorite removed successfuly"})
    

# DELETE
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_fav_people(people_id):
    current_user_id = 1
    favorite = Favorite.query.filter_by(user_id=current_user_id, people_id=people_id).first()
    if not favorite:
        return jsonify({"message": "people not in favorites"}), 400
    print("Favorite to be removed", favorite)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message" : "Favorite removed successfuly"})

# DELETE
@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def remove_fav_vehicle(vehicle_id):
    current_user_id = 1
    favorite = Favorite.query.filter_by(user_id=current_user_id, vehicle_id=vehicle_id).first()
    if not favorite:
        return jsonify({"message": "Vehicle not in favorites"}), 400
    print("Favorite to be removed", favorite)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message" : "Favorite removed successfuly"})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)