from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import relationship,backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

tag_table = Table('post_tags', Base.metadata,
                  Column('post', Integer, ForeignKey('posts.index')),
                  Column('tag', Integer, ForeignKey('tags.index'))
                  )  


class Post(Base):
    __tablename__ = "posts"

    index = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    time = Column(DateTime)
    views = Column(Integer)
    favorites = Column(Integer)

    tags = relationship("Tag", secondary=tag_table)
    comments = relationship("Comment", backref="post")
    analysis = relationship("PostAnalysis", backref=backref("post", uselist=False))

    def __init__(self, title, body, time,views=0,favorites=0):
        self.title = title
        self.text = body
        self.time = time
        self.views = views
        self.favorites = favorites

    def __repr__(self):
        return "Post<title=%s,time=%s>" % (self.title, str(self.time))


class Tag(Base):
    __tablename__ = "tags"
    index = Column(Integer, primary_key=True)
    name = Column(String)
    posts = relationship("Post", secondary=tag_table)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Topic(%s)" % self.name

    def __eq__(self, other):
        return self is other or self.name == other



class Comment(Base):
    __tablename__ = "comments"

    index = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.index'))


    text = Column(String)
    time = Column(DateTime)
    type = Column(String)

    def __init__(self, text, time, type):
        self.text = text
        self.time = time
        self.type = type

    def __repr__(self):
        return "Comment(%s)" % self.text


keyword_table = Table('post_keywords', Base.metadata,
                      Column('post', Integer, ForeignKey('post_analyses.index')),
                      Column('keyword', Integer, ForeignKey('keywords.index'))
                     )   


class PostAnalysis(Base):
    __tablename__ = "post_analyses"

    index = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.index'))

    keywords = relationship("Keyword", secondary=keyword_table)
    polarity = Column(Float)
    subjectivity = Column(Float)

    def __init__(self,polarity=0,subjectivity=0):
        self.polarity = polarity
        self.subjectivity = subjectivity


class Keyword(Base):
    __tablename__ = "keywords"
    index = Column(Integer, primary_key=True)
    name = Column(String)
    posts = relationship("PostAnalysis", secondary=keyword_table)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Topic(%s)" % self.name

    def __eq__(self, other):
        return self is other or self.name == other



if __name__ == "__main__":
    engine = create_engine('sqlite:///test.db', echo=False)
    Base.metadata.create_all(engine)
    print("Created Database")
