from errors import EmptyStringError, IdNotExist
from datetime import date, datetime
from config import db
from turma.turma_model import Classroom

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("classroom.id"))
    born_date = db.Column(db.String)
    first_grade = db.Column(db.Float)
    second_grade = db.Column(db.Float)
    final_average = db.Column(db.Float)
    age = db.Column(db.Integer)

    def __init__(self, name, class_id, born_date, first_grade, second_grade):
        self.name = name
        self.class_id = class_id
        self.born_date = born_date
        self.first_grade = first_grade
        self.second_grade = second_grade
        self.calculate_final_grade()
        self.calculate_age()

    def calculate_age(self):
        born_date = self.born_date.split("-")
        today = date.today()
        age = today.year - int(born_date[0])
        if (today.month, today.day) < (int(born_date[1]), int(born_date[2])):
            age -= 1
        self.age = age

    def calculate_final_grade(self):
        final_average = (float(self.first_grade) + float(self.second_grade)) / 2
        self.final_average = final_average

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "class_id": self.class_id,
            "born_date": self.born_date,
            "first_grade": self.first_grade,
            "second_grade": self.second_grade,
            "final_average": self.final_average,
            "age": self.age,
        }

def addStudent(data):
    classroom = Classroom.query.get(data['class_id'])

    if 'name' and 'class_id' and 'born_date' and 'first_grade' and 'second_grade' not in data:
        raise KeyError
    
    if data['name'] == "" or data['class_id'] == "" or data['born_date'] == "" or data['first_grade'] == "" or data['second_grade'] == "":
        raise EmptyStringError
    
    if not classroom:
        raise IdNotExist('O Id da classe não existe.')
    
    datetime.strptime(data['born_date'], '%Y-%m-%d')

    student = Student(
        name=data['name'],
        class_id=data['class_id'],
        born_date=data['born_date'],
        first_grade=data['first_grade'],
        second_grade=data['second_grade']
    )

    db.session.add(student)
    db.session.commit()


def getStudents():
    students = Student.query.all()
    return [student.to_dict() for student in students]


def getStudentById(id):
    student = Student.query.get(id)

    if not student:
        raise IdNotExist("O aluno não foi encontrado.")
    
    return student.to_dict()


def updateStudent(id, data):
    student = Student.query.get(id)
    classroom = Classroom.query.get(data['class_id'])

    if not student:
        raise IdNotExist("O aluno que você quer atualizar não foi encontrado.")
    
    if 'name' and 'class_id' and 'born_date' and 'first_grade' and 'second_grade' not in data:
        raise KeyError
    
    if data['name'] == "" or data['class_id'] == "" or data['born_date'] == "" or data['first_grade'] == "" or data['second_grade'] == "":
        raise EmptyStringError
    
    if not classroom:
        raise IdNotExist('O Id da classe não existe.')
    
    datetime.strptime(data['born_date'], '%Y-%m-%d')
    
    student.name = data['name']
    student.class_id = data['class_id']
    student.born_date = data['born_date']
    student.first_grade = data['first_grade']
    student.second_grade = data['second_grade']
    student.calculate_final_grade()
    student.calculate_age()
    db.session.commit()

def deleteStudent(id):
    student = Student.query.get(id)

    if not student:
        raise IdNotExist("O aluno que você quer deletar não foi encontrado.")
    
    db.session.delete(student)
    db.session.commit()