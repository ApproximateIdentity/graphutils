import sys
import argparse
from sys import stdin, stdout

from graphutils.common import Pairwise


def convert_paul_to_thomas(infile, outfile):
    """
    Convert from Paul's graph format to Thomas' graph format.

    Parameters
    ----------
    infile : file object
    outfile : file object
    """
    with open(infile) as f:
        for vertex, edges in Pairwise(f):
            vertex = vertex.strip()
            edges = edges.strip().replace(' ', ',')
            with open(outfile, 'a') as g:
                g.write(vertex + '->' + edges + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inF', help = 'input file.', default = None)
    parser.add_argument('outF', help = 'output file.', default = None)
    args = parser.parse_args()
    inF = args.inF
    outF = args.outF
    print "hey", inF, outF
    try:
	convert_paul_to_thomas(inF, outF)
        #convert_paul_to_thomas(stdin, stdout)
    except IOError:
	pass
