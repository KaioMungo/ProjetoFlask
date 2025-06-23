from flask import Blueprint, jsonify, request
from .aluno_model import addStudent, getStudents, getStudentById, updateStudent, deleteStudent
from errors import EmptyStringError, IdNotExist

student_blueprint = Blueprint('aluno', __name__)

@student_blueprint.route('/alunos', methods=['POST'])
def create_student():
    data = request.json
    try:
        addStudent(data)
        return jsonify(data), 201
    except EmptyStringError:
        return jsonify({'Error': 'As chaves não podem estar vazias.'}), 400
    except KeyError:
        return jsonify({'Error': 'Você não passou alguma chave.'}), 400
    except ValueError:
        return jsonify({'Error': 'A data está escrita de forma errada, o certo é yyyy-mm-dd.'}), 400
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404

@student_blueprint.route("/alunos", methods=['GET'])
def get_students():
    return jsonify(getStudents())

@student_blueprint.route("/alunos/<int:id>", methods=['GET'])
def get_student(id):
    try:
        return jsonify(getStudentById(id))
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404

@student_blueprint.route("/alunos/<int:id>", methods=['PUT'])
def update_student(id):
    data = request.json
    try:
        updateStudent(id, data)
        return jsonify(getStudentById(id))
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404
    except EmptyStringError:
        return jsonify({'Error': 'As chaves não podem estar vazias.'}), 400
    except KeyError:
        return jsonify({'Error': 'Você não passou alguma chave.'}), 400
    except ValueError:
        return jsonify({'Error': 'A data está escrita de forma errada, o certo é yyyy-mm-dd.'}), 400

@student_blueprint.route("/alunos/<int:id>", methods=['DELETE'])
def delete_student(id):
    try:
        deleteStudent(id)
        return jsonify({'Success': True})
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404