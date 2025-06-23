from config import app, db
from aluno.aluno_routes import student_blueprint
from professor.professor_routes import professor_blueprint
from turma.turma_routes import classroom_blueprint
from reseta.reseta_routes import reset_blueprint  
from swagger.swagger_config import configure_swagger

app.register_blueprint(professor_blueprint)
app.register_blueprint(classroom_blueprint)
app.register_blueprint(student_blueprint)
app.register_blueprint(reset_blueprint)

configure_swagger(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )