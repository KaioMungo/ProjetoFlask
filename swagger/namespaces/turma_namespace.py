from flask_restx import Namespace, Resource, fields
from turma.turma_model import getClassrooms, addClassroom, getClassroomById, updateClassroom, deleteClassroom

turmas_ns = Namespace("turmas", description="Operações relacionadas as turmas")

turma_model = turmas_ns.model("TurmaInput", {
    "name": fields.String(required=True, description="Nome da turma"),
    "professor_id": fields.Integer(required=True, description="Id do professor regente da sala"),
    "active": fields.Boolean(required=True, description="Status da turma (true, false)")
})

turma_output_model = turmas_ns.model("TurmaOutput", {
    "id": fields.Integer(description="ID da turma"),
    "name": fields.String(required=True, description="Nome da turma"),
    "professor_id": fields.Integer(required=True, description="Id do professor regente da sala"),
    "active": fields.Boolean(required=True, description="Status da turma (true, false)")
})

@turmas_ns.route("/")
class TurmaResource(Resource):
    @turmas_ns.marshal_list_with(turma_output_model)
    def get(self):
        """Lista todos as turmas"""
        return getClassrooms()

    @turmas_ns.expect(turma_model)
    def post(self):
        """Cria uma nova turma"""
        data = turmas_ns.payload
        addClassroom(data)
        return data, 200

@turmas_ns.route("/<int:id_turma>")
class TurmaIdResource(Resource):
    @turmas_ns.marshal_with(turma_output_model)
    def get(self, id_turma):
        """Obtém um turma pelo ID"""
        return getClassroomById(id_turma)

    @turmas_ns.expect(turma_model)
    def put(self, id_turma):
        """Atualiza um turma pelo ID"""
        data = turmas_ns.payload
        updateClassroom(id_turma, data)
        return data, 200

    def delete(self, id_turma):
        """Exclui um turma pelo ID"""
        deleteClassroom(id_turma)
        return {"message": "Turma excluída com sucesso"}, 200