from sys import stdin, stdout

from graphutils.common import Pairwise

if __name__ == '__main__':
    for vertex, edges in Pairwise(stdin):
        vertex = vertex.strip()
        edges = edges.strip().replace(' ', ',')
        try:
            stdout.write(vertex + '->' + edges + '\n')
        except IOError:
            break
