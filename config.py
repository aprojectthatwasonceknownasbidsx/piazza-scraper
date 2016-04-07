import os

get = lambda *args: os.environ.get(*args)

class Config:
    username = get('DB_USERNAME', "")
    password = get('DB_PASSWORD', "")
    courseid = get('COURSEID', "")
