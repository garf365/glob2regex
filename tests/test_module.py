import re

import mock

from glob2regex import compile
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

    mock_translator_init.assert_called_once_with(None)
    mock_translator.translate.assert_called_once_with("value", True)


@mock.patch("glob2regex.Translator", autospec=True)
@mock.patch("os.name", "posix")
def test_helper_glob2regex_with_custom_separator(mock_translator_init):
    mock_translator = mock.MagicMock()
    mock_translator.translate = mock.Mock(return_value="mocked_value")
    mock_translator_init.return_value = mock_translator

    res = glob2regex("value", "sep")

    assert res == "mocked_value"

    mock_translator_init.assert_called_once_with("sep")
    mock_translator.translate.assert_called_once_with("value", True)


@mock.patch("re.match")
@mock.patch("glob2regex.glob2regex")
def test_helper_match(mock_glob2regex, mock_re_match):
    mock_glob2regex.return_value = "mocked_value"
    mock_re_match.return_value = "result"

    assert match("t*to", "toto", "sep", False) == "result"

    mock_re_match.assert_called_once_with("mocked_value", "toto")
    mock_glob2regex.assert_called_once_with("t*to", "sep", False)


@mock.patch("glob2regex.glob2regex")
def test_helper_compile(mock_glob2regex):
    mock_glob2regex.return_value = "mocked_value"

    assert isinstance(compile("t*to", "sep", False), re.Pattern)

    mock_glob2regex.assert_called_once_with("t*to", "sep", False)
