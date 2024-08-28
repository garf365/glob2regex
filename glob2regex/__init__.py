"""
Glob2Regex library, for globber which want powerfull of regex
"""

from .translator import Translator  # noqa


def glob2regex(pattern: str, separator: str = None, strict: bool = True):
    """Translate the given glob pattern into regex form, using custom separator.
    If no seperator is given, glob2regex will use file separator according operating
    system: "\\" for Windows, "/" for every other (real) systems

    >>> glob2regex("*toto*")
    '^[^/]*toto[^/]*$'
    >>> glob2regex("*toto*", "")
    '^.*toto.*$'

    :param str pattern: Glob pattern to translate
    :param str separator: Separator to be used. Use file separator if not given. For no
                          separator, simply passe empty string
    :param bool strict: Enable strict mode, ie string should exactly match pattern. In
                        term of regex, pattern starts with `^` and ends with `$`
    :returns: regex equivalent to glob pattern
    :rtype: str
    """
    translator = Translator(separator)
    return translator.translate(pattern, strict)


def match(pattern: str, string: str, separator: str = None, strict: bool = True):
    """Return a re.Match object for string given, using glob pattern

    >>> match("t*to", "toto")
    <re.Match object; span=(0, 4), match='toto'>
    >>> match("t*to, "alpha")
    None

    :param str pattern: Glob pattern to use
    :param str string: String to match
    :param str separator: Separator to be used. Use file separator if not given. For no
                          separator, simply passe empty string
    :returns: re.Match if string match glob pattern, otherwise None
    :rtype: re.Match or None
    """
    import re

    return re.match(glob2regex(pattern, separator, strict), string)


def compile(pattern: str, separator: str = None, strict: bool = True):
    """Return a re.Pattern object for glob pattern given. Indeed, result of
    this function can be used exactly as result of re.compile

    >>> pattern = compile("t*to")
    >>> pattern.match("toto")
    <re.Match object; span=(0, 4), match='toto'>
    >>> pattern.findall("toto")
    ['toto']

    >>> pattern = compile("t?t?", " ", strict = False)
    >>> pattern.findall("toto alpha tata beta tototo")
    ['toto', 'tata']

    :param str pattern: Glob pattern to compile
    :param str separator: Separator to be used. Use file separator if not given. For no
                          separator, simply passe empty string
    :returns: Compiled glob pattern, useable like result of re.compile
    :rtype: re.Pattern
    """
    import re

    return re.compile(glob2regex(pattern, separator, strict))
