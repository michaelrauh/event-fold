import unittest
import mongomock

import ortho
import session as subject


class MyTestCase(unittest.TestCase):
    def test_it_inserts_a_pair(self):
        client = mongomock.MongoClient()
        collection = client.top
        session = subject.start_session(client)
        session.ingest('A b.')
        self.assertEqual('b', collection.pairs.find_one({'from': 'a'})['to'])

    def test_it_updates_pair(self):
        client = mongomock.MongoClient()
        collection = client.top
        session = subject.start_session(client)
        session.ingest('A b. A c.')
        result = collection.pairs.find({'from': 'a'})
        self.assertEqual({'b', 'c'}, set([found['to'] for found in list(result)]))

    def test_it_can_ingest_in_multiple_chunks(self):
        client = mongomock.MongoClient()
        collection = client.top
        session = subject.start_session(client)
        session.ingest('A b.')
        session.ingest('A c.')
        result = collection.pairs.find({'from': 'a'})
        self.assertEqual({'b', 'c'}, set([found['to'] for found in list(result)]))

    def test_it_can_persist_across_objects(self):
        client = mongomock.MongoClient()
        collection = client.top
        session = subject.start_session(client)
        session.ingest('A b.')
        session = subject.start_session(client)
        session.ingest('A c.')
        result = collection.pairs.find({'from': 'a'})
        self.assertEqual({'b', 'c'}, set([found['to'] for found in list(result)]))

    def test_it_projects_backward(self):
        client = mongomock.MongoClient()
        session = subject.start_session(client)
        session.ingest('A b. C b.')
        result = session.project_backward('b')
        self.assertEqual({'a', 'c'}, result)

    def test_it_projects_forward(self):
        client = mongomock.MongoClient()
        session = subject.start_session(client)
        session.ingest('A b. A c.')
        result = session.project_forward('a')
        self.assertEqual({'b', 'c'}, result)

    def test_it_creates_ex_nihilo(self):
        client = mongomock.MongoClient()
        collection = client.top
        s = subject.start_session(client)
        s.ex_nihilo("a", "b", "c", "d")
        expected = ortho.create("a", "b", "c", "d")
        result = collection.orthos.find_one({"data": expected})['data']
        self.assertEqual(expected, result)


    def test_it_will_not_double_insert_orthos(self):
        client = mongomock.MongoClient()
        collection = client.top
        s = subject.start_session(client)
        expected = ortho.create("a", "b", "c", "d")
        s.ex_nihilo("a", "b", "c", "d")
        s.ex_nihilo("a", "c", "b", "d")
        result = len(list(collection.orthos.find({"data": expected})))

        self.assertEqual(1, result)


if __name__ == '__main__':
    unittest.main()
