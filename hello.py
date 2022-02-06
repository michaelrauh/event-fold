import ssl
import string

import certifi as certifi
import nltk
import pymongo
import more_itertools


def start_session(mongo):
    return Session(mongo)


class Session:
    def __init__(self, database):
        self.db = database
        self.collection = self.db.config

    def ingest(self, s):
        sentences = self._text_to_sentence_token_list(s)
        for sentence in sentences:
            for (f, s) in more_itertools.windowed(sentence, n=2):
                self.collection.forwards.update_one({"from": f}, {"$addToSet": {"to": s}}, upsert=True)

    @staticmethod
    def _text_to_sentence_token_list(s):
        return [[word.translate(str.maketrans('', '', string.punctuation)).lower() for word in sentence if word.translate(str.maketrans('', '', string.punctuation)).isalpha()] for sentence in
                [nltk.word_tokenize(t) for t in nltk.sent_tokenize(s)]]


if __name__ == '__main__':
    
    session = start_session(client)
    session.ingest("a b. c d.")
    print(session.db)

