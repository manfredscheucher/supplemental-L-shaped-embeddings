# generate all ordered trees with n vertices and maximum degree 4 that have
# more than one embedding when considering them as unordered trees
# (c) 2018 Manfred Scheucher <scheucher@math.tu-berlin.de>

from sys import argv

# Run DFS through tree T in all possible ways, i.e.,
# with all possible orderings of subtrees at each vertex.
# Generates all possible vertex orderings/plane embeddings
# obtained in this way.
def dfs(V,T,O=[]):
    if len(O) == len(V):
        yield O
    else:
        if not O:
            O.append(V[0])  # pick root

        found = 0
        for w in reversed(O):  # explore lastly added vertices first (=DFS)
            for v in T.neighbors(w):
                if v not in O:
                    found = 1
                    for O2 in dfs(V,T,O+[v]):
                        yield O2
            if found: break

n = int(argv[1])
# call nauty for tree generation
# generate graphs with n vertices, n-1 edges, connected, maximum degree 4
for T in graphs.nauty_geng(str(n)+" "+str(n-1)+" -c -D4"):
    V = T.vertices()
    V1 = [v for v in V if T.degree(v) == 1]
    E = T.edges(labels=0)
    gstrs = []
    to_print = []
    for O in dfs(V,T):
        O1 = [v for v in O if v in V1]  # extract cyclic ordering of leaves in the embedding
        G = Graph(E,multiedges=1)  # create larger plane graph G from embedded tree
        for i in range(len(O1)):
            G.add_edge(O1[i-1],O1[i])  # add edges cyclically between any two consecutive leaves
            G.add_edge(O1[i],n+i)  # add pending dummy each at each leaf to mark outer face
        gstr = G.canonical_label().sparse6_string()
        if gstr not in gstrs:
            gstrs.append(gstr)
            T2 = copy(T)
            T2.relabel({O[i]:i for i in range(n)})
            to_print.append(T2)

    if len(gstrs) > 1:  # tree can be embedded in more than one way
        for T2 in to_print:
            E2 = sorted(T2.edges(labels=False),key=lambda e:e[1])
            # The tree is represented as an array of length n-1 whose i-th entry is
            # the parent of vertex i, for i=1,...,n-1 (vertex 0 has no parent).
            # The neighbors of each vertex are numbered increasingly in cw or ccw order.
            for i in range(len(E2)):
                assert(E2[i][1] == i+1)
                print E2[i][0],
            print
