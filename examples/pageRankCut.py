import math
from numpy import matrix

#compute dim = # nodes of graph
def getDim(filename):
	k = 0
	fp = open(filename)
	while (fp.readline()):
		k += 1
	dim = k/2
	return dim
	
def vertOutList(filename):
	fp = open(filename)
	line = fp.readline()
	A = []

	while(line):
		line = fp.readline()
		temp = line.split("\n")
		#temp = temp[0].split("\t")
		temp = temp[0].split(" ")
		
		i = 0
		while (i < len(temp)):
			if (temp[i] == ""):
				del temp[i]
			else:
				i += 1
		A.append(temp)
		line = fp.readline()
	return A

# return A when undirected
# It has come to my attention that this algorithm assumes undirectedness
def vertInList(A, dim):
	"""
	B = []
	i = 0
	while (i < dim):
		j = 0
		x = []
		while (j < dim):
			k = 0
			while k < len(A[j]):
				if (i == int(A[j][k])):
					x.append(j)
				k += 1
			j += 1
		B.append(x)
		i += 1
	B = A"""
	
	B = A
	return B 
	
def getAlpha():
	alpha = 2.
	while ((alpha < 0) or (alpha > 1)):
		print "Choose a jumping constant (0 to 1) for alpha"
		alpha = float(raw_input(">"))
	return alpha

#get the point with starting distribution 1
def getS(dim):
	s = -1
	while ((s < 0) or (s > dim -1)):
		print "Choose a vertex (0 to %d) for S" %(dim-1)
		s = int(raw_input(">"))
	return s

#returns the initial PageRank distribution
#(1 at s, 0 everywhere else)
def init_distribution(s, dim):
	i = 0
	q = []
	while (i < dim):
		q.append(0.)
		i += 1
	q[s] = 1.
	return q
#returns a list containing the number of outbound edges
#for each vertex
def computeRank(A, dim):
	i = 0
	rank = []
	while (i < dim):
		rank.append(len(A[i]))
		i += 1
	return rank
			
#returns the distribution after another iteration of
#the PageRank algorithm
def new_distribution(q, B, dim, alpha, rank):
	p = []
	i = 0
	while (i < dim):
		p.append((1-alpha) / dim)
		i += 1
	i = 0
	while (i < dim):
		j = 0
		while (j < len(B[i])):
			x = int(B[i][j])
			p[i] += alpha * (q[x] / rank[x])
			j += 1
		i += 1
	return p

#returns the Euclidean distance between n-1st and nth
#distributions
def distance(p, q, dim):
	i = 0
	dist = 0.
	while(i < dim):
		x = math.fabs(p[i]-q[i])
		dist += x
		i += 1
	return dist

# returns a list of pairs (a, b) with a a vertex
# and b it's pageRank value
def getVector(dim, A, B, p):
	i = 0
	v = []
	while (i < dim):
		x = []
		x.append(i)
		x.append(p[i]/(.5*(len(A[i]) + len(B[i]))))
		v.append(x)
		i += 1
	return v

#sorts a list of pairs(see getVector) from least to greatest
#to compute the pageRank ordering of the vertices
def sortIndices(v):
	V = matrix(v)
	i = 0
	while (i < dim):
		next1 = V[i, 1]
		next0 = V[i, 0]
		j = i
		while (j > 0 and V[j-1, 1] > next1):
			V[j, 1] = V[j-1, 1]
			V[j, 0] = V[j-1, 0]
			j = j - 1
		V[j, 1] = next1
		V[j, 0] = next0
		i += 1
	
	I = []
	i = 0
	while (i < dim):
		I.append(int(V[i, 0]))
		i += 1
	return I
#computes the total volume of the graph
def getTotalVol(A, B, dim):
	i = 0
	tVol = 0.
	while (i < dim):
		tVol += .5*(len(A[i])+len(B[i]))
		i += 1
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
#	print "bound ", bound
	return float(bound)/minVol




"""
MAIN
"""



default  = 'graph.txt'

print "Enter graph filename or press enter to use default: %s" % default
filename = raw_input('>')
if (filename == ''):
	filename = default

dim = getDim(filename)

A = vertOutList(filename)

B = vertInList(A, dim)
alpha = getAlpha()
s = getS(dim)

q = init_distribution(s, dim)

rank = computeRank(A, dim)

p = new_distribution(q, B, dim, alpha, rank)

dist = distance(p, q, dim)
iter = 1
#iterates the PageRank algorithm until it converges
while (dist > .0000001):
	q = p
	p = new_distribution(q, B, dim, alpha, rank)
	dist = distance(p, q, dim)
	iter += 1
#print "distribution is:"
#print p
print "iterations: %d" %iter
v = getVector(dim, A, B, p)
S = sortIndices(v)
#print "S:"
#print S
tVol = getTotalVol(A, B, dim)
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
print set
