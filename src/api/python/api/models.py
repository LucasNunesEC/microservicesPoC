from api import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(140))
    done = db.Column(db.Boolean)

    def __init__(self, title, description, done):
        self.title = title
        self.description = description
        self.done = done

    def __repr__(self):
        return '<Task: Title: {} -- Description: {} -- Done: {} .>'.format(self.title, self.description, self.done)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
        }