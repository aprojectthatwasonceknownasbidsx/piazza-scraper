from datetime import datetime

def parse_time(s='2016-03-16T17:31:14Z'):

    """
    Converts Piazza Date-time format into a 
    pythonic construct.

    Examples of Piazza Datetime:
    - 2016-03-16T17:31:14Z
    """

    format = "%Y-%m-%dT%H:%M:%SZ"
    return datetime.strptime(s,format)

def process_all_children(post):
    return post['children'] + sum([process_all_children(child) 
                for child in post['children']], [])
