from flask_sqlalchemy import SQLAlchemy
from random import randrange
# You will have to install names to randomly generate them 
import names # Generates names (first, last, full ...)

# Create DB instance
Db = SQLAlchemy()

class User(Db.Model):
    # Fields
    __tablename__ = 'users'
    user_id = Db.Column(Db.Integer, primary_key=True, autoincrement=True)
    first_name = Db.Column(Db.String(64), nullable=False)
    age = Db.Column(Db.Integer, nullable=False)

    # toString
    def toString(self):
        print(f"{self.user_id}: {self.first_name} ({self.age})")

    def __init__(self, idrange=100, agerange=70):
		# self.user_id = randrange(idrange)
        #self.user_id = randrange(idrange)
        self.age = randrange(agerange)
        self.first_name = names.get_first_name() # generates a random first name
        return