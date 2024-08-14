import pytest
import mock

from glob2regex import Translator

@pytest.mark.parametrize("glob,regex", [
        ("a","a"),
        ("*", "[^/]*"),
        ("**", ".*"),
        ("*toto*", "[^/]*toto[^/]*"),
        ("*to*to", "[^/]*to[^/]*to"),
        ("\[ab", "\[ab"),
        ("*toto(", "[^/]*toto\(")
])
@mock.patch('os.name', 'posix')
def test_translate(glob, regex):
    translator = Translator()

    assert translator.translate(glob) == regex

@pytest.mark.parametrize("os_name,separator",[
    ("posix", "/"),
    ("java", "/"),
    ("nt", "\\")
])
def test_auto_set_separator(os_name, separator):
    with mock.patch('os.name', os_name):
        translator = Translator()

        assert translator.separator == separator




