import mongomock
import pytest

import ortho
import pair as subject
import session


@pytest.fixture
def current_session(client):
    return session.start_session(client)


@pytest.fixture
def collection(client):
    return client.top


@pytest.fixture
def client():
    return mongomock.MongoClient()


class TestPair:
    def test_it_attempts_b_d_ex_nihilo(self, current_session, collection):
        current_session.ingest('A b.')
        current_session.ingest('C d.')
        current_session.ingest('A c.')
        current_session.ingest('B d.')
        subject.new_pair(current_session, "b", "d")
        o = ortho.create("a", "b", "c", "d")
        assert o == current_session.get_one_ortho()

    def test_it_attempts_a_b_ex_nihilo(self, current_session, collection):
        current_session.ingest('C d.')
        current_session.ingest('A c.')
        current_session.ingest('B d.')
        current_session.ingest('A b.')
        subject.new_pair(current_session, "a", "b")
        o = ortho.create("a", "b", "c", "d")
        assert o == current_session.get_one_ortho()

    def test_it_attempts_c_d_ex_nihilo(self, current_session, collection):
        current_session.ingest('A c.')
        current_session.ingest('B d.')
        current_session.ingest('A b.')
        current_session.ingest('C d.')
        subject.new_pair(current_session, "c", "d")
        o = ortho.create("a", "b", "c", "d")
        assert o == current_session.get_one_ortho()

    def test_it_attempts_a_c_ex_nihilo(self, current_session, collection):
        current_session.ingest('B d.')
        current_session.ingest('A b.')
        current_session.ingest('C d.')
        current_session.ingest('A c.')
        subject.new_pair(current_session, "a", "c")
        o = ortho.create("a", "b", "c", "d")
        assert o == current_session.get_one_ortho()

    def test_it_attempts_an_up_using_a_pair_and_existing_orthos_using_origin_projection(self, current_session, collection):
        # todo insert base check for up

        # insert l ortho
        current_session.ingest('a b.')
        current_session.ingest('c d.')
        current_session.ingest('a c.')
        current_session.ingest('b d.')
        subject.new_pair(current_session, "b", "d")

        # insert r ortho
        current_session.ingest('e f.')
        current_session.ingest('g h.')
        current_session.ingest('e g.')
        current_session.ingest('f h.')
        subject.new_pair(current_session, "f", "h")

        # insert up ortho with origin mapping coming last
        left = ortho.create("a", "b", "c", "d")
        right = ortho.create("e", "f", "g", "h")
        o = ortho.zip_up(left, right, {"f": "b", "g": "c"})
        current_session.ingest('b f')
        current_session.ingest('c g')
        current_session.ingest('d h')
        current_session.ingest('a e')
        subject.new_pair(current_session, "a", "e")

        assert o == current_session.get_matching_ortho(o)

# TODO:
# non-base dimension
# different shapes
# hop projection
# same projected coordinate
# location category mismatch
# coordinate mismatch
# coords are good but projection fails
# hit with a late miss (another pair is missing)