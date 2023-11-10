"""
Script to summarize text
"""

import spacy
import en_core_web_md
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest


def less_words(s):
    words = s.split()
    return len(words) <= 15


def summarize(original_text):
    if (less_words(original_text)) or (original_text.isnumeric()):
        return ''
    nlp = spacy.load("en_core_web_md")
    nlp = en_core_web_md.load()
    doc = nlp(original_text)
    keyword = []
    stopwords = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if (token.text in stopwords or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            keyword.append(token.text)
    freq_word = Counter(keyword)
    max_freq = Counter(keyword).most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = (freq_word[word]/max_freq)
    freq_word.most_common(5)
    sent_strength = {}
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
    return summary