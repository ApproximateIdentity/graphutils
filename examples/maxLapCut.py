import math
from numpy import matrix
from numpy import linalg
def getEigens(m):
	return linalg.eig(m)
	
#returns an Adjacency matrix and dim the number of vertices
def getAdjacency(filename):
	edgeList = []
	dim = 0
	#compute dim = # nodes of graph
	with open(filename) as f:
		i = 0
		for verts in f:
			if (i % 2 == 1):
				dim += 1
				edgeList.append(verts.strip().split(" "))
			i += 1	
	a = []
	for i in range(dim):		
		b = []
		for j in range(dim):
			b.append(0)
		for node in edgeList[i]:
			#print i, node
			b[int(node)] += 1.		
		a.append(b)

	return matrix(a), dim

#given an adjacency matrix and number of nodes, produces 
def getDiagonal(A, dim):
	i = 0
	j = 0
	d = [];
	for i in range(dim):
		row = []
		deg = 0
		for k in range(dim):
			row.append(0)
		for j in range(dim):
			deg += A[i, j]
		
		row[i] = deg
		d.append(row)

	return matrix(d)

#given a pageRank vector, returns a list of indices ordered from
#corresponding least to greatest components		
def sortIndices(M):
	i = 0
	v = []
	while (i < dim):
		row = []
		row.append(i)
		row.append(M[i])
		v.append(row)
		i += 1
#	print v
	V = matrix(v)
	i = 0
	while (i < dim):
		next1 = V[i, 1]
		next0 = V[i, 0]
		j = i
		while (j > 0 and V[j-1, 1] < next1):
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
def getTotalVol(D):
	i = 0 
	total = 0
	for i in range(dim):
		total += D[i, i]
	return total

#given a list of vertices S and the size of the set,
#compute cheager ratio of the set of the first 'size' vertices
def update(S, size, A, D):
	global vol
	vol += D[S[size], S[size]]

	global bound
	bound += D[S[size], S[size]]
	for i in range(size):
		bound -= A[S[size], S[i]]

def getMinVol():
	global vol, tVol
	volC = tVol - vol
	if (vol < volC):
		return vol
	return volC

def getMaxVol():
	global vol, tVol
	volC = tVol - vol
	if (vol < volC):
		return volC
	return vol
		
					
		
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
# returns dim x dim identity matrix

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

def getDMinusHalf(D, dim):
	d = D.copy()
	for i in range(dim):
		d[i, i] = d[i, i] ** -.5
	return d

def getMaxEval(M, dim):
	lMax = 0
	ind = 0
	for i in range(dim):
		if (M[i] > lMax):
			lMax = M[i]
			ind = i
	return ind
		
#get Adjacency matrix A and number of vertices A, dim = getAdjacency('graph.txt')
default = 'Bipartite.txt'
print "Enter graph filename or press enter to use default %s" %default
filename = raw_input('>')
if (filename == ''):
	filename = default
A, dim = getAdjacency(filename)
D = getDiagonal(A, dim)
L = D - A
DMinusHalf = getDMinusHalf(D, dim)
Lap = DMinusHalf * L * DMinusHalf
vals, vecs = getEigens(Lap)
ind = getMaxEval(vals, dim)
vec = matrix(vecs[:, ind])
i = 0
v = []
for i in range(dim):
	temp = []
	temp.append(vec[i,0].real)
	v.append(temp)
	i += 1
v1 = DMinusHalf * matrix(v)

V = sortIndices(v1)
print "V:", V
#find max inductance of bigraph
vol = 0
bound = 0
tVol = getTotalVol(D)
min = 2
ind = 0
for i in range(dim-1):
	update(V, i, A, D)
	#print vol, bound
	phi = (1.*bound)/getMinVol()
	#print "phi: ", phi
	if phi < min:
		min = phi
		ind = i

print "Min Conductance of Graph: ", min
result = "S: {"
for i in range(ind + 1):
	result += " %d" %int(V[i])
result += "}"
print result
