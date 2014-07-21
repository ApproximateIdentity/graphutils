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

#given an adjacency matrix and number of nodes, produces degree matrix 
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

#Given Degree matrix, number of vertices, 
def getDminusHalf(D, dim):
	i = 0
	d = D.copy()
	while (i < dim):
		d[i, i] = d[i, i] ** -.5
		i += 1
	return d

#given a list of eigenvalues, returns the index of the 
#smallest nonzero one
def getL2(M):
	l2 = 200
	i = 0
	ind = 0
	
	while (i < dim):
		if (M[i] > .0001 and M[i] < l2):
			l2 = M[i]
			ind = i
		i += 1
		
	return ind
#given an eigenvector, returns a list of indices ordered from
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


#get Adjacency matrix A and number of vertices A, dim = getAdjacency('graph.txt')
default = 'newgraph.txt'
print "Enter graph filename or press enter to use default %s" %default
filename = raw_input('>')
if (filename == ''):
	filename = default
A, dim = getAdjacency(filename)
D = getDiagonal(A, dim)

#Compute the Normalized Laplacian Lap
L = D - A
DminusHalf = getDminusHalf(D, dim)
Lap = DminusHalf * L * DminusHalf
#calculate the eigenvectors and eigenvalues
vals, vecs = getEigens(Lap)

#find the smallest nonzero eigenvalue
ind = getL2(vals)
#print vecs
vec = matrix(vecs[:,ind])
i = 0
v = []
"""the eigenvectors are annoyingly returned as complex entries
the while loop creates v, which is a list of the real
elements of the entries of the eigenvector vec"""
while (i < dim):
	temp = []
	temp.append(vec[i,0].real)
	v.append(temp)
	i += 1
v1 = matrix(v)
"""v1 is the eigenvector corresponding to l2 after it 
has been multiplied by the degree matrix to the -1/2 power """
v1 = DminusHalf * v1
#sort the components of v1 to determine an order of the vertices
V = sortIndices(v1)
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
print sort(set)