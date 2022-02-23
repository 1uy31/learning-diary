from flask import current_app
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String

from .base import ModelMixin, TimestampMixin

with current_app.app_context():
    # Need to use db.Model for migrations to be detected.
    db = current_app.extensions["migrate"].db


class Diary(ModelMixin, TimestampMixin, db.Model):  # type: ignore
    topic = Column(String, nullable=False)
    category = Column(Integer, ForeignKey("category.id", ondelete="RESTRICT"))
    note = Column(Integer, ForeignKey("note.id", ondelete="CASCADE"))
    source_url = Column(String(256))
    review_count = Column(SmallInteger, default=0)
    rate = Column(SmallInteger, default=0)

    def __str__(self):
        return f"<Diary {self.id}, topic {self.topic}>"
