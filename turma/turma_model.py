from errors import EmptyStringError, IdNotExist
from config import db
from professor.professor_model import Professor

class Classroom(db.Model):
    __tablename__ = "classroom"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey("professors.id"))
    active = db.Column(db.Boolean, default=True)
    reserved = db.Column(db.Boolean, default=False)

    def __init__(self, name, professor_id, active=True, reserved=False):
        self.name = name
        self.professor_id = professor_id
        self.active = active
        self.reserved = reserved

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "professor_id": self.professor_id,
            "active": self.active,
            "reserved": self.reserved
        }

def addClassroom(data):
    professor = Professor.query.get(data['professor_id'])

    if 'name' and 'professor_id' and 'active' not in data:
        raise KeyError
    
    if data['name'] == "" or data['professor_id'] == "" or data['active'] == "":
        raise EmptyStringError
    
    if not professor:
        raise IdNotExist("O Id do professor não existe.")

    classroom = Classroom(
        name=data['name'],
        professor_id=data['professor_id'],
        active=data['active']
    )

    db.session.add(classroom)
    db.session.commit()

def getClassrooms():
    classrooms = Classroom.query.all()
    return [classroom.to_dict() for classroom in classrooms]

def getClassroomById(id):
    classroom = Classroom.query.get(id)

    if not classroom:
        raise IdNotExist("A turma não foi encontrada.")
    
    return classroom.to_dict()

def updateClassroom(id, data):
    classroom = Classroom.query.get(id)
    professor = Professor.query.get(data['professor_id'])

    if not classroom:
        raise IdNotExist("A turma que você quer atualizar não foi encontrada.")

    if 'name' and 'professor_id' and 'active' not in data:
        raise KeyError
    
    if data['name'] == "" or data['professor_id'] == "" or data['active'] == "":
        raise EmptyStringError
    
    if not professor:
        raise IdNotExist("O Id do professor não existe.")

    classroom.name = data['name']
    classroom.professor_id = data['professor_id']
    classroom.active = data['active']
    
    if 'reserved' in data:
        classroom.reserved = data['reserved']

    db.session.commit()

def deleteClassroom(id):
    classroom = Classroom.query.get(id)

    if not classroom:
        raise IdNotExist("A turma que você quer deletar não foi encontrada.")
    
    db.session.delete(classroom)
    db.session.commit()