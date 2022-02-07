import unittest
import ortho as subject


class MyTestCase(unittest.TestCase):
    def test_create(self):
        result = subject.create("a", "b", "c", "d")
        expected = [['a', []], ['b', ['b']], ['c', ['c']], ['d', ['b', 'c']]]
        self.assertEqual(expected, result)

    def test_rotation_independence(self):
        result = subject.create("a", "b", "c", "d")
        expected = subject.create("a", "c", "b", "d")
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
