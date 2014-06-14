from graphutils.parsing import parseline
from graphutils.metrics import l1
from graphutils.distributions import initdist, iterdist

data_filepath = './graph.thomas'
EPSILON = 0.0000001

if __name__ == '__main__':
    dist = initdist('a', data_filepath)

    numiter = 0
    while True:
        numiter += 1
        nextdist = iterdist(0.5, dist, data_filepath)
        if l1(dist, nextdist) < EPSILON:
            break
        dist = nextdist
    
    print "Number of iterations: %s" % numiter
    print "Final dist:", nextdist

    dist = initdist('b', data_filepath)

    numiter = 0
    while True:
        numiter += 1
        nextdist = iterdist(0.5, dist, data_filepath)
        if l1(dist, nextdist) < EPSILON:
            break
        dist = nextdist
    
    print "Number of iterations: %s" % numiter
    print "Final dist:", nextdist
