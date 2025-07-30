import spacy
from sklearn.feature_extraction.text import CountVectorizer
 
nlp = spacy.load('en_core_web_sm')

text = ['Fabolous Prodct', 'worthless. waste of money', 'bad service', 'happy about using and owning the product']

def tokenise(text): 
    doc = nlp(text)
    return [token for token in doc]

vect = CountVectorizer(tokeniser = tokenise)

x = vect.fit_transform(text)
print(x)