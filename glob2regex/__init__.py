from .translator import Translator  # noqa


def glob2regex(pattern: str, separator: str = None):
    translator = Translator(separator)
    return translator.translate(pattern)


def match(pattern: str, string: str, separator: str = None):
    import re

    return re.match(glob2regex(pattern, separator), string)


def compile(pattern: str, separator: str = None):
    import re

    return re.compile(glob2regex(pattern, separator))
