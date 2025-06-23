from config import db

def resetTables():
    db.drop_all()
    db.session.commit()

    db.create_all()
    db.session.commit()