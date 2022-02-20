from flask import current_app
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, SmallInteger,
                        String, Text, func)
from sqlalchemy.orm import declared_attr, relationship

with current_app.app_context():
    # Need to use db.Model for migrations to be detected.
    db = current_app.extensions["migrate"].db


class ModelMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Category(ModelMixin, TimestampMixin, db.Model):  # type: ignore
    name = Column(String(256), nullable=False, unique=True)
    diaries = relationship("Diary")

    def __str__(self):
        return f"<Category: {self.name}>"


class Note(ModelMixin, TimestampMixin, db.Model):  # type: ignore
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


class Diary(ModelMixin, TimestampMixin, db.Model):  # type: ignore
    topic = Column(String, nullable=False)
    category = Column(Integer, ForeignKey("category.id", ondelete="RESTRICT"))
    note = Column(Integer, ForeignKey("note.id", ondelete="CASCADE"))
    source_url = Column(String(256))
    review_count = Column(SmallInteger, default=0)
    rate = Column(SmallInteger, default=0)

    def __str__(self):
        return f"<Diary {self.id}, topic {self.topic}>"
