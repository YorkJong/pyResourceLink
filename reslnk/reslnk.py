# -*- coding: utf-8 -*-
"""
The main goal of ResLnk is to link resource files into single one.

"""
__software__ = "Resource Link"
__version__ = "0.01"
__author__ = "Jiang Yu-Kuan <york_jiang@mars-semi.com.tw>"
__date__ = "2013/02/26 (initial version) ~ 2013/02/26 (last revision)"

import os
import sys
import argparse


def read_map_file(fn):
    """Read a resource map file and return a file with description list.
    """
    def del_nonuse(lines):
        lines = (x.split("#", 1)[0].strip() for x in lines)
        return [x for x in lines if len(x) > 0]

    with open(fn) as f:
        lines = del_nonuse(f.read().splitlines())

    # check :offset lines
    for line in lines:
        if line.startswith(':'):
            try:
                offset = int(eval(line[1:]))
            except:
                raise ValueError('offset error -> %s' % line)
    return lines


#-----------------------------------------------------------------------------

def offset_filename_pairs(lines, res_dir='.'):
    pairs = []
    offset = 0
    for line in lines:
        if line.startswith(':'):
            val = eval(line[1:])
            if val < offset:
                raise ValueError('offset too small -> %s' % line)
            offset = val
        else:
            fn = '{path}/{name}'.format(path=res_dir, name=line)
            pairs += [(offset, line)]
            fsize = os.path.getsize(fn)
            offset += fsize
    return pairs

#-----------------------------------------------------------------------------

def link(lines, res_dir='.', outfile='res.bin'):
    """Link resources into single file.
    """
    pairs = offset_filename_pairs(lines, res_dir)
    print pairs


def gen_offset_ifile(lines, res_dir='.', outfile='res_offset.i'):
    """Generate a C included file that lists offsets of resources.
    """
    pass


def gen_id_hfile(lines, outfile=''):
    """Generate a C header file of resource ID enumeration.
    """
    pass

#-----------------------------------------------------------------------------

def parse_args(args):
    def do_link(args):
        link(args.lines, args.dir, args.outfile)

    def do_offset(args):
        gen_offset_ifile(args.lines, args.dir, args.outfile)

    def do_id(args):
        gen_id_hfile(args.lines, args.outfile)

    # create top-level parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--version', action='version',
                        version='%s v%s by %s' %
                        (__software__, __version__, __author__))
    subparsers = parser.add_subparsers(help='commands')

    #--------------------------------------------------------------------------

    # create the parent parser of resource map file
    src = argparse.ArgumentParser(add_help=False)
    src.add_argument('lines', metavar='map-file',
        type=read_map_file,
        help='The map file of resources.')

    # create the parent parser of resource directory
    dir = argparse.ArgumentParser(add_help=False)
    dir.set_defaults(dir='.')
    dir.add_argument('-d', '--dir', metavar='<directory>',
        help="""assign the <directory> to read resource files.
            The default directory is "%s".
            """ % dir.get_default('dir'))

    # create the parser for the "link" command
    sub = subparsers.add_parser('link', parents=[src, dir],
        help='link resource files into single one.')
    sub.set_defaults(func=do_link,
        outfile='res.bin')
    sub.add_argument('-o', '--output', metavar='<file>', dest='outfile',
        help='''place the output into <file>, the file after linking
            (default "%s").
            ''' % sub.get_default('outfile'))

    # create the parser for the "offset" command
    sub = subparsers.add_parser('offset', parents=[src, dir],
        help='generate a C included file listing byte offsets of resources.')
    sub.set_defaults(func=do_offset,
        outfile='res_offset.i')
    sub.add_argument('-o', '--output', metavar='<file>', dest='outfile',
        help='''place the output into <file>, the C included file listing
            the offsets (default "%s").
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
    parse_args(sys.argv[1:])
    #main()

