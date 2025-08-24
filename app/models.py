from . import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="Pending")

    def __repr__(self):
        return f"<Task {self.id}: {self.title} [{self.status}]>"
