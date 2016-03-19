from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Post, Comment, Topic
from piazza_api import Piazza
from utils import *

class Scraper:

    def __init__(self):
        self.piazza = Piazza()
        self.piazza.user_login(email=Config.username, password=Config.password)
        self.course = self.piazza.network(Config.courseid)
        self.engine = create_engine('sqlite:///test.db', echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def get(self, limit=10):
        for post in self.course.iter_all_posts(limit=limit):
            self.process_one(post)
            print("Entered")

    def process_one(self, post):
        if len(post['history']) == 0:
            return
        time = parse_time(post['created'])
        title = post['history'][0]['subject']
        body = post['history'][0]['content']
        sqlpost = Post(title, body, time)
        for comment in process_all_children(post):
            if len(comment['history']) == 0:
                continue
            time = parse_time(comment['created'])
            subject = comment['history'][0]['content']
            sqlpost.children.append(Comment(subject, time))
        session = self.Session()
        session.add(sqlpost)
        session.commit()

    def print_all(self):
        session = self.Session()
        posts = session.query(Post).all()
        for post in posts:
            print("Post: ", post)

