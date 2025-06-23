from flask import Blueprint, jsonify
from .reseta_model import resetTables

reset_blueprint = Blueprint('reset', __name__)

@reset_blueprint.route("/reseta", methods = ["POST"])
def reset_data():
    resetTables()
    return jsonify({'Success': True})