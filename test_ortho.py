import ortho as subject


class TestOrtho:
    def test_create(self):
        result = subject.create("a", "b", "c", "d")
        expected = [['a', []], ['b', ['b']], ['c', ['c']], ['d', ['b', 'c']]]
        assert expected == result

    def test_rotation_independence(self):
        result = subject.create("a", "b", "c", "d")
        expected = subject.create("a", "c", "b", "d")
        assert expected == result

    def test_zip_up(self):
        result = subject.zip_up(subject.create("a", "b", "c", "d"), subject.create("e", "f", "g", "h"),
                                {"f": "b", "g": "c"})
        expected = [['a', []],
                    ['b', ['b']],
                    ['c', ['c']],
                    ['d', ['b', 'c']],
                    ['e', ['a']],
                    ['f', ['b', 'a']],
                    ['g', ['c', 'a']],
                    ['h', ['b', 'c', 'a']]]

        assert expected == result

    def test_get_axes(self):
        assert subject.get_axes(subject.create("a", "b", "c", "d")), ["b", "c"]

    def test_name_at_location(self):
        ortho = subject.create("a", "b", "c", "d")
        assert subject.name_at_location(ortho, ["b"]) == "b"
        assert subject.name_at_location(ortho, []) == "a"
        assert subject.name_at_location(ortho, ["b", "c"]) == "d"

    def test_get_names_as_list_of_diagonal_sets(self):
        ortho = subject.create("a", "b", "c", "d")
        assert subject.get_names_as_list_of_diagonal_sets(ortho) == [{"a"}, {"b", "c"}, {"d"}]

    def test_get_position_type_of_name(self):
        ortho = subject.create("a", "b", "c", "d")
        assert subject.position(ortho, "a") == subject.Position.ORIGIN
        assert subject.position(ortho, "b") == subject.Position.HOP
        assert subject.position(ortho, "d") == subject.Position.OTHER
