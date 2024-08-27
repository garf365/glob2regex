import mock
import pytest

from glob2regex import glob2regex
from glob2regex import match


@mock.patch("glob2regex.Translator", autospec=True)
@mock.patch("os.name", "posix")
def test_helper_glob2regex(mock_translator_init):
    mock_translator = mock.MagicMock()
    mock_translator.translate = mock.Mock(return_value="mocked_value")
    mock_translator_init.return_value = mock_translator

    res = glob2regex("value")

    assert res == "mocked_value"

    mock_translator_init.assert_called_with(None)
    mock_translator.translate.assert_called_with("value")


@mock.patch("glob2regex.Translator", autospec=True)
@mock.patch("os.name", "posix")
def test_helper_glob2regex_with_custom_separator(mock_translator_init):
    mock_translator = mock.MagicMock()
    mock_translator.translate = mock.Mock(return_value="mocked_value")
    mock_translator_init.return_value = mock_translator

    res = glob2regex("value", "sep")

    assert res == "mocked_value"

    mock_translator_init.assert_called_with("sep")
    mock_translator.translate.assert_called_with("value")


@pytest.mark.parametrize(
    "pattern,value,expected",
    [
        ("toto", "toto", True),
        ("*tot*", "toto", True),
        ("toto", "tutu", False),
        ("t*to", "toto", True),
        ("t*to", "tato", True),
        ("t*to", "tata", False),
    ],
)
@mock.patch("os.name", "posix")
def test_helper_match(pattern, value, expected):
    import re

    if expected:
        assert isinstance(match(pattern, value), re.Match)
    else:
        assert match(pattern, value) is None
