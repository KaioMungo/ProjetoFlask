from flask import Blueprint, jsonify, request
from .turma_model import addClassroom, getClassrooms, getClassroomById, updateClassroom, deleteClassroom
from errors import EmptyStringError, IdNotExist

classroom_blueprint = Blueprint('turma', __name__)

@classroom_blueprint.route('/turmas', methods=['POST'])
def create_classroom():
    data = request.json
    try:
        addClassroom(data)
        return jsonify(data), 201
    except EmptyStringError:
        return jsonify({'Error': 'As chaves não podem estar vazias.'}), 400
    except KeyError:
        return jsonify({'Error': 'Você não passou alguma chave.'}), 400
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404

@classroom_blueprint.route("/turmas", methods=['GET'])
def get_classrooms():
    return jsonify(getClassrooms())

@classroom_blueprint.route("/turmas/<int:id>", methods=['GET'])
def get_classroom(id):
    try:
        return jsonify(getClassroomById(id)) 
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404

@classroom_blueprint.route("/turmas/<int:id>", methods=['PUT'])
def update_classroom(id):
    data = request.json
    try:
        updateClassroom(id, data)
        return jsonify(getClassroomById(id))
    except EmptyStringError:
        return jsonify({'Error': 'As chaves não podem estar vazias.'}), 400
    except KeyError:
        return jsonify({'Error': 'Você não passou alguma chave.'}), 400
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404

@classroom_blueprint.route("/turmas/<int:id>", methods=['DELETE'])
def delete_classroom(id):
    try:
        deleteClassroom(id)
        return jsonify({'Success': True})
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404