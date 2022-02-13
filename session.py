import string

import certifi as certifi
import nltk
import pymongo
import more_itertools
import ortho


def start_session(mongo):
    return Session(mongo)


class Session:
    def __init__(self, database):
        self.db = database
        self.collection = self.db.top

    def project_backward(self, x):
        return {found['from'] for found in self.collection.pairs.find({"to": x})}

    def project_forward(self, x):
        return {found['to'] for found in self.collection.pairs.find({"from": x})}

    def ingest(self, s):
        sentences = self._text_to_sentence_token_list(s)
        for sentence in sentences:
            for (f, s) in more_itertools.windowed(sentence, n=2):
                ex = self.collection.pairs.find_one({"from": f, "to": s})
                if not ex:
                    print(f"inserting {f, s}")
                    self.collection.pairs.insert_one({"from": f, "to": s})
                else:
                    print(f"dropping {f, s}")

    def ortho_with_name(self, name):
        return [res['data'] for res in self.collection.orthos.find({"data": {"$elemMatch": {"$in": [name]}}})]

    @staticmethod
    def _text_to_sentence_token_list(s):
        return [[word.translate(str.maketrans('', '', string.punctuation)).lower() for word in sentence if
                 word.translate(str.maketrans('', '', string.punctuation)).isalpha()] for sentence in
                [nltk.word_tokenize(t) for t in nltk.sent_tokenize(s)]]

    def add_ortho(self, desired):
        ex = self.collection.orthos.find_one({"data": desired})
        if not ex:
            print(f"inserting {desired}")
            self.collection.orthos.insert_one({"data": desired})
        else:
            print(f"dropping {desired}")


if __name__ == '__main__':
    uri = "mongodb+srv://cluster0.t0zld.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri,
                                 tls=True,
                                 tlsCertificateKeyFile='X509-cert-5204489386261822956.pem', tlsCAFile=certifi.where())
    session = start_session(client)
    session.ingest("e f.")
