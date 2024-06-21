from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Pet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    animal_type: Mapped[str]
    personality: Mapped[str]
    color: Mapped[str]

def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "animal type": self.animal_type,
            "personality": self.personality,
            "coloring": self.color
        }