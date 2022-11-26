from dataclasses import dataclass

from flask import current_app
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import relationship

from .base import ModelMixin, TimestampMixin
from .category import Category
from .database import DatabaseConnector

with current_app.app_context():
    # Need to use db.Model for migrations to be detected.
    db = current_app.extensions["migrate"].db


class Diary(ModelMixin, TimestampMixin, db.Model):  # type: ignore
    topic = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="RESTRICT"))
    category = relationship(Category, back_populates="diaries")
    notes = relationship("Note", back_populates="diary")
    source_url = Column(String(256))
    review_count = Column(SmallInteger, default=0)
    rate = Column(SmallInteger, default=0)

    __table_args__ = (db.UniqueConstraint("category_id", "topic"),)

    def __str__(self):
        return f"<Category {self.category.name}, topic {self.topic}>"


@dataclass
class DiaryConnector:
    model = Diary
    database_helper = DatabaseConnector()
