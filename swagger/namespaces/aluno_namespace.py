from flask_restx import Namespace, Resource, fields
from aluno.aluno_model import getStudents, addStudent, getStudentById, updateStudent, deleteStudent

alunos_ns = Namespace("alunos", description="Operações relacionadas aos alunos")

aluno_model = alunos_ns.model("AlunoInput", {
    "name": fields.String(required=True, description="Nome do aluno"),
    "born_date": fields.String(required=True, description="Data de nascimento (YYYY-MM-DD)"),
    "first_grade": fields.Float(required=True, description="Nota do primeiro semestre"),
    "second_grade": fields.Float(required=True, description="Nota do segundo semestre"),
    "class_id": fields.Integer(required=True, description="ID da turma associada"),
})

aluno_output_model = alunos_ns.model("AlunoOutput", {
    "id": fields.Integer(description="ID do aluno"),
    "name": fields.String(description="Nome do aluno"),
    "age": fields.Integer(description="Idade do aluno"),
    "born_date": fields.String(description="Data de nascimento (YYYY-MM-DD)"),
    "first_grade": fields.Float(description="Nota do primeiro semestre"),
    "second_grade": fields.Float(description="Nota do segundo semestre"),
    "final_average": fields.Float(description="Média final do aluno"),
    "class_id": fields.Integer(description="ID da turma associada"),
})

@alunos_ns.route("/")
class AlunosResource(Resource):
    @alunos_ns.marshal_list_with(aluno_output_model)
    def get(self):
        """Lista todos os alunos"""
        return getStudents()

    @alunos_ns.expect(aluno_model)
    def post(self):
        """Cria um novo aluno"""
        data = alunos_ns.payload
        response, status_code = addStudent(data)
        return response, status_code

@alunos_ns.route("/<int:id_aluno>")
class AlunoIdResource(Resource):
    @alunos_ns.marshal_with(aluno_output_model)
    def get(self, id_aluno):
        """Obtém um aluno pelo ID"""
        return getStudentById(id_aluno)

    @alunos_ns.expect(aluno_model)
    def put(self, id_aluno):
        """Atualiza um aluno pelo ID"""
        data = alunos_ns.payload
        updateStudent(id_aluno, data)
        return data, 200

    def delete(self, id_aluno):
        """Exclui um aluno pelo ID"""
        deleteStudent(id_aluno)
        return {"message": "Aluno excluído com sucesso"}, 200