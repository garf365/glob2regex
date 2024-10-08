"""
Translator
Based on https://en.wikipedia.org/wiki/Glob_(programming), using UNIX-like
"""

import os


class Translator:
    #: Default separator for windows based system
    DEFAULT_SEPARATOR_WINDOWS = "\\"
    #: Default separator for everyone else
    DEFAULT_SEPARATOR_UNIX = "/"

    def __init__(self, separator: str = None):
        """Constructor of translator

        :param str separator: Separator to be used. Use file separator if not given.
                              For no separator, simply passe empty string
        """
        if separator is not None:
            self.separator = separator
        elif os.name == "nt":
            self.separator = Translator.DEFAULT_SEPARATOR_WINDOWS
        else:
            self.separator = Translator.DEFAULT_SEPARATOR_UNIX

        self._init_translator()

    def _init_translator(self):
        """Internal function to reinit translator for new translation"""
        self.is_next_escaped = False
        self.is_previous_wildcard = False
        self.is_previous_open_bracket = False
        self.is_in_bracket = False

    def translate(self, glob: str, strict: bool = True):
        """Translate glob pattern to regex pattern

        :param str glob: Glob pattern to translate
        :param bool strict: Enable strict mode, ie string should exactly match pattern.
                            In term of regex, pattern starts with `^` and ends with `$`
        :returns: Regex equivalent of given glob pattern
        :rtype: str
        """
        if not isinstance(glob, str):
            raise ValueError("glob should be a string")

        self._init_translator()
        result = r"^" if strict else r""

        for c in glob:
            if self.is_next_escaped:
                if c in "\\*?[]":
                    result += "\\" + c
                else:
                    result += "\\\\" + c
                self.is_next_escaped = False
            elif self.is_previous_wildcard:
                if c == "*":
                    result += ".*"
                elif not self.separator:
                    result += ".*" + c
                else:
                    result += f"[^{self.separator}]*{c}"
                self.is_previous_wildcard = False
            elif c == "\\":
                self.is_next_escaped = True
            elif c == "*":
                self.is_previous_wildcard = True
            elif c == "?":
                result += "."
            elif c == "[":
                if not self.is_in_bracket:
                    self.is_previous_open_bracket = True
                self.is_in_bracket = True
                result += "["
            elif c == "]":
                self.is_in_bracket = False
                result += "]"
            elif c == "!":
                if self.is_previous_open_bracket:
                    result += "^"
                else:
                    result += "!"
            elif c in ".^$+(){}|":
                result += "\\" + c
            else:
                result += c

            if c != "[":
                self.is_previous_open_bracket = False

        if self.is_next_escaped:
            result += "\\"
        elif self.is_previous_wildcard:
            if self.separator:
                result += f"[^{self.separator}]*"
            else:
                result += ".*"

        if strict:
            return result + "$"

        return "(" + result + r")\W"
