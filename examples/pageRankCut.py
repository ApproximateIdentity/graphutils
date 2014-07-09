import math
from numpy import matrix

from graphutils.common import Pairwise

def getDim(filename):
    """
    Return the number of verticies of a graph.
    """
    numlines = 0
    with open(filename) as f:
        for _, _ in Pairwise(f):
            numlines += 1
    return numlines


def getVertOutList(filename):
    """
    Build lists of vertices reachable by each vertex.
    """
    vertOutList = []
    with open(filename) as f:
        for _, line in Pairwise(f):
            line = line.strip()
            line = line.split(' ')
            vertOutList.append(line)
    return vertOutList


def getVertInList(vertOutList, dim):
    """
    Build lists of vertices pointing to each vertex.
    """
    vertInList = vertOutList
    return vertInList


def getAlpha():
    """
    Prompt for initial alpha.
    """
    while True:
        print "Choose a jumping constant (0 to 1) for alpha"
        alpha = raw_input(">")
        try:
            alpha = float(alpha)
        except ValueError:
            continue
        if alpha >= 0 and alpha <= 1:
            break
    return alpha


def getS(dim):
    """
    Prompt for point to "personalize around".
    """
    while True:
        print "Choose a vertex (0 to %d) for S" % (dim - 1)
        s = raw_input(">")
        try:
            s = int(s)
        except ValueError:
            continue
        if s >= 0 and s <= dim -1:
            break
    return s


def init_distribution(s, dim):
    """
    returns the initial PageRank distribution
    #(1 at s, 0 everywhere else)
    """
    q = []
    for _ in range(dim):
        q.append(0.0)
    q[s] = 1.0
    return q


def computeRank(A, dim):
    """
    returns a list containing the number of outbound edges
    for each vertex
    """
    rank = [len(a) for a in A]
    return rank


def new_distribution(dist_old, B, dim, alpha, rank, s):
    """
    #returns the distribution after another iteration of
    #the PageRank algorithm
    """
    newdist = []
    for i in range(dim):
        newdist.append(0.0)
    newdist[s] = 1 - alpha
    for i in range(dim):
        b = B[i]
        newdist[i] += .5 * alpha * dist_old[i]
        for x in b:
            x = int(x)
            newdist[i] += .5 * alpha * (dist_old[x] / rank[x])
    return newdist


def distance(p, q):
    """
    #returns the L1 distance between n-1st and nth
    #distributions
    """
    dist = 0.
    for i, j in zip(p, q):
        dist += abs(i - j)
    return dist


def getVector(dim, A, B, p):
    """
    # returns a list of pairs (a, b) with a a vertex
    # and b it's pageRank value
    """
    i = 0
    v = []
    for i in range(dim):
        x = []
        x.append(i)
        #Extremely weird way to do degree
        x.append(p[i]/(.5*(len(A[i]) + len(B[i]))))
        v.append(x)
    return v


def sortIndices(v):
    """
    #sorts a list of pairs(see getVector) from least to greatest
    #to compute the pageRank ordering of the vertices
    """
    I = sorted(v, key=lambda a: a[1])
    I = [pair[0] for pair in I]
    return I


def getTotalVol(A, B):
    """
    Return total volume of a graph.
    """
    tVol = 0.
    for a, b in zip(A, B):
        tVol += .5*(len(a) + len(b))
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

    default  = 'graph1.txt'

    print "Enter graph filename or press enter to use default: %s" % default
    filename = raw_input('>')
    if (filename == ''):
        filename = default

    dim = getDim(filename)

    A = getVertOutList(filename)

    B = getVertInList(A, dim)
    alpha = getAlpha()
    s = getS(dim)

    dist_old = init_distribution(s, dim)

    rank = computeRank(A, dim)

    dist_new = new_distribution(dist_old, B, dim, alpha, rank, s)

    dist = distance(dist_new, dist_old)
    iter = 1
    #iterates the PageRank algorithm until it converges
    while (dist > .0000001):
        dist_old = dist_new
        dist_new = new_distribution(dist_old, B, dim, alpha, rank, s)
        dist = distance(dist_old, dist_new)
        iter += 1
    #print "distribution is:"
    #print p
    print "iterations: %d" %iter
    v = getVector(dim, A, B, dist_new)
    S = sortIndices(v)
    #print "S:"
    #print S
    tVol = getTotalVol(A, B)
    i = 0
    minH = 2
    ind = 0
    #computes CheagerRatio of each S(i), keeping track
    # of smallest one along the way
    while (i < dim-1):
        x = getCheager(S, i, A, B, tVol)
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
