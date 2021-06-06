#! /usr/bin/python3

from re import sub
import praw
from praw.models import MoreComments
import datetime as dt
import time
import json

from praw.reddit import Comment
import logging

logging.basicConfig(level=logging.DEBUG)

#Put your own credentials. Tutorial: https://medium.com/swlh/scraping-reddit-using-python-57e61e322486
reddit = praw.Reddit(client_id='', \
                     client_secret='', \
                     user_agent='', \
                     username='', \
                     password='')

url = "https://www.reddit.com/r/PublicFreakout/comments/nhr1cy/exactly_12_hours_since_the_ceasefire_israeli/?sort=controversial"
submission = reddit.submission(url=url)

begin = time.time()

submission.comment_sort = "controversial"
submission.comments.replace_more(limit=1)
comment_queue = submission.comments[:]
print(time.time() - begin)
print("  ".join([str(e.controversiality) for e in comment_queue]))

with open("data.json", "w") as f:
    l = []
    for e in comment_queue:
        d = e.__dict__
        d.pop("_replies")
        d.pop("_submission")
        d.pop("_reddit")
        d["author"] = str(d["author"])
        d.pop("subreddit")
        if d["controversiality"] == 1:
            # d.pop("_replies")
            # d.pop("_submission")
            # d.pop("_reddit")
            # d["author"] = str(d["author"])
            # d.pop("subreddit")
            l.append(d)

    json.dump(l, f, indent=4, sort_keys=True)

while comment_queue:
    comment = comment_queue.pop(0)
    print(comment.author, comment.body)
    try:
        comment_queue.extend(comment.replies)
    except AttributeError:
        pass
