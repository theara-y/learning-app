from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    info = db.Column(db.JSON, nullable=False)
    group_id = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "info": self.info,
            "group_id": self.group_id
        }


class Progress(db.Model):
    __tablename__ = 'progress'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    question_id = db.Column(db.Integer, primary_key=True, nullable=False)
    next_milestone = db.Column(db.Integer, nullable=False)
    next_milestone_date = db.Column(db.DateTime(timezone=True), nullable=False)
    mastered = db.Column(db.Boolean, nullable=False)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "question_id": self.question_id,
            "next_milestone": self.next_milestone,
            "next_milestone_date": self.next_milestone_date.strftime('%Y-%m-%d'),
            "mastered": self.mastered
        }
