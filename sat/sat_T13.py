#!/usr/bin/python
"""
	This program generates a CNF formula that can be used to
	verify that the 13-vertex tree T13 does not admit an
	L-shaped embedding in the (2,2,2,1,2,2,2)-staircase point set.
  The program can easily be adjusted for testing other pairs
  of trees and point sets by changing the definitions of Y and E.
	(c) 2018 Manfred Scheucher <scheucher@math.tu-berlin.de>
"""

from itertools import *


sign = lambda x: (x>0)-(x<0) 


def writeDIMACScnf(CNF,VARS,filename):
	print "write instance to DIMACS cnf file:",filename
	with open(filename,"w") as f:
		f.write("p cnf "+str(len(VARS))+" "+str(len(CNF))+"\n")
		for clause in CNF:
			f.write(" ".join(str(x) for x in clause)+" 0\n")
	print "use for example picosat to solve"


def segments_intersect((A,B),(C,D)):
	(ax,ay) = A
	(bx,by) = B
	(cx,cy) = C
	(dx,dy) = D
	assert(ay==by)
	assert(cx==dx)

	if ax > bx: ax,bx = bx,ax
	if cy > dy: cy,dy = dy,cy

	return (ax <= cx and cx <= bx) and (cy <= ay and ay <= dy)


def test_embeddings(E,Y):
	N = len(Y)
	E = list(set([(a,b) for (a,b) in E]+[(b,a) for (a,b) in E]))

	# variable names as python lambda functions for readability
	M = lambda p,n: "M("+str(p)+","+str(n)+")"
	not_M = lambda x,y: "not_"+M(x,y)
	H = lambda a,b: "H("+str(a)+","+str(b)+")"
	not_H = lambda x,y: "not_"+H(x,y)

	# list of variables
	VARS = {}
	count = 0
	for var_name in sorted([M(p,n) for p in range(N) for n in range(N)]+[H(a,b) for (a,b) in E]):
		count += 1
		VARS[var_name] = count
	parseVar = lambda var: VARS[var] if var[:4] != "not_" else -VARS[var[4:]] 

	# generate CNF
	CNF = []

	# (1) injective mapping from vertices to points
	for n0 in range(N):
		CNF.append([M(p,n0) for p in range(N)])

		for p in range(N):
			for q in range(p):
				CNF.append([not_M(p,n0),not_M(q,n0)])

	for p0 in range(N):
		CNF.append([M(p0,n) for n in range(N)])

		for m in range(N):
			for n in range(m):
				CNF.append([not_M(p0,m),not_M(p0,n)])

	# (2) every edge of the tree must be represented by some L-shaped edge
	for (a,b) in E:	
		CNF.append([H(a,b),H(b,a)])
		CNF.append([not_H(b,a),not_H(a,b)])

	# (3) no overlapping edge segments
	for p in range(N):
		for q in range(N):
			for r in range(q):

				for (a,b) in E:
					for (a2,c) in E:
						if a != a2: continue
						if b == c: continue

						# (3.1)
						if sign(p-q) == sign(p-r):
							CNF.append([not_M(p,a),not_M(q,b),not_M(r,c),not_H(a,b),not_H(a,c)])

						# (3.2)
						if sign(Y[p]-Y[q]) == sign(Y[p]-Y[r]):
							CNF.append([not_M(p,a),not_M(q,b),not_M(r,c),H(a,b),H(a,c)])

	# (4) no crossing edge segments
	Epairs = [((a,b),(c,d)) for (a,b) in E for (c,d) in E if a!=c and b!=d and (a,b) != (d,c)]
	for (p,q) in permutations(range(N),2):
		for (r,s) in permutations(range(N),2):
			if p < r: continue
			if p==r or q==s: continue

			vecP = [p,Y[p]]
			vecQ = [q,Y[q]]
			vecR = [r,Y[r]]
			vecS = [s,Y[s]]

			vecP_H = (vecQ[0],vecP[1])
			vecR_H = (vecS[0],vecR[1])

			# relax endpoints (crossings will occur here)
			assert(vecP[0] != vecP_H[0])
			assert(vecQ[1] != vecP_H[1])
			assert(vecR[0] != vecR_H[0])
			assert(vecS[1] != vecR_H[1])
			vecP[0] += 1 if vecP[0] < vecP_H[0] else -1
			vecR[0] += 1 if vecR[0] < vecR_H[0] else -1

			vecQ[1] += 1 if vecQ[1] < vecP_H[1] else -1
			vecS[1] += 1 if vecS[1] < vecR_H[1] else -1

			if segments_intersect((vecP,vecP_H),(vecR_H,vecS)) or segments_intersect((vecR,vecR_H),(vecP_H,vecQ)):
				for (a,b),(c,d) in Epairs:
					CNF.append({not_M(p,a),not_M(q,b),not_M(r,c),not_M(s,d),not_H(a,b),not_H(c,d)})

	# write CNF to file
	CNF = [[parseVar(var) for var in clause] for clause in CNF]
	writeDIMACScnf(CNF,VARS,"instance.cnf")


# compute y-coordinates for given staircase point set
def staircase(S):
	Y = []
	l = 0
	for s in S:
		Y += list(reversed(range(l,l+s)))
		l += s
	return Y


Y = staircase((2,2,2,1,2,2,2))
E = [(0,i) for i in range(1,4)]+[((i-1)/3,i) for i in range(4,13)] 
print "Y:",Y
print "E:",E
test_embeddings(E,Y)