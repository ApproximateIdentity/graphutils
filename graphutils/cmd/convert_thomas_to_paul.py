from sys import stdin, stdout

from graphutils.parsing import parseline


def convert_thomas_to_paul(infile, outfile):
    """
    Convert from Thomas' graph format to Paul's graph format.

    Parameters
    ----------
    infile : file object
    outfile : file object
    """
    for line in infile:
        id, neighbors = parseline(line)
        outfile.write(id + '\n' + ' '.join(neighbors) + ' \n')
        
    outfile.write('\n')


if __name__ == '__main__':
    try:
        convert_thomas_to_paul(stdin, stdout)
    except IOError:
        pass
