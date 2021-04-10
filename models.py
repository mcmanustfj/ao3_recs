from datetime import datetime

import sqlalchemy
from sqlalchemy import (JSON, Column, DateTime, ForeignKey, Integer, String,
                        Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, configure_mappers, relationship

kudos_table = Table('kudos', Base.metadata,
                    Column('user', String, ForeignKey('users.id')),
                    Column('work', Integer, ForeignKey('works.id')),
                    extend_existing=True
                    )

bookmarks_table = Table(
    'bookmarks',
    Base.metadata,
    Column('user', String, ForeignKey('users.id')),
    Column('work', Integer, ForeignKey('works.id')),
    extend_existing=True
)


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True)
    works = relationship('Work', backref='author')
    bookmarks_ts = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"User(id='{self.id}')"


class Work(Base):
    __tablename__ = 'works'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(String, ForeignKey('users.id'), nullable=True)
    json = Column(JSON, nullable=True)

    def __repr__(self):
        return f"Work(id={repr(self.id)}, \"{self.title}\" by {self.author.id})"

    kudos = relationship("User",
                         secondary=kudos_table,
                         backref='kudos')

    bookmarks = relationship("User",
                             secondary=bookmarks_table,
                             backref='bookmarks')

    bookmarks_ts = Column(DateTime, nullable=True)
