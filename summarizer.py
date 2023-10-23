"""
Script to summarize text
"""

import spacy
import en_core_web_sm
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest



original_text ="""
API stands for Application Programming Interface. It is a set of rules and protocols that allows different software systems to communicate with each other. APIs allow different applications, services, and devices to exchange data and functionality in a secure and standardized way.

APIs are used to build complex systems by allowing different components to work together seamlessly. For example, a mobile app might use an API to retrieve data from a web service or to send data to a server. APIs can also be used to connect different devices, such as sensors or machines, to the internet and enable them to exchange data.
"""

nlp = spacy.load("en_core_web_sm")
nlp = en_core_web_sm.load()
doc = nlp(original_text)
keyword = []
stopwords = list(STOP_WORDS)
pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
for token in doc:
    if(token.text in stopwords or token.text in punctuation):
        continue
    if(token.pos_ in pos_tag):
        keyword.append(token.text)
freq_word = Counter(keyword)
max_freq = Counter(keyword).most_common(1)[0][1]
for word in freq_word.keys():
        freq_word[word] = (freq_word[word]/max_freq)
freq_word.most_common(5)
sent_strength={}
for sent in doc.sents:
    for word in sent:
        if word.text in freq_word.keys():
            if sent in sent_strength.keys():
                sent_strength[sent]+=freq_word[word.text]
            else:
                sent_strength[sent]=freq_word[word.text]
summarized_sentences = nlargest(3, sent_strength, key=sent_strength.get)
final_sentences = [ w.text for w in summarized_sentences ]
summary = ' '.join(final_sentences)
print("\n\n==!! Original Version !!==")
print(original_text)

print("\n\n==!! Summarized Version !!==")
print(summary)




