import spacy
from spacy.matcher import Matcher
import syllapy
import random
import tweepy
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
consumer_key = config['Auth']['consumer_key']
consumer_secret = config['Auth']['consumer_secret']
access_token = config['Auth']['access_token']
access_token_secret = config['Auth']['access_token_secret']
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
patterns = [
    [{'POS': {"IN": ["NOUN", "ADP", "ADJ", "ADV"]} },
     {'POS': {"IN": ["NOUN", "VERB"]} }],
    [{'POS': {"IN": ["NOUN", "ADP", "ADJ", "ADV"]} },
     {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
     {'POS': {"IN": ["NOUN", "VERB", "ADJ", "ADV"]} }],
    [{'POS': {"IN": ["NOUN", "ADP", "ADJ", "ADV"]} },
     {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
     {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
     {'POS': {"IN": ["NOUN", "VERB", "ADJ", "ADV"]} }]
]
for i, pattern in enumerate(patterns):
    matcher.add(f"pattern{i}", [pattern])

# Create an empty list to store haikus
haikus = []

# Read the haiku file line by line
with open("haiku.txt", "r") as f:
    haiku = ""
    for line in f:
        line = line.strip()
        if line:
            haiku += " " + line
        else:
            haikus.append(haiku)
            haiku = ""

g_5 = set()
g_7 = set()

# Process each haiku in the list
for haiku in haikus:
    doc = nlp(haiku)
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        syl_count = 0
        for token in span:
            syl_count += syllapy.count(token.text)
        if syl_count == 5:
            g_5.add(span.text)
        elif syl_count == 7:
            g_7.add(span.text)

# Choose random haikus and tweet it
message = "%s\n%s\n%s" % (random.choice(list(g_5)), random.choice(list(g_7)), random.choice(list(g_5)))
print(message)
api.update_status(message)

