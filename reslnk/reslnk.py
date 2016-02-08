# -*- coding: utf-8 -*-
"""
The main goal of ResLnk (Resource Link) is to link resource files into single
one (link command). It provides map command to generate resource map file in C
array style, id command to generate a C header file of resource ID enumeration.
It also provids additional commmands (e.g. checksum, and filesize) for the USB
boot and the bootloading on A1016 ICs.
"""
__software__ = "Resource Link"
__version__ = "1.14"
__author__ = "Jiang Yu-Kuan <yukuan.jiang@gmail.com>"
__date__ = "2013/02/26 (initial version) ~ 2016/02/08 (last revision)"

import os
import sys
import re
import argparse

from myutil import *


#-----------------------------------------------------------------------------
# File Read
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


#-----------------------------------------------------------------------------
# Misc
#-----------------------------------------------------------------------------

def prefix_authorship(lines, comment_mark='//'):
    """Prefix authorship infomation to the given lines
    with given comment-mark.
    """
    return prefix_info(lines,
                       __software__, __version__, __author__,
                       comment_mark)


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
# Action Functions
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
# Command Line Interface
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

