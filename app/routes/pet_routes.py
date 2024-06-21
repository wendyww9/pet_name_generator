from flask import Blueprint, jsonify, request, abort, make_response
from ..db import db
from ..models.pet import Pet

bp = Blueprint("pets", __name__, url_prefix="/pets")

@bp.post("")
def add_pets():
    pass