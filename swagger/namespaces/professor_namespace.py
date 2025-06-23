from flask_restx import Namespace, Resource, fields
from professor.professor_model import getProfessors, addProfessor, getProfessorById, updateProfessor, deleteProfessor

professores_ns = Namespace("professores", description="Operações relacionadas aos professores")

professor_model = professores_ns.model("ProfessorInput", {
    "name": fields.String(required=True, description="Nome do professor"),
    "age": fields.Integer(required=True, description="Idade do professor"),
    "subject": fields.String(required=True, description="Matéria aplicada pelo professor"),
    "info": fields.String(required=True, description="Informações adicionais sobre o professor")
})

professor_output_model = professores_ns.model("ProfessorOutput", {
    "id": fields.Integer(description="ID do professor"),
    "name": fields.String(required=True, description="Nome do professor"),
    "age": fields.Integer(required=True, description="Idade do professor"),
    "subject": fields.String(required=True, description="Matéria aplicada pelo professor"),
    "info": fields.String(required=True, description="Informações adicionais sobre o professor")
})

@professores_ns.route("/")
class ProfessoresResource(Resource):
    @professores_ns.marshal_list_with(professor_output_model)
    def get(self):
        """Lista todos os professores"""
        return getProfessors()

    @professores_ns.expect(professor_model)
    def post(self):
        """Cria um novo professor"""
        data = professores_ns.payload
        addProfessor(data)
        return data, 200

@professores_ns.route("/<int:id_professor>")
class ProfessorIdResource(Resource):
    @professores_ns.marshal_with(professor_output_model)
    def get(self, id_professor):
        """Obtém um professor pelo ID"""
        return getProfessorById(id_professor)

    @professores_ns.expect(professor_model)
    def put(self, id_professor):
        """Atualiza um professor pelo ID"""
        data = professores_ns.payload
        updateProfessor(id_professor, data)
        return data, 200

    def delete(self, id_professor):
        """Exclui um professor pelo ID"""
        deleteProfessor(id_professor)
        return {"message": "Professor excluído com sucesso"}, 200