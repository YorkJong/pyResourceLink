# -*- coding: utf-8 -*-
"""
The main goal of ResLnk (Resource Link) is to link resource files into single
one (link command). It provides map command to generate resource map file in C
array style, id command to generate a C header file of resource ID enumeration.
It also provids additional commmands (e.g. checksum, and filesize) for the USB
boot and the bootloading on A1016 ICs.
"""
__software__ = "Resource Link"
__version__ = "1.13"
__author__ = "Jiang Yu-Kuan <yukuan.jiang@gmail.com>"
__date__ = "2013/02/26 (initial version) ~ 2015/04/07 (last revision)"

import os
import sys
import re
import hashlib
import argparse


#-----------------------------------------------------------------------------

def save_utf8_file(fn, lines):
    """Save string lines into an UTF8 text files.
    """
    out_file = open(fn, 'w')
    out_file.write("\n".join(lines).encode('utf-8'))
    out_file.close()


def prefix_authorship(lines, comment_mark='//'):
    """Prefix authorship infomation to the given lines
    with given comment-mark.
    """
    prefix = ['%s Generated by the %s v%s' % (comment_mark,
              __software__, __version__)]
    prefix += ['%s    !author: %s' % (comment_mark, __author__)]
    prefix += ['%s    !trail: %s %s' % (comment_mark,
               os.path.basename(sys.argv[0]), ' '.join(sys.argv[1:]))]
    return prefix + lines


def main_basename(path):
    """Return a main name of a basename of a given file path.

    Example
    -------
    >>> main_basename('c:\code\langconv\MsgID.h')
    'MsgID.h'
    """
    base = os.path.basename(path)
    base_main, base_ext = os.path.splitext(base)
    return base_main


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


#-----------------------------------------------------------------------------

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


#-----------------------------------------------------------------------------

def is_numeric(str):
    try:
        offset = int(eval(str))
    except:
        return False
    return True


#-----------------------------------------------------------------------------

def read_lst_file(fn):
    """Read a resource map file and return statement list.
    """
    def del_nonuse(lines):
        lines = (x.split("#", 1)[0].strip() for x in lines)
        return [x for x in lines if len(x) > 0]

    with open(fn) as f:
        lines = del_nonuse(f.read().splitlines())

    kind_cmd_pattern = re.compile(':\s*kind\s*=')
    for line in lines:
        if not line.startswith(':'):        # check filename
            continue
        if kind_cmd_pattern.match(line):    # check :kind command
            continue
        if is_numeric(line[1:]):            # check :offset
            continue
        raise ValueError('syntax error -> %s' % line)
    return lines


def res_id_from_filename(fn):
    """Return resource ID from filename.
    """
    base = os.path.basename(fn)
    base_main, base_ext = os.path.splitext(base)
    return 'RES_%s_%s' % (c_identifier(base_ext[1:]).upper(),
                          c_identifier(base_main.replace('_', ' ')))


def map_from_statements(statements, res_dir='res', align_bytes=1):
    """Return (offset, size, filename) tuples from statements.
    """
    assert align_bytes >= 1

    tuples = []
    offset = 0
    for sta in statements:
        if sta.startswith(':'):
            if not is_numeric(sta[1:]):
                continue
            val = eval(sta[1:])
            if val < offset:
                raise ValueError('offset too small -> %s' % sta)
            offset = val
        else:
            fn = '{path}/{name}'.format(path=res_dir, name=sta)
            fsize = os.path.getsize(fn)
            tuples += [(offset, fsize, sta)]
            offset += fsize
            offset = (offset + align_bytes - 1) / align_bytes * align_bytes
    return tuples


#-----------------------------------------------------------------------------

def link(statements, res_dir='res', outfile='res.bin',
        align_bytes=1, padding_hex=0xFF):
    """Link resources into single file.
    """
    assert padding_hex <= 0xFF
    assert align_bytes >= 1

    begins, sizes, fns = zip(
        *map_from_statements(statements, res_dir, align_bytes))
    ends = list(begins[1:]) + [begins[-1] + sizes[-1]]
    spaces = [end - begin for begin, end in zip(begins, ends)]

    with open(outfile, 'wb') as outfile:
        for space, fn in zip(spaces, fns):
            fn = '{path}/{name}'.format(path=res_dir, name=fn)
            with open(fn, 'rb') as infile:
                raw = infile.read()
            padding = chr(padding_hex) * (space - len(raw))
            outfile.write(raw + padding)


def gen_map_ifile(statements,
                  res_dir='res', outfile='ResMap.i', align_bytes=1):
    """Generate a C included file that lists map of resources.
    """
    assert align_bytes >= 1

    lines = ['']
    lines += ['// %8s,   %8s     (in bytes)' % ('offset', 'size')]
    lines += ['{  %8d,   %8d},   // %s (%s)'
            % (offset, size, res_id_from_filename(fn), fn)
            for offset, size, fn
            in map_from_statements(statements, res_dir, align_bytes)]
    lines += ['']

    lines = prefix_authorship(lines)
    save_utf8_file(outfile, lines)


