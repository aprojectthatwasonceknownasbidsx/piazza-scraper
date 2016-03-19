from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Post, Comment, Topic
from piazza_api import Piazza
from utils import *
import html


class Scraper:

    def __init__(self):
        self.piazza = Piazza()
        self.piazza.user_login(email=Config.username, password=Config.password)
        self.course = self.piazza.network(Config.courseid)
        self.engine = create_engine('sqlite:///test.db', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get(self, limit=10):
        for post in self.course.iter_all_posts(limit=limit):
            self.process_one(post)
            print("Entered")

    def process_one(self, post):
        time = parse_time(post['created'])
        title = html.unescape(post['history'][0]['subject'])
        body = html.unescape(post['history'][0]['content'])
        sqlpost = Post(title, body, time)
        for comment in process_all_children(post):
            time = parse_time(comment['created'])
            if 'history' not in comment:
                subject = html.unescape(comment['subject'])
            else:
                subject = html.unescape(comment['history'][0]['content'])
            sqlpost.children.append(Comment(subject, time))
        for topic in post['tags']:
            sqlpost.topics.append(self.get_topic(topic))
        self.session.add(sqlpost)
        self.session.commit()

    def get_topic(self, name):
        """
        Returns the topic if it exists, and otherwise creates it
        """

        topic = self.session.query(Topic).filter(Topic.name == name).first()
        if not topic:
            topic = Topic(name)
            self.session.add(topic)
            self.session.commit()
        return topic

    def print_posts(self):
        """
        Prints a list of all posts currently
        in the database
        """
        posts = self.session.query(Post).all()
        for post in posts:
            print(post)
            for comment in post.children:
                print("\t", comment)

    def print_topics(self):
        topics = self.session.query(Topic).all()
        for topic in topics:
            print(topic)
           