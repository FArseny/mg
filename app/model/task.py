from app import db

class Task(db.Model):
    
    __tablename__ = 'task'

    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    x        = db.Column(db.Integer)
    y        = db.Column(db.Integer)
    operator = db.Column(db.String(1))
    finished = db.Column(db.Boolean, default=False)
    result   = db.Column(db.Float, default=0)

    def __repr__(self):
        return f"{self.x} {self.operator} {self.y}"
