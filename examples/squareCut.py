import math
from numpy import matrix
from numpy import linalg
def getEigens(m):
	return linalg.eig(m)
	
#returns an Adjacency matrix and dim the number of vertices
def getAdjacency(filename):
	a = []
	fp = open(filename)
	dim = 0
	#compute dim = # nodes of graph
	while (fp.readline()):
		dim += 1
	dim = dim/2
	fp = open(filename)
	line = fp.readline()
	w = 0
	while (line):
		line = fp.readline()
		temp = line.split("\n")
		temp = temp[0].split(" ")
		if (w == 0):
			k = 0
			while (k < len(temp)):
				k += 1
		w += 1
		k = 0
		while (k < len(temp)):
			if (temp[k] == ''):
				del temp[k]
				print w, k
			else:
				k += 1

		j = 0
		b = []
		while (j < dim):
			b.append(0)
			j += 1	
		for i in temp:
			b[int(i)] = 1.
		
		a.append(b)
		line = fp.readline()
	return matrix(a), dim

#given an adjacency matrix and number of nodes, produces 
def getDiagonal(A, dim):
	i = 0
	j = 0
	d = [];
	
	while (i < dim):
		deg = 0
		row = []
		k = 0
	
		while (k < dim):
			row.append(0)
			k += 1
		j = 0
		while (j < dim):
			deg += A[i, j]
			j += 1
		row[i] = deg
		d.append(row)
		i+=1
	return matrix(d)




#given a pageRank vector, returns a list of indices ordered from
#corresponding least to greatest components		
def sortIndices(M):
	i = 0
	v = []
	while (i < dim):
		row = []
		row.append(i)
		row.append(M[0,i])
		v.append(row)
		i += 1
#	print v
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
		I.append(V[i, 0])
		i += 1
	return I		

#given a Degree matrix, returns the total volume of a graph		
def getTotalVol(M):
	i = 0
	tVol = 0
	while (i < dim):
		tVol += M[i, i]
		i+=1
	return tVol

#given a list of vertices S and the size of the set,
#compute cheager ratio of the set of the first 'size' vertices
def getCheager(S, size):
	bound = 0
	vol = 0
	minVol = 0
	i = 0
	while (i <= size):
		vol += D[S[i], S[i]]
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
			if (A[S[j], S[k]] == 1):
				bound += 1
			k += 1
		j += 1
#	print "bound ", bound
	return float(bound)/minVol

def sort(Set):
	i = 0
	while (i < len(Set)):
		next = int(Set[i])
		j = i
		while (j > 0 and Set[j-1] > next):
			Set[j] = int(Set[j-1])
			j = j - 1
		Set[j] = next
		i += 1
	return Set

def getID(dim):
	i = 0
	j = 0
	id = []
	while (i < dim):
		temp  = []
		j = 0
		while (j < dim):
			if (i == j):
				temp.append(1)
			else:
				temp.append(0)
			j += 1
		id.append(temp)
		i += 1
	return matrix(id)

def distance(p, q, dim):
        i = 0
        dist = 0.
        while(i < dim):
                x = math.fabs(p[0,i]-q[0,i])
                dist += x
                i += 1
        return dist

#get Adjacency matrix A and number of vertices A, dim = getAdjacency('graph.txt')
default = 'Bipartite.txt'
print "Enter graph filename or press enter to use default %s" %default
filename = raw_input('>')
if (filename == ''):
	filename = default
A, dim = getAdjacency(filename)
D = getDiagonal(A, dim)

InvD = D.I
ID = getID(dim)
#Compute Lazy Random Walk
W = .5*(ID +InvD * A)
#Compte Lazy Random Walk Square
W2 = W*W

print "choose alpha between 0 and 1"
alpha = float(raw_input(">"))

print "choose starting vertex between 0 and %d" %(dim-1)
su = int(raw_input(">"))
q = []
i = 0
#initialize starting distribution Xu
while (i < dim):
	if (i == su):
		q.append(1)
	else:
		q.append(0)
	i += 1
q = matrix(q)
Xu = q
i = 2
p = alpha * (1-alpha) * q * W2
#compute p = alpha*Sum(((1-alpha)**i)*Xu * (W2**i))
while (distance(p, q, dim) > .000001):
	q = p
	p = q + alpha*((1-alpha)**i) * Xu * (W2 ** i)
	i += 1

#order the vertices by least to greatest square pageRank component
V = sortIndices(p)
print V
"""
#compute the total volume of the graph
tVol = getTotalVol(D)
#find minimum cheager ratio
minH = 2
i = 0
while (i < dim-1):
	x = getCheager(V, i)
	if (x > .0001 and x < minH):
		minH = x
		ind = i
	i += 1
print "minH: ", minH
i = 0
set = []
#print the optimal s[i]
while (i <= ind):
	set.append(int(V[i]))
	i += 1
	
print "S(%d) =  " % ind
print sort(set)"""
