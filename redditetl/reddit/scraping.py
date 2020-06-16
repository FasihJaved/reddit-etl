from requests_html import HTML, HTMLSession
import pandas as pd 

MAINLINK = 'https://www.isidewith.com/'
SECONDLINK = "https://www.isidewith.com/candidates/"

#top_topics = []
#cand_ratings = []

def start_session(link):
    session = HTMLSession()
    return session.get(link)

def main_top_topics(r):
    top_topics = []
    polls = r.html.find('div.polls')

    for poll in polls[0].find('a'):
        top_topics.append(poll.text)

    return top_topics

def save_topic_data(topics):
    topics = pd.DataFrame(topics,columns=['topics'])
    topics.to_csv('topics.csv', sep=',', index=False)

def save_rating_data(ratings):
    ratings = pd.DataFrame(ratings,columns=['title', 'rating'])
    ratings.to_csv('ratings.csv', sep=',', index=False)

def save_data(top_topics, cand_ratings):
    save_topic_data(top_topics)
    save_rating_data(cand_ratings)

def get_cand_ratings(cand_r):
    cand_ratings = []
    rating_titles = cand_r.html.find('h3.rating_title')
    rating_text = cand_r.html.find('p.ign_cols')

    for i in range(len(rating_titles)):
        cand_ratings.append([rating_titles[i].text, rating_text[i].text])

    return cand_ratings

def scrape_data():
    r = start_session(MAINLINK)
    top_topics = main_top_topics(r)

    cand_r = start_session(SECONDLINK)
    cand_ratings = get_cand_ratings(cand_r)

    save_data(top_topics, cand_ratings)