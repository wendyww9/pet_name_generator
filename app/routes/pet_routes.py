from flask import Blueprint, jsonify, request, abort, make_response
from ..db import db
from ..models.pet import Pet

bp = Blueprint("pets", __name__, url_prefix="/pets")

@bp.post("")
def create_pet():
    request_body = request.get_json()
    try: 
        new_pet = Pet.from_dict(request_body)
        db.session.add(new_pet)
        db.session.commit()

        return make_response(new_pet.to_dict(), 201)
    
    except KeyError as e:
        abort(make_response({"message": f"missing required value: {e}"}, 400))

@bp.get("")
def get_pets():
    pet_query = db.select(Pet)

    pets = db.session.scalars(pet_query)
    response = []

    for pet in pets:
        response.append(pet.to_dict())

    return jsonify(response)

@bp.get("/<pet_id>")
def get_single_cat(pet_id):
    cat = validate_model(Pet,pet_id)
    return cat.to_dict()

def validate_model(cls,id):
    try:
        id = int(id)
    except:
        response =  response = {"message": f"{cls.__name__} {id} invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)
    if model:
        return model

    response = {"message": f"{cls.__name__} {id} not found"}
    abort(make_response(response, 404))