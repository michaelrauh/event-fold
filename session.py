import string
from enum import Enum, auto

import more_itertools
import nltk

import MongoClient


class ChangeType(Enum):
    PAIRS = auto()
    ORTHOS = auto()

    @staticmethod
    def from_str(label):
        if label == "pairs":
            return ChangeType.PAIRS
        elif label == "orthos":
            return ChangeType.ORTHOS


def start_session(mongo):
    return Session(mongo)


class Session:
    def __init__(self, database):
        self.db = database
        self.collection = self.db.top

    def delete_pair(self, f, t):
        self.collection.pairs.delete_one({"from": f, "to": t})

    def delete_ortho(self, o):
        self.collection.orthos.delete_one({"data": o})

    def project_backward(self, x):
        return {found['from'] for found in self.collection.pairs.find({"to": x})}

    def project_forward(self, x):
        return {found['to'] for found in self.collection.pairs.find({"from": x})}

    def listen_on_change(self, action):  # todo unit test
        print("listening")
        with self.db.watch() as stream:
            for change in stream:
                action(self, change)

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
        return [res['data'] for res in self.collection.orthos.find({"data": {"$elemMatch": {"$in": [name]}}})] # todo make ortho a class, and have it serialize on input. Serialization can include redundant info like origin. Then return the orthos and why. Split this method in three.

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

    @staticmethod  # todo unit test
    def change_type(change):
        return ChangeType.from_str(change['ns']['coll'])

    @staticmethod  # todo unit test
    def get_from(change):
        return change['fullDocument']['from']

    @staticmethod  # todo unit test
    def get_to(change):
        return change['fullDocument']['to']

    @staticmethod  # todo unit test
    def get_data(change):
        return change['fullDocument']['data']


if __name__ == '__main__':
    session = start_session(MongoClient.client)
    session.ingest("e f.")
