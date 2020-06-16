import string
import datetime
import praw
import pandas as pd 
import nltk
from nltk import bigrams
from nltk import FreqDist
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize.treebank import TreebankWordDetokenizer

# Setting global credentials
CLIENT_ID = 'WmnGA9wuUHoBeA'
CLIENT_SECRET = 'E4hSpxdgfFNNgV3tKXsjPSoSf2g'
USER_AGENT = 'reddit for petproject'
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

def get_top_posts(subreddit_name, time):
    top_posts = reddit.subreddit(subreddit_name).top(time)
    return top_posts

def punctuation_list():
    punctuations = list(string.punctuation)
    punctuations.extend(["''", 'â€˜', 'â€™'])
    return punctuations

def remove_punctuation(text):
    punc = punctuations_list()
    filtered_text = [i.strip("".join(punc)) for i in word_tokenize(text) if i not in punc]
    return filtered_text

def token_to_text(token):
    return TreebankWordDetokenizer().detokenize(token)

def get_all_comments(post_id):
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=None) 
    return submission.comments.list()

def filter_text(text):
    tokenized_text = remove_punctuation(text)
    filtered = token_to_text(tokenized_text)
    return filtered

def extract_comments(post_id):
    comments = []
    all_comments = get_all_comments(post_id)

    for comment in all_comments:
        filtered_comment = filter_text(comment.body)

        if filtered_comment is None:
            comments.append([post_id, 'empty'])
        else:
            comments.append([post_id, filtered_comment])

    return comments

def save_data(posts, comments):
    comments = pd.DataFrame(comments,columns=['post_id', 'comment'])
    posts = pd.DataFrame(
        posts,
        columns=[
            'id', 'score', 'upvote_ratio', 
            'title', 'subreddit', 'url',
            'num_comments', 'body', 'created'
            ]
        )
    posts['created']=(pd.to_datetime(posts['created'],unit='s'))

    posts.to_csv('posts.csv', sep=',', index=False)
    comments.to_csv('comments.csv', sep=',', index=False)

def download_data():
    posts = []
    comments = []
    top_posts = get_top_posts('politics', 'day')

    for post in top_posts:
        filtered_title = filter_text(post.title)
        posts.append([
            post.id, post.score, post.upvote_ratio, 
            post.title, post.subreddit, post.url, 
            post.num_comments, post.selftext, post.created
            ])
        comments.append(extract_comments(filtered_title))

    save_data(posts, comments)
    
    