# generate all unordered trees with n vertices and maximum degree 4
# see also http://oeis.org/A000602
# (c) 2018 Manfred Scheucher <scheucher@math.tu-berlin.de>

from sys import argv

# Run BFS through tree T starting at v0 to relabel vertices in the order
# they are encountered during the BFS with 0,...,n.
# Output representation is an array of length n-1 whose i-th entry is
# the parent of vertex i, for i=1,...,n-1 (vertex 0=v0 has no parent).
def bfs_parents(T,v0):
    todo = [v0]
    parent = []
    label = {}
    while todo:
        v = todo.pop(0)
        label[v] = len(label)
        N = sorted(T.neighbors(v), key=lambda w:T.degree(w), reverse=0)
        for w in N:
            assert(w not in todo)  # input should be a tree
            if w in label:
                parent.append(label[w])
            else:
                todo.append(w)

    # recover tree from parent array representation, and check for correctness
    T2 = Graph([(i+1,parent[i]) for i in range(len(parent))])
    assert(T2.is_isomorphic(T))

    return parent

n = int(argv[1])
# call nauty for tree generation
# generate graphs with n vertices, n-1 edges, connected, maximum degree 4
for T in graphs.nauty_geng(str(n)+" "+str(n-1)+" -c -D4"):
    maxdeg = max(T.degree())
    for v in T:
        if T.degree(v) == maxdeg:
            for w in bfs_parents(T,v): print w,
            print
            break
