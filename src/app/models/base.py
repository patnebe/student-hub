from src.app import db

class Base(db.Model):
    """
    Base model to be inherited by other database tables
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    date_created = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