def gen_map_binfile(statements,
                    res_dir='res', outfile='ResMap.bin', align_bytes=1):
    """Generate a binary map file of resources.
    """
    def str_from_val(x):
        """"Return char-string from a two-byte value (high byte first)."""
        return (chr((x >> 24) & 0xff) +
                chr((x >> 16) & 0xff) +
                chr((x >> 8) & 0xff) +
                chr(x & 0xff))

    assert align_bytes >= 1

    lines = []
    for offset, size, fn in map_from_statements(statements, res_dir, align_bytes):
        lines += [str_from_val(offset), str_from_val(size)]
    bytes = 'ResMapTb' + ''.join(lines)

    with open(outfile, 'wb') as f:
        f.write(bytes)


def gen_id_hfile(statements, h_fn='ResID.h'):
    """Generate a C header file of resource ID enumeration.
    """
    def group_filenames(statements):
        def is_kept(sta):
            if sta.strip() == '':
                return False
            if not sta.startswith(':'):
                return True
            if re.match(':\s*kind\s*=', sta):
                return True
            return False

        def delete_space_lines(lines):
            return (line for line in lines if line != '')

        statements = [sta for sta in statements if is_kept(sta)]
        statements += ['']      # for last empty kind statement
        lines = '\n'.join(statements)
        kinds = re.findall(r':\s*kind\s*=\s*(.*)\s*\n', lines)
        fns_lst = re.split(r':\s*kind\s*=.*\n', lines)
        if statements[0].startswith(':'):
            fns_lst = fns_lst[1:]
        else:
            kinds = [''] + kinds
        fns_lst = (delete_space_lines(lines.split('\n')) for lines in fns_lst)
        return zip(kinds, fns_lst)

    def lines_from_fns(kind, fns, id_end):
        ids = [res_id_from_filename(fn) for fn in fns]
        id_begin = res_id_from_filename('BEGIN.' + kind)

        lines = []
        if id_end == '':
            lines += ['    %s,' % id_begin]
        else:
            lines += ['    %s = %s,' % (id_begin, id_end)]
        id_end = res_id_from_filename('END.' + kind)
        if ids:
            lines += ['    %s = %s,' % (ids[0], id_begin)]
            lines += ['    %s,' % id for id in ids[1:]]
            lines += ['    %s,' % id_end]
        else:
            lines += ['    %s = %s,' % (id_end, id_begin)]
        lines += ['']
        return lines, id_end

    lines = ['/** IDs of Resources */']
    lines += ["typedef enum {"]

    id_end = ''
    for kind, fns in group_filenames(statements):
        tmp_lines, id_end = lines_from_fns(kind, fns, id_end)
        lines += tmp_lines

    lines += ['    RES_End = %s,' % id_end]
    lines += ['    RES_Total = RES_End']
    lines += ['} ResID;']

    lines = wrap_header_guard(lines, h_fn)
    lines = prefix_authorship(lines, comment_mark='//')
    save_utf8_file(h_fn, lines)

#-----------------------------------------------------------------------------

ords = lambda x: [ord(c) for c in x]
delittle = lambda x: x[0] | (x[1]<<8) | (x[2]<<16) | (x[3]<<24)
unpack = lambda x: delittle(ords(x))

belittle = lambda x: (x&0xFF, (x>>8)&0xFF, (x>>16)&0xFF, (x>>24)&0xFF)
chrs = lambda x: [chr(v) for v in x]
pack = lambda x: ''.join(chrs(belittle(x)))


def gen_checksum_headerfile(in_fn, out_fn):
    """Generate a checksum header file for booting from USB on A1016.
    It also generates a MD5 checksum for ISP file checking.
    """
    def calc_checksum(data):
        values = [unpack(data[i:i+4]) for i in xrange(0, len(data), 4)]
        checksum = 0xFFFFFFFF - (sum(values) & 0xFFFFFFFF)
        return pack(checksum)

    CHECK_LEN = 13 * 512
    filesize = os.path.getsize(in_fn)
    with open(in_fn, 'rb') as f:
        check_str = calc_checksum(f.read(CHECK_LEN))
    with open(in_fn, 'rb') as f:
        md5_str = hashlib.md5(f.read()).hexdigest()

    len_str = pack(256 + filesize)
    data = ''.join([chr(0) * 0x20,
                    'SRAM6101', chr(0) * 24,
                    check_str,  chr(0) * 28,
                    len_str, chr(0) * 60,
                    md5_str, chr(0) * 64])
    assert len(data) == 256
    with open(out_fn, 'wb') as f:
        f.write(data)


def gen_filesize_binaryfile(in_fn, out_fn):
    """Generate a file-size header file (4-byte file-size in a 256-byte header
    ).
    """
    filesize = os.path.getsize(in_fn)
    data = pack(filesize) + chr(0) * (256 - 4)

    with open(out_fn, 'wb') as f:
        f.write(data)


#-----------------------------------------------------------------------------

