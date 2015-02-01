#!/usr/bin/python

## Author: 	Luke Caldwell
## Org: Duke University S-1 Speculative Sensation Lab
## Website: http://s-1lab.org
## License: Creative Commons BY-NC-SA 4.0
##			http://creativecommons.org/licenses/by-nc-sa/4.0/

"""
run using:
python (path_to)/parse_ip.py

replace (path_to) with the full path
---------------
creates an .xyz 3d-model @  ./tcpflow_parse.xyz
from IP address data
or
creates a list of filenames for uploading to the website
---------------
options:
-t outputs a text file for uploading to the website for
    creation of a google map
-i allows for nonstandard input directory. Default is ./tcpflow
-o allows for the specification of nonstandard output file.
-v displays more information to the console.

"""
from __future__ import print_function
import os
import glob
import re
import random
from argparse import ArgumentParser
from datetime import datetime


BASE_DIR = os.path.dirname(__file__)
DATE = datetime.now().strftime('%m-%d-%Y')

parser = ArgumentParser()
parser.add_argument('-t', '--text', dest="txt", action="store_true",
                    default=False, help="outputs text file for geolocation")
parser.add_argument('-i', '--input', dest="input", action="store",
                    default=os.path.join(BASE_DIR, 'tcpflow'),
                    help="Sets input folder for TCPflow files.")
parser.add_argument('-o', '--output', dest="output", action="store",
                    default=os.path.join(BASE_DIR, 'tcpflow-' + DATE + '.xyz'),
                    help="""Sets output file for results. Can be either full
					path or path relative to tcpflow directory""")
parser.add_argument('-v', '--verbose', dest='debug', action="store_true",
                    default=False, help="Displays more information to console.")
args = parser.parse_args()

#	Handle relative paths
if not args.output.startswith(('/', '~/')):
    args.output = os.path.join(BASE_DIR, args.output)
if not args.input.startswith(('/', '~/')):
    args.input = os.path.join(BASE_DIR, args.input)
if args.input.endswith('/'):
    args.input = args.input.rstrip('/')

#	Handle unexpected filenames
if args.txt and not args.output.endswith('.txt'):
    if args.output == os.path.join(BASE_DIR, 'tcpflow-' + DATE + '.xyz'):
        default = True
    else:
        default = False
    args.output = os.path.join(BASE_DIR, 'tcpflowlist-' + DATE + '.txt')
    if not default:
        print("Output path seems incorrect... setting output to {0}".format(args.output))
elif not args.txt and not args.output.endswith('.xyz'):
    args.output = os.path.join(BASE_DIR, 'tcpflow-' + DATE + '.xyz')
    print("Output path seems incorrect... setting output to {0}".format(args.output))

#   Regular expression for splitting filename
spl = re.compile(
    r"(?P<ts>\d+)T"
    r"(?P<orig>\d{3}\.\d{3}\.\d{3}\.\d{3})\.(?P<orig_port>\d+)\-"
    r"(?P<dest>\d{3}\.\d{3}\.\d{3}\.\d{3})\.(?P<dest_port>\d+)"
)


def logger(*s):
    """
    :param s: list of strings

    Prints if verbose setting is active.
    """
    if args.debug:
        print(*s)


class XYZData:
    """
    data wrapper for xyz data
    :param ts: timestamp
    :param orig: origin ip address
    :param orig_port: origin port
    :param dest: destination ip address
    :param dest_port: destination port
    """

    def __init__(self, **kwargs):
        # replace . in ip addresses so we can divide it
        d = dict((k, int(v.replace('.', ''))) for k, v in kwargs.iteritems())
        self.__dict__.update(d)


def split_name(f):
    """
    splits filename according to regex defined above
    """
    split = spl.search(f)
    if split:
        return split.groupdict()
    return None


def parse_filenames(files):
    """
    parse timestamp, origin ip address and port, destination ip address and port;
    divide origin ip address by origin port, destination ip address by dest port;
    shuffle columns and rejoin with new lines
    """

    s = []
    for f in files:
        dct = split_name(f)
        if dct:
            o = XYZData(**dct)
            q = [o.ts, o.orig/o.orig_port, o.dest/o.dest_port]
            random.shuffle(q)
            s.append((' '.join((str(n) for n in q))))
    return '\n'.join(s)


def main():
    files = glob.glob(args.input + '/*')
    logger(files)
    if not files:
        raise Exception("No files to look at. Run tcpflow before parsing.")
    files = [os.path.basename(f) for f in files]

    #   Prepare txt list of filenames for geolocation on site
    if args.txt:
        output = '\n'.join(files)

    #   Parses filenames for .xyz file
    else:
        output = parse_filenames(files)

    if output:
        logger(output)

    with open(args.output, 'wb') as f:
            f.write(output)
    print('Success! You can find your file at {}'.format(args.output))


if __name__ == "__main__":
    main()
