import unittest

import mongomock

import ortho
import pair as subject
import session


class MyTestCase(unittest.TestCase):
    def test_it_attempts_b_d_ex_nihilo(self):
        client = mongomock.MongoClient()
        collection = client.top
        s = session.start_session(client)
        s.ingest('A b.')
        s.ingest('C d.')
        s.ingest('A c.')
        s.ingest('B d.')
        subject.new_pair(s, "b", "d")
        o = ortho.create("a", "b", "c", "d")
        self.assertEqual(o, collection.orthos.find_one({"data": o})['data'])

    def test_it_attempts_a_b_ex_nihilo(self):
        client = mongomock.MongoClient()
        collection = client.top
        s = session.start_session(client)
        s.ingest('C d.')
        s.ingest('A c.')
        s.ingest('B d.')
        s.ingest('A b.')
        subject.new_pair(s, "a", "b")
        o = ortho.create("a", "b", "c", "d")
        self.assertEqual(o, collection.orthos.find_one({"data": o})['data'])

    def test_it_attempts_c_d_ex_nihilo(self):
        client = mongomock.MongoClient()
        collection = client.top
        s = session.start_session(client)
        s.ingest('A c.')
        s.ingest('B d.')
        s.ingest('A b.')
        s.ingest('C d.')
        subject.new_pair(s, "c", "d")
        o = ortho.create("a", "b", "c", "d")
        self.assertEqual(o, collection.orthos.find_one({"data": o})['data'])

    def test_it_attempts_a_c_ex_nihilo(self):
        client = mongomock.MongoClient()
        collection = client.top
        s = session.start_session(client)
        s.ingest('B d.')
        s.ingest('A b.')
        s.ingest('C d.')
        s.ingest('A c.')
        subject.new_pair(s, "a", "c")
        o = ortho.create("a", "b", "c", "d")
        self.assertEqual(o, collection.orthos.find_one({"data": o})['data'])


if __name__ == '__main__':
    unittest.main()
