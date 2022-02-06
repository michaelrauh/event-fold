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
        self.collection = self.db.top

    def ingest(self, s):
        sentences = self._text_to_sentence_token_list(s)
        for sentence in sentences:
            for (f, s) in more_itertools.windowed(sentence, n=2):
                ex = self.collection.forwards.find_one({"from": f, "to": s})
                print(f"considering inserting {f, s}")
                if not ex:
                    print("inserting")
                    self.collection.forwards.insert_one({"from": f, "to": s})
                else:
                    print(f"dropping {f, s}")

    @staticmethod
    def _text_to_sentence_token_list(s):
        return [[word.translate(str.maketrans('', '', string.punctuation)).lower() for word in sentence if word.translate(str.maketrans('', '', string.punctuation)).isalpha()] for sentence in
                [nltk.word_tokenize(t) for t in nltk.sent_tokenize(s)]]


if __name__ == '__main__':
    uri = "mongodb+srv://cluster0.t0zld.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='X509-cert-5204489386261822956.pem', tlsCAFile=certifi.where())
    session = start_session(client)
    session.ingest("q r s t u v w x.")
