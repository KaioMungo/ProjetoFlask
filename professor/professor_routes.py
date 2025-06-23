from errors import EmptyStringError, IdNotExist
from config import db

class Professor(db.Model):
    __tablename__ = "professors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(255), nullable=True)

    def __init__(self, name, age, subject, info):
        self.name = name
        self.age = age
        self.subject = subject
        self.info = info

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "subject": self.subject,
            "info": self.info
        }

def addProfessor(data):
    if 'name' and 'age' and 'subject' and 'info' not in data:
        raise KeyError
    
    if data['name'] == "" or data['age'] == "" or data['subject'] == "" or data['info'] == "":
        raise EmptyStringError

    professor = Professor(
        name=data['name'],
        age=data['age'],
        subject=data['subject'],
        info=data['info']
    )

    db.session.add(professor)
    db.session.commit()

def getProfessors():
    professors = Professor.query.all()
    return [professor.to_dict() for professor in professors]

def getProfessorById(id):
    professor = Professor.query.get(id)

    if not professor:
        raise IdNotExist("O professor não foi encontrado.")
    
    return professor.to_dict()

def updateProfessor(id, data):
    professor = Professor.query.get(id)

    if not professor:
        raise IdNotExist("O professor que você quer atualizar não foi encontrado.")

    if 'name' and 'age' and 'subject' and 'info' not in data:
        raise KeyError
    
    if data['name'] == "" or data['age'] == "" or data['subject'] == "" or data['info'] == "":
        raise EmptyStringError

    professor.name = data['name']
    professor.age = data['age']
    professor.subject = data['subject']
    professor.info = data['info']

    db.session.commit()

def deleteProfessor(id):
    professor = Professor.query.get(id)

    if not professor:
        raise IdNotExist("O professor que você quer deletar não foi encontrado.")
    
    db.session.delete(professor)
    db.session.commit()