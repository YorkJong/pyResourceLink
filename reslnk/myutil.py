# -*- coding: utf-8 -*-
"""
This module put my utility functions
"""
__author__ = "Jiang Yu-Kuan <yukuan.jiang@gmail.com>"
__date__ = "2016/02/08 (initial version) ~ 2016/04/27 (last revision)"

import re
import os
import sys


#------------------------------------------------------------------------------
# File
#------------------------------------------------------------------------------

def save_utf8_file(fn, lines):
    """Save string lines into an UTF8 text files.
    """
    with open(fn, "w") as out_file:
        out_file.write("\n".join(lines).encode("utf-8"))


def main_basename(path):
    r"""Return a main name of a basename of a given file path.

    Example
    -------
    >>> main_basename('c:\code\langconv\MsgID.h')
    'MsgID.h'
    """
    base = os.path.basename(path)
    base_main, _base_ext = os.path.splitext(base)
    return base_main


#------------------------------------------------------------------------------
# Math
#------------------------------------------------------------------------------

def is_numeric(str):
    try:
        _offset = int(eval(str))
    except:
        return False
    return True


#------------------------------------------------------------------------------
# String
#------------------------------------------------------------------------------

def replace_chars(text, replaced_pairs='', deleted_chars=''):
    """Return a char replaced text.

    Arguments
    ---------
    text -- the text
    replaced_pairs -- the replaced chars

    Example
    -------
    >>> replaced = [('a','b'), ('c','d')]
    >>> removed = 'e'
    >>> replace_chars('abcde', replaced, removed)
    'bbdd'
    """
    for old, new in replaced_pairs:
        text = text.replace(old, new)
    for ch in deleted_chars:
        text = text.replace(ch, '')
    return text


def camel_case(string):
    """Return camel case string from a space-separated string.

    Example
    -------
    >>> camel_case('good job')
    'GoodJob'
    """
    return ''.join(w.capitalize() for w in string.split())


def replace_punctuations(text):
    """Replace punctuation characters with abbreviations for a string.
    """
    punctuations = [
        ('?', 'Q'),   # Q:  question mark
        ('.', 'P'),   # P:  period; full stop
        ('!', 'E'),   # E:  exclamation mark
        ("'", 'SQ'),  # SQ: single quotation mark; single quote
        ('"', 'DQ'),  # DQ: double quotation mark; double quotes
        ('(', 'LP'),  # LP: left parenthese
        (')', 'RP'),  # RP: right parenthese
        (':', 'Cn'),  # Cn: colon
        (',', 'Ca'),  # Ca: comma
        (';', 'S'),   # S:  semicolon
    ]
    deleted = '+-*/^=%$#@|\\<>{}[]'
    return replace_chars(text, punctuations, deleted)


def remain_alnum(text):
    """Remain digits and English letters of a string.
    """
    return ''.join(c for c in text if c.isalnum()
                                   and ord(' ') <= ord(c) <= ord('z'))


#------------------------------------------------------------------------------
# For code generation
#------------------------------------------------------------------------------

def c_identifier(text):
    """Convert input text into an legal identifier in C.

    Example
    -------
    >>> c_identifier("Hello World")
    'HelloWorld'
    >>> c_identifier("Anti-Shake")
    'Antishake'
    """
    if ' ' in text:
        text = camel_case(text)
    text = re.sub(r'\+\d+', lambda x: x.group().replace('+', 'P'), text)
    text = re.sub(r'\-\d+', lambda x: x.group().replace('-', 'N'), text)
    text = replace_punctuations(text)
    return remain_alnum(text)


def wrap_header_guard(lines, h_fn):
    """Wrap a C header guard for a given line list.
    """
    def underscore(txt):
        """Return an under_scores text from a CamelCase text.

        This function will leave a CamelCase text unchanged.
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', txt)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    h_fn_sig = '_%s_H' % underscore(main_basename(h_fn)).upper()
    begin = ['#ifndef %s' % h_fn_sig]
    begin += ['#define %s' % h_fn_sig, '', '']
    end = ['', '', '#endif // %s' % h_fn_sig, '']
    return begin + lines + end


def prefix_info(lines, software, version, author, comment_mark='//'):
    """Prefix information to the given lines with given comment-mark.
    """
    prefix = ['%s Generated by the %s v%s' % (comment_mark,
              software, version)]
    prefix += ['%s    !author: %s' % (comment_mark, author)]
    prefix += ['%s    !trail: %s %s' % (comment_mark,
               os.path.basename(sys.argv[0]), ' '.join(sys.argv[1:]))]
    return prefix + lines



