from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Post, Comment, Tag
from piazza_api import Piazza
from utils import *


class Scraper:
    """
    Usage for Scraper:

    >>> s = Scraper() # Initializes scraper/db connection
    >>> s.get(10) #Fetches 10 posts and stores them
    >>> s.print_topics() # Prints list of current topics/tags
    >>> s.print_posts() # Prints all posts in DB
    """
    
    def __init__(self):
        self.piazza = Piazza()
        self.piazza.user_login(email=Config.username, password=Config.password)
        self.course = self.piazza.network(Config.courseid)
        self.engine = create_engine('sqlite:///test.db', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get(self, limit=10):
        """
        Starts the scraper, and stores a certain number of 
        posts to the database: this is the primary method
        to be used in scraping

        <Possible Error> Currently, if you run the scraper twice
        it will duplicate -- must look into methods to fix that
        (probably using ID)

        Parameters:
            limit - Number of posts to fetch

        Returns:
            None
        """
        for _,post in enumerate(self.course.iter_all_posts(limit=limit)):
            self.process_one(post)
            print(_,post['history'][0]['subject'])

    def process_one(self, post):
        """
        Takes a post from the Piazza API,
        converts it into a format ready for the database,
        and stores it
        """

        time = parse_time(post['created'])
        title = remove_tags(post['history'][0]['subject'])
        body = remove_tags(post['history'][0]['content'])
        views = post['unique_views']
        favorites = post['num_favorites']
        sqlpost = Post(title, body, time, views, favorites)

        # Adding Comments
        for comment in process_all_children(post):
            time = parse_time(comment['created'])
            type = comment['type']
            if 'history' not in comment:
                subject = remove_tags(comment['subject'])
            else:
                subject = remove_tags(comment['history'][0]['content'])
            sqlpost.comments.append(Comment(subject, time, type))

        #Adding Tags
        for tag in post['tags']:
            sqlpost.tags.append(self.get_tag(tag))

        #Saving to Database
        self.session.add(sqlpost)
        self.session.commit()


    def get_tag(self, name):
        """
        Returns the topic if it exists, and otherwise creates it
        """

        tag = self.session.query(Tag).filter(Tag.name == name).first()
        if not tag:
            tag = Tag(name)
            self.session.add(tag)
            self.session.commit()
        return tag

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

    def print_tags(self):
        """
            Prints a list of topics currently registerd
        """
        topics = self.session.query(Tag).all()
        for topic in topics:
            print(topic)
           
