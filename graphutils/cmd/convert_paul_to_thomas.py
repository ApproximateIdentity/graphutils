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
    for vertex, edges in Pairwise(infile):
        vertex = vertex.strip()
        edges = edges.strip().replace(' ', ',')
        outfile.write(vertex + '->' + edges + '\n')


if __name__ == '__main__':
    try:
        convert_paul_to_thomas(stdin, stdout)
    except IOError:
        pass
