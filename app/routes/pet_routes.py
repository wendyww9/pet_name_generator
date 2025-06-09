from flask import Blueprint, request, abort, make_response
from ..db import db
from ..models.pet import Pet
from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
bp = Blueprint("pets", __name__, url_prefix="/pets")

@bp.post("")
def create_pet():
    request_body = request.get_json()
    request_body["name"] = generate_names(request_body)
    try: 
        new_pet = Pet.from_dict(request_body)
        db.session.add(new_pet)
        db.session.commit()

        return new_pet.to_dict(), 201
    
    except KeyError as e:
        abort(make_response({"message": f"missing required value: {e}"}, 400))


@bp.get("")
def get_pets():
    pet_query = db.select(Pet)

    pets = db.session.scalars(pet_query)
    response = []

    for pet in pets:
        response.append(pet.to_dict())

    return response

@bp.get("/<pet_id>")
def get_single_pet(pet_id):
    pet = validate_model(Pet,pet_id)
    return pet.to_dict()

def generate_names(request_body):
    input_message = (
        f"I need to come up with a pet name. "
        f"The pet species is a {request_body['coloration']} {request_body['animal']} "
        f"and has a personality {request_body['personality']}. "
        "Just return one name based on species, color and personality."
    )
    response = client.models.generate_content(
    model='gemini-1.5-flash',
    contents=input_message
)

    return response.text.strip("\n")


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