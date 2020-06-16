import nltk
from nltk import bigrams
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
import pandas as pd 
import csv

def read_csv_text(filename):
    text = ''
    with open(filename+'.csv', "rt", encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:
            if filename == 'posts':
                text += row[3] + ' '
            if filename == 'comments':
                text += row[1] + ' '
    return text

def create_tokens(text):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    return tokens

def remove_stopwords_from_tokens(tokens):
    return [word for word in tokens if word not in stopwords.words('english')]

def create_bigrams_from_tokens(tokens):
    return list(bigrams(filtered_words))

def sep_bigram_n_count(bigrams):
    bigram_final = []
    count = []
    for bigram in bigrams:
        bigram_final.append(bigram[0][0]+'-'+bigram[0][1])
        count.append(bigram[1])
    return bigram_final, count

def extract_words_n_bigrams(filename):
    text = read_csv_text(filename)
    tokens = create_tokens(text)

    filtered_words = remove_stopwords_from_tokens(tokens)
    filtered_bigram = create_bigrams_from_tokens(filtered_words)
    return filtered_words, filtered_bigram

def save_data(words, bigrams):
    words_to_write = pd.DataFrame(words.most_common(50),columns=['word', 'count'])
    words_to_write.to_csv('words.csv', sep=',', index=False)

    sep_bigram, sep_count = sep_bigram_n_count(bigrams.most_common(50))

    bigrams_to_write = pd.DataFrame({'bigram': sep_bigram, 'count': sep_count})
    bigrams_to_write.to_csv('bigrams.csv', sep=',', index=False)

def analyze(filename):
    words, bigrams = extract_words_n_bigrams(filename)

    freq_words = FreqDist(words)
    freq_bigrams = FreqDist(bigrams)

    save_data(freq_words, freq_bigrams)


def analyze_files():
    analyze('posts')
    analyze('comments')