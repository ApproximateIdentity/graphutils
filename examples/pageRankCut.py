import sys
import argparse

import math
from numpy import matrix

from graphutils.common import Pairwise

def loadgraph(graphfile):
    graph = graphfile.read().splitlines()
    graph = [line.split('->') for line in graph]
    graph = [[node, edges.split(',')] for node, edges in graph]
    return graph

def getVertOutList(graph):
    """
    Build lists of vertices reachable by each vertex.
    """
    vertOutList = [edges for _, edges in graph]
    return vertOutList


def getVertInList(vertOutList):
    """
    Build lists of vertices pointing to each vertex.
    """
    vertInList = vertOutList
    return vertInList


def init_distribution(pnode, graph):
    """
    Initializes a distribution with all weight at node pnode.
    """
    dist = {}
    for node, _ in graph:
        dist[node] = 0.0
    dist[pnode] = 1.0
    return dist


def new_distribution(distold, graph, alpha, pnode):
    """
    #returns the distribution after another iteration of
    #the PageRank algorithm
    """
    newdist = {}
    for node, _ in graph:
        newdist[node] = 0.0
    newdist[pnode] = 1 - alpha
    for node, targets in graph:
        newdist[node] += .5 * alpha * distold[node]
        for target in targets:
            newdist[target] += .5 * alpha * (distold[node] / len(targets))
    return newdist


def distance(dist1, dist2):
    """
    #returns the L1 distance between n-1st and nth
    #distributions
    """
    dist = 0.0
    for key in dist1.iterkeys():
        dist += abs(dist1[key] - dist2[key])
    return dist


def getVector(graph, dist):
    """
    # returns a list of pairs (a, b) with a a vertex
    # and b it's pageRank value
    """
    v = []
    for node, targets in graph:
        v.append([node, dist[node]/len(targets)])
    return v


def getTotalVol(graph):
    """
    Return total volume of a graph.
    """
    tVol = 0.0
    for _, targets in graph:
        tVol += len(targets)
    return tVol


#given a list of vertices S and the size of the set,
#compute cheager ratio of the set of the first 'size' vertices
def getCheager(S, size, A, B, tVol):
    bound = 0
    vol = 0
    minVol = 0
    i = 0
    while (i <= size):
        vol += .5*(len(A[int(S[i])]) + len(B[int(S[i])]))
        i += 1
    volC = tVol - vol
    if (vol < volC):
        minVol = vol
    else:
        minVol = volC
    j = 0
    k = 0
    while (j <= size):
        k = size + 1
        while (k < dim):
            for x in A[int(S[j])]:
                if (int(x) == int(S[k])):
                    bound += 1
            k += 1
        j += 1
#    print "bound ", bound
    return float(bound)/minVol


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        nargs='?',
                        help=('File containing graph. If left unspecified, '
                              'will read from standard in.'),
                        default=None)
    parser.add_argument('-a', '--alpha', dest='alpha',
                        help='Alpha parameter.',
                        type=float,
                        default=0.5)
    parser.add_argument('-p', '--personalizednode', dest='pnode',
                        help='Alpha parameter.',
                        type=str,
                        default=0)
    args = parser.parse_args()

    filename = args.filename
    if filename is not None:
        graphfile = open(filename)
    else:
        graphfile = sys.stdin
    graph = loadgraph(graphfile)
    graphfile.close()

    dim = len(graph)

    alpha = args.alpha
    assert(alpha >= 0.0 and alpha <= 1.0)

    pnode = args.pnode

    distold = init_distribution(pnode, graph)

    distnew = new_distribution(distold, graph, alpha, pnode)

    iter = 1
    #iterates the PageRank algorithm until it converges
    while (distance(distnew, distold) > .0000001):
        distold = distnew
        distnew = new_distribution(distold, graph, alpha, pnode)
        iter += 1

    print "iterations: %d" %iter
    v = getVector(graph, distnew)

    S = [node for node, _ in sorted(v, key=lambda a: a[1])]

    #print "S:"
    #print S
    tVol = getTotalVol(graph)
    i = 0
    minH = 2
    ind = 0
    #computes CheagerRatio of each S(i), keeping track
    # of smallest one along the way
    vertOutList = getVertOutList(graph)
    vertInList = getVertInList(vertOutList)
    while (i < dim-1):
        x = getCheager(S, i, vertOutList, vertInList, tVol)
        if (x > .0001 and x < minH):
            minH = x
            ind = i
        i += 1
    print "minH: ", minH
    i = 0
    set = []
    #print the optimal s[i]
    while (i <= ind):
        set.append(int(S[i]))
        i += 1

    print "S(%d) =  " % ind
    print S