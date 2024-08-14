import re

import mock
import pytest

from glob2regex import Translator


@pytest.mark.parametrize(
    "glob,regex",
    [
        ("a", "^a$"),
        ("*", "^[^/]*$"),
        ("**", "^.*$"),
        ("*toto*", "^[^/]*toto[^/]*$"),
        ("*to*to", "^[^/]*to[^/]*to$"),
        ("\[ab", "^\[ab$"),
        ("*toto(", "^[^/]*toto\($"),
        ("**toto**", "^.*toto.*$"),
    ],
)
@mock.patch("os.name", "posix")
def test_translate(glob, regex):
    translator = Translator()

    assert translator.translate(glob) == regex


@pytest.mark.parametrize(
    "glob,s,match",
    [
        ("toto", "toto", True),
        ("toto", "totoa", False),
        ("*toto*", "atotoa", True),
        ("*toto*", "/atotoa/", False),
        ("*/*toto*/*", "/atotoa/", True),
        ("**toto**", "a/atotoa/a", True),
    ],
)
@mock.patch("os.name", "posix")
def test_regex(glob, s, match):
    translator = Translator()

    result = re.match(translator.translate(glob), s)

    if match:
        assert result
    else:
        assert not result


@pytest.mark.parametrize(
    "os_name,separator", [("posix", "/"), ("java", "/"), ("nt", "\\")]
)
def test_auto_set_separator(os_name, separator):
    with mock.patch("os.name", os_name):
        translator = Translator()

        assert translator.separator == separator


@pytest.mark.parametrize("os_name", [("posix"), ("java"), ("nt")])
def test_custom_separator(os_name):
    with mock.patch("os.name", os_name):
        translator = Translator("-")

        assert translator.separator == "-"


@pytest.mark.parametrize(
    "glob,regex",
    [
        ("a", "^a$"),
        ("*", "^[^-]*$"),
        ("**", "^.*$"),
        ("*toto*", "^[^-]*toto[^-]*$"),
        ("*to*to", "^[^-]*to[^-]*to$"),
        ("\[ab", "^\[ab$"),
        ("*toto(", "^[^-]*toto\($"),
        ("**toto**", "^.*toto.*$"),
    ],
)
@mock.patch("os.name", "posix")
def test_translator_with_custom_separator(glob, regex):
    translator = Translator("-")

    assert translator.translate(glob) == regex


@pytest.mark.parametrize(
    "glob,regex",
    [
        ("a", "^a$"),
        ("*", "^.*$"),
        ("**", "^.*$"),
        ("*toto*", "^.*toto.*$"),
        ("*to*to", "^.*to.*to$"),
        ("\[ab", "^\[ab$"),
        ("*toto(", "^.*toto\($"),
        ("**toto**", "^.*toto.*$"),
    ],
)
@mock.patch("os.name", "posix")
def test_translator_with_empty_separator(glob, regex):
    translator = Translator("")

    assert translator.translate(glob) == regex
