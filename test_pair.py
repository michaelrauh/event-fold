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

    def test_it_attempts_an_up_using_a_pair_and_existing_orthos_using_origin_projection(self):
        # todo insert base check for up
        client = mongomock.MongoClient()
        collection = client.top
        s = session.start_session(client)

        # insert l ortho
        s.ingest('a b.')
        s.ingest('c d.')
        s.ingest('a c.')
        s.ingest('b d.')
        subject.new_pair(s, "b", "d")

        # insert r ortho
        s.ingest('e f.')
        s.ingest('g h.')
        s.ingest('e g.')
        s.ingest('f h.')
        subject.new_pair(s, "f", "h")

        # insert up ortho with origin mapping coming last
        left = ortho.create("a", "b", "c", "d")
        right = ortho.create("e", "f", "g", "h")
        o = ortho.zip_up(left, right, {"f": "b", "g": "c"})
        s.ingest('b f')
        s.ingest('c g')
        s.ingest('d h')
        s.ingest('a e')
        subject.new_pair(s, "a", "e")

        self.assertEqual(o, collection.orthos.find_one({"data": o})['data'])

# TODO:
# integrated
# non-base dimension
# different shapes
# hop projection
# same projected coordinate
# location category mismatch
# coordinate mismatch
# coords are good but projection fails
# hit with a late miss (another pair is missing)

if __name__ == '__main__':
    unittest.main()
