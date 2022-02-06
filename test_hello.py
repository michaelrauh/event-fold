import unittest
import mongomock
import hello as subject


class MyTestCase(unittest.TestCase):
    def test_it_inserts_a_forward(self):
        client = mongomock.MongoClient()
        collection = client.top
        session = subject.start_session(client)
        session.ingest('a b.')
        self.assertEqual('b', collection.forwards.find_one({'from': 'a'})['to'])

    def test_it_updates_forward(self):
        client = mongomock.MongoClient()
        collection = client.top
        session = subject.start_session(client)
        session.ingest('a b. a c.')
        result = collection.forwards.find({'from': 'a'})
        self.assertEqual({'b', 'c'}, set([found['to'] for found in list(result)]))

    def test_it_can_ingest_in_multiple_chunks(self):
        client = mongomock.MongoClient()
        collection = client.top
        session = subject.start_session(client)
        session.ingest('a b.')
        session.ingest('a c.')
        result = collection.forwards.find({'from': 'a'})
        self.assertEqual({'b', 'c'}, set([found['to'] for found in list(result)]))

    def test_it_can_persist_across_objects(self):
        client = mongomock.MongoClient()
        collection = client.top
        session = subject.start_session(client)
        session.ingest('a b.')
        session = subject.start_session(client)
        session.ingest('a c.')
        result = collection.forwards.find({'from': 'a'})
        self.assertEqual({'b', 'c'}, set([found['to'] for found in list(result)]))


if __name__ == '__main__':
    unittest.main()
