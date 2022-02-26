from flask import current_app
from sqlalchemy import Column, SmallInteger, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .diary import Diary
from .base import ModelMixin, TimestampMixin

with current_app.app_context():
    # Need to use db.Model for migrations to be detected.
    db = current_app.extensions["migrate"].db


class Note(ModelMixin, TimestampMixin, db.Model):  # type: ignore
    diary_id = Column(Integer, ForeignKey("diary.id", ondelete="CASCADE"))
    diary = relationship(Diary, back_populates='notes')
    position = Column(
        SmallInteger,
        nullable=False,
        unique=True,
        comment="The position of each note in a diary.",
    )
    text = Column(Text)
    image_url = Column(String(256))
    source_url = Column(String(256))

    def __str__(self):
        return f"<Note {self.id}>"
