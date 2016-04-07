from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from piazza_api import Piazza
from utils import *
from datetime import datetime,timedelta
import argparse

class Scraper:
    """
    Usage for Scraper:

    >>> s = Scraper() # Initializes scraper/db connection
    >>> s.get(10) #Fetches 10 posts and stores them
    >>> s.print_topics() # Prints list of current topics/tags
    >>> s.print_posts() # Prints all posts in DB
    """
    
    def __init__(self,days_refresh=10):
        self.piazza = Piazza()
        self.piazza.user_login(email=Config.username, password=Config.password)
        self.course = self.piazza.network(Config.courseid)
        self.engine = create_engine('sqlite:///test.db', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.days    = days_refresh

    def parse(self):
        self.refetch_stats()
        print("Finished getting stats")
        self.delete_recent()
        self.get_recent_posts()

    def get_recent_posts(self):
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

        for _,post in enumerate(self.course.iter_all_posts()):
            if not self.process_one(post):
                return
            print(_,post['history'][0]['subject'])

    def process_one(self, post):
        """
        Takes a post from the Piazza API,
        converts it into a format ready for the database,
        and stores it
        """

        time = parse_time(post['created'])
        duplicate = self.session.query(Post).filter(Post.time == time).first()
        title = remove_tags(post['history'][0]['subject'])
        body = remove_tags(post['history'][0]['content'])
        views = post['unique_views']
        favorites = post['num_favorites']
        if duplicate is not None:
            if post['bucket_name'] == 'Pinned':
                return True
            return False
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
        return True


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

    def delete_all(self):
        self.session.query(Post).delete()
        self.session.query(Comment).delete()
        self.session.query(Tag).delete()

    def delete_recent(self):
        recent = datetime.now()-timedelta(days=self.days)
        self.session.query(Post).filter(Post.time > recent).delete()

    def refetch_stats(self):
        mostrecent = s.session.query(DayStats).order_by(DayStats.day.desc()).first()
        if mostrecent is not None:
            delta = datetime.now()-mostrecent.day
        if mostrecent is None or delta > timedelta(days=1):
            stats = self.course.get_statistics()
            self.session.query(DayStats).delete()
            for daily in stats['daily']:
                day = parse_day(daily['day'])
                self.session.add(DayStats(daily['questions'],day,daily['users'],daily['posts']))
            self.session.commit()
        print("Finished updating statistics")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrapes Piazza posts for use in AnnPod Analysis')
    parser.add_argument('-r','--refresh',nargs='?',type=int, 
        default=2,help='The amount of time to check for new content (Typically around a week is good)')
    refresh =parser.parse_args().refresh
    print("Scraping all new posts (with overlap %d)"%refresh)
    s = Scraper(refresh)
    s.parse()