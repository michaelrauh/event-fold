
import mongomock

import ortho
import session as subject


class TestSession:
    def test_it_inserts_a_pair(self):
        client = mongomock.MongoClient()
        collection = client.top
        session = subject.start_session(client)
        session.ingest('A b.')
        assert 'b' == collection.pairs.find_one({'from': 'a'})['to']

    def test_it_updates_pair(self):
        client = mongomock.MongoClient()
        collection = client.top
        session = subject.start_session(client)
        session.ingest('A b. A c.')
        result = collection.pairs.find({'from': 'a'})
        assert {'b', 'c'} == set([found['to'] for found in list(result)])

    def test_it_can_ingest_in_multiple_chunks(self):
        client = mongomock.MongoClient()
        collection = client.top
        session = subject.start_session(client)
        session.ingest('A b.')
        session.ingest('A c.')
        result = collection.pairs.find({'from': 'a'})
        assert {'b', 'c'} == set([found['to'] for found in list(result)])

    def test_it_can_persist_across_objects(self):
        client = mongomock.MongoClient()
        collection = client.top
        session = subject.start_session(client)
        session.ingest('A b.')
        session = subject.start_session(client)
        session.ingest('A c.')
        result = collection.pairs.find({'from': 'a'})
        assert {'b', 'c'} == set([found['to'] for found in list(result)])

    def test_it_projects_backward(self):
        client = mongomock.MongoClient()
        session = subject.start_session(client)
        session.ingest('A b. C b.')
        result = session.project_backward('b')
        assert {'a', 'c'} == result

    def test_it_projects_forward(self):
        client = mongomock.MongoClient()
        session = subject.start_session(client)
        session.ingest('A b. A c.')
        result = session.project_forward('a')
        assert {'b', 'c'} == result

    def test_it_adds_ortho(self):
        client = mongomock.MongoClient()
        collection = client.top
        s = subject.start_session(client)
        expected = ortho.create("a", "b", "c", "d")
        s.add_ortho(expected)
        result = collection.orthos.find_one({"data": expected})['data']
        assert expected == result

    def test_it_will_not_double_insert_orthos(self):
        client = mongomock.MongoClient()
        collection = client.top
        s = subject.start_session(client)
        expected = ortho.create("a", "b", "c", "d")
        s.add_ortho(expected)
        s.add_ortho(expected)
        result = len(list(collection.orthos.find({"data": expected})))

        assert 1 == result

    def test_it_can_find_an_ortho_with_a_name(self):
        client = mongomock.MongoClient()
        s = subject.start_session(client)
        expected = ortho.create("a", "b", "c", "d")
        s.add_ortho(expected)
        res = s.ortho_with_name("b")
        assert res[0] == expected

    def test_it_can_delete_a_pair_for_testing_purposes(self):
        client = mongomock.MongoClient()
        s = subject.start_session(client)
        s.ingest("a b.")
        s.delete_pair("a", "b")
        assert s.collection.pairs.find_one({"from": "a", "to": "b"}) is None


    def test_it_can_delete_an_ortho_for_testing_purposes(self):
        client = mongomock.MongoClient()
        s = subject.start_session(client)
        o = ortho.create("a", "b", "c", "d")
        s.add_ortho(o)
        s.delete_ortho(o)
        assert s.collection.orthos.find_one({"data": o}) is None
