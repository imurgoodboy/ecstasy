import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
nlp = spacy.load('en_core_web_sm')
sia = SentimentIntensityAnalyzer()


y = sia.polarity_scores('Heavy rainfall triggers severe waterlogging on mehran')
print(y['compound'])