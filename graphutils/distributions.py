from collections import defaultdict

from .parsing import parseline

def initdist(vertex, data_filepath):
    '''
    Initiate distribution from data file.
    
    Parameters
    ----------
    data_filepath : string
        path to datafile
    
    Returns
    -------
    dist : dict of floats
    '''
    dist = {}
    with open(data_filepath) as f:
        for line in f:
            id, _ = parseline(line)
            dist[id] = 0.0

    dist[vertex] = 1.0

    return dist


def iterdist(alpha, dist, data_filepath):
    '''
    Iterate next distribution from old distributation and data file using
    PageRank.
    
    Parameters
    ----------
    dist : dict of floats
    data_filepath : string
        path to datafile
    
    Returns
    -------
    dist : dict of floats
    '''
    nextdist = defaultdict(float)
    nodecount = 0
    with open(data_filepath) as f:
        for line in f:
            nodecount += 1
            id, neighbors = parseline(line)

            weight = dist[id]/len(neighbors)
            for neighbor in neighbors:
                nextdist[neighbor] += alpha*weight

    for id in nextdist.iterkeys():
        nextdist[id] += (1.0 - alpha)/nodecount

    return nextdist
