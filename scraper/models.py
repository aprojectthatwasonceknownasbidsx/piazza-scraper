from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import relationship,backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

association_table = Table('topic_post', Base.metadata,
                            Column('post', Integer, ForeignKey('posts.index')),
                            Column('topic', Integer, ForeignKey('topics.index'))
                          )   


class Post(Base):
    __tablename__ = "posts"

    index = Column(Integer, primary_key=True)
    subject = Column(String)
    body = Column(String)
    time = Column(DateTime)

    topics = relationship("Topic", secondary=association_table)
    children = relationship("Comment", backref="posts")

    def __init__(self, title, body, time):
        self.subject = title
        self.body = body
        self.time = time

    def __repr__(self):
        return "Post<title=%s,time=%s" % (self.subject, str(self.time))


class Topic(Base):
    __tablename__ = "topics"
    index = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Topic(%s)" % self.name

    def __eq__(self, other):
        return self is other or self.name == other


class Comment(Base):
    __tablename__ = "comments"

    index = Column(Integer, primary_key=True)
    text = Column(String)
    parent = Column(Integer, ForeignKey('posts.index'))
    time = Column(DateTime)

    def __init__(self, text, time):
        self.text = text
        self.time = time

    def __repr__(self):
        return "Comment(%s)" % self.text

if __name__ == "__main__":
    engine = create_engine('sqlite:///test.db', echo=True)
    Base.metadata.create_all(engine)
