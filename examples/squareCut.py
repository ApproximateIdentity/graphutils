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
"""
def getConductance(S, size, D):
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
"""
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

def distance(p, q, dim):
#returns distance between old and new distributions
        i = 0
        dist = 0.
        while(i < dim):
                x = math.fabs(p[0,i]-q[0,i])
                dist += x
                i += 1
        return dist

def writeBigraph(A, dim):
#writes a file expressing the weighted bigraph obtained 
#from the original graph

	with open('bigraph.txt', 'w') as f:
		for i in range(dim):
			f.write("%d\n" %i)
			for j in range(dim):
				if A[i, j] == 1:
					for k in range(dim):
						if (A[j,k] == 1):
							f.write("%d " %k)
			if i < dim -1:
				f.write("\n")
		
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
writeBigraph(A, dim)
ATwo, dim = getAdjacency('bigraph.txt')
DTwo = getDiagonal(ATwo, dim)
WTwo = .5*(ID + DTwo.I*ATwo)
print "choose alpha between 0 and 1"
alpha = float(raw_input(">"))

print "choose starting vertex between 0 and %d" %(dim-1)
su = int(raw_input(">"))
q = []
#initialize starting distribution Xu
for i in range(dim):	
	if (i == su):
		q.append(1)
	else:
		q.append(0)
q = matrix(q)
Xu = q
#print "Xu", Xu
i = 2
p = alpha * (1-alpha) * q * WTwo
#compute p = alpha*Sum(((1-alpha)**i)*Xu * (W2**i))
while (distance(p, q, dim) > .000001):
	q = p
	p = q + alpha*((1-alpha)**i) * Xu * (WTwo ** i)
	i += 1

#order the vertices by least to greatest square pageRank component
V = sortIndices(p*DTwo.I)
#print p*DTwo.I
print V

#find min cheager of orig. graph
vol = 0
bound = 0
tVol = getTotalVol(D)
min = 2
ind = 0
for i in range(dim-1):
	update(V, i, A, D)
	#print vol, bound
	phi = 1.*bound/getMinVol()
	if phi < min:
		min = phi
		ind  = i
print "Min Inductance of Graph: ", min
result = "S: {"
for i in range(ind + 1):
	result += " %d" %int(V[i])
result += "}"
print result

#find max inductance of bigraph
vol = 0
bound = 0
tvol = getTotalVol(DTwo)
max = 0
ind = 0
for i in range(dim-1):
	update(V, i, ATwo, DTwo)
	#print vol, bound
	psi = 1.*bound/getMaxVol()
	if psi > max:
		max = psi
		ind = i

print "Max Conductance of Bigraph: ", max
result = "S: {"
for i in range(ind + 1):
	result += " %d" %int(V[i])
result += "}"
print result

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