def parse_args(args):
    def do_link(args):
        link(args.statements, args.dir, args.outfile, args.align, args.padding)

    def do_map(args):
        gen_map_ifile(args.statements, args.dir, args.outfile, args.align)

    def do_bmap(args):
        gen_map_binfile(args.statements, args.dir, args.outfile, args.align)

    def do_id(args):
        gen_id_hfile(args.statements, args.outfile)

    def do_checksum(args):
        gen_checksum_headerfile(args.infile, args.outfile)

    def do_filesize(args):
        gen_filesize_binaryfile(args.infile, args.outfile)

    def hex_check(value):
        value = int(eval(value))
        assert value < 256
        return value

    # create top-level parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--version', action='version',
                        version='%s v%s by %s' %
                        (__software__, __version__, __author__))
    subparsers = parser.add_subparsers(help='commands')

    #--------------------------------------------------------------------------

    # create the parent parser of resource map file
    src = argparse.ArgumentParser(add_help=False)
    src.add_argument('statements', metavar='lst-file',
        type=read_lst_file,
        help='The list file of resources.')

    # create the parent parser of resource directory
    dir = argparse.ArgumentParser(add_help=False)
    dir.set_defaults(dir='.')
    dir.add_argument('-d', '--dir', metavar='<directory>',
        help="""assign the <directory> to read resource files.
            The default directory is "%s".
            """ % dir.get_default('dir'))

    # create the parent parser of align bytes
    aln = argparse.ArgumentParser(add_help=False)
    aln.set_defaults(align=1)
    aln.add_argument('-a', '--align', metavar='<number>',
        type=int, choices=(1, 2, 4, 8, 16, 32, 64, 128, 256),
        help="""specify the <number> of alignment bytes
            (default "%d").
            """ % aln.get_default('align'))

    # create the parser for the "link" command
    sub = subparsers.add_parser('link', parents=[src, dir, aln],
        help='link resource files into single one.')
    sub.set_defaults(func=do_link,
        outfile='res.bin', padding=0xFF)
    sub.add_argument('-p', '--padding', metavar='<char hex>', type=hex_check,
        help='''specify the padding hex value of a char (default "0x%X").
            ''' % sub.get_default('padding'))
    sub.add_argument('-o', '--output', metavar='<file>', dest='outfile',
        help='''place the output into <file>, the file after linking
            (default "%s").
            ''' % sub.get_default('outfile'))

    # create the parser for the "map" command
    sub = subparsers.add_parser('map', parents=[src, dir, aln],
        help='generate a resource map file in format of C array.')
    sub.set_defaults(func=do_map,
        outfile='ResMap.i')
    sub.add_argument('-o', '--output', metavar='<file>', dest='outfile',
        help='''place the output into <file>, the C included file listing
            the offset, size pairs (default "%s").
            ''' % sub.get_default('outfile'))

    # create the parser for the "bmap" command
    sub = subparsers.add_parser('bmap', parents=[src, dir, aln],
        help='generate a resource map file in binary format.')
    sub.set_defaults(func=do_bmap,
        outfile='ResMap.bin')
    sub.add_argument('-o', '--output', metavar='<file>', dest='outfile',
        help='''place the output into <file>, the binary version of resource
            map file listing the offset, size pairs (default "%s").
            ''' % sub.get_default('outfile'))

    # create the parser for the "id" command
    sub = subparsers.add_parser('id', parents=[src],
        help='generate a C header file of resource ID enumeration.')
    sub.set_defaults(func=do_id,
        outfile='ResID.h')
    sub.add_argument('-o', '--output', metavar='<file>', dest='outfile',
        help='''place the output into <file>, the C header file of
            resource ID enumeration (default "%s").
            ''' % sub.get_default('outfile'))

    #--------------------------------------------------------------------------

    # create the parser for the "checksum" command
    sub = subparsers.add_parser('checksum',
        help='generate a checksum header file for the USB boot on A1016.')
    sub.set_defaults(func=do_checksum,
        infile='fw.bin', outfile='checksum.bin')
    sub.add_argument('infile', metavar='binary-file',
        help='''The firmware binary file used to calculate checksum and
            filesize fields of the USB ISP header''')
    sub.add_argument('-o', '--output', metavar='<file>', dest='outfile',
        help='''place the output into <file>, the checksum header file
            (default "%s").
            ''' % sub.get_default('outfile'))

    # create the parser of the "filesize" command
    sub = subparsers.add_parser('filesize',
        help='''generate a file-size header file (4-byte file-size in a
            256-byte header).''')
    sub.set_defaults(func=do_filesize,
        infile='fw.bin', outfile='filesize.bin')
    sub.add_argument('infile', metavar='binary-file',
        help='''The firmware binary file used to calculate file-size''')
    sub.add_argument('-o', '--output', metavar='<file>', dest='outfile',
        help='''place the output into <file>, the file-size header file
            (default "%s").
            ''' % sub.get_default('outfile'))

    #--------------------------------------------------------------------------

    # parse args and execute functions
    args = parser.parse_args(args)
    args.func(args)


def main():
    """Start point of this module.
    """
    try:
        parse_args(sys.argv[1:])
    except IOError as err:
        print err
    except ValueError as err:
        print err
    except KeyError as key:
        print 'KeyError:', key


if __name__ == '__main__':
    main()
    #parse_args(sys.argv[1:])
    #gen_checksum_headerfile('noheader.bin', 'usbheader.bin')

