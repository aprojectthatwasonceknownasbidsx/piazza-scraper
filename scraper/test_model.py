from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Post, Comment, Topic

engine = create_engine('sqlite:///test.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def add_post():
    p = Post("What is Piazza?","ITS COOL")
    p.children = [Comment("Who are you?")]
    p.topics = [Topic("Coolness"),Topic("Ultracool")]
    session.add(p)
    session.commit()

def get_posts():
    res = session.query(Post).all()
    for post in res:
        print(post.subject, ":", post.body)
        if post.topics:
            print("All topics",post.topics)
        if post.children:
            print("Responses:")
            for num,comment in enumerate(post.children):
                print("\t",num, ":", comment.text) 
        post.children.append(Comment("I agree"))
        session.add(post)
    session.commit()

    
if __name__ == "__main__":
    add_post()
    get_posts()