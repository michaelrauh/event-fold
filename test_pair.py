import unittest
import mongomock
import pair as subject

import session


class MyTestCase(unittest.TestCase):
    def test_it_attempts_forward_ex_nihilo(self):
        client = mongomock.MongoClient()
        collection = client.top
        session = ingestor.start_session(client)
        session.ingest('a b. c d. a c. b d.')
        subject.new_pair(session, "b", "d")
        ortho = [{"": "a"}, {"b": "b"}, {"c": "c"}, {"b.c": "d"}]
        self.assertEqual(ortho, collection.orthos.find_one(ortho)['data'])

# todo it ignores preexisting orthos even if they are rotated

# todo these can come in any order, and in any forward/backward layout that makes 8 cases

# a b
# c d

# a c
# b d


if __name__ == '__main__':
    unittest.main()
