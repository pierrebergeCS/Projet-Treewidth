from Verification import *
from copy import deepcopy
from queue import Queue


def create_s_t_graph(grph, S, T):
    st_g = deepcopy(grph)

    st_g['s'] = set()
    st_g['t'] = set()
    for u in S:
        for v in grph[u]:
            st_g[v].remove(u)
            st_g[v].add('s')
            if v not in S:
                st_g['s'].add(v if v not in T else 't')
    for u in T:
        for v in grph[u]:
            st_g[v].remove(u)
            st_g[v].add('t')
            if v not in T:
                st_g['t'].add(v if v not in S else 's')
    for u in S:
        del st_g[u]
    for u in T:
        del st_g[u]

    lu = list(st_g.keys())
    for u in lu:
        st_g[u + '_'] = set([u])

    for u in lu:
        lgu = list(st_g[u])
        for v in lgu:
            st_g[u].remove(v)
            st_g[u].add(v + '_')
    return st_g


graph = {}
graph['1'] = {'4', '2'}
graph['2'] = {'1', '3', '8'}
graph['3'] = {'2', '6'}
graph['4'] = {'7', '1'}
graph['6'] = {'9', '3'}
graph['7'] = {'4', '8'}
graph['8'] = {'7', '9', '2'}
graph['9'] = {'8', '6'}

print(create_s_t_graph(graph, {'1', '4'}, {'6', '9'}))

oo = 1 << 16


def create_residual_graph(st_g):
    res_g = deepcopy(st_g)
    for u in st_g:
        if u[-1] == '_':
            v = u[:-1]
            res_g[u] = {v: 1}
        else:
            res_g[u] = {u + '_': 0}
            for v in st_g[u]:
                res_g[u][v] = oo

    return res_g


print(create_residual_graph(create_s_t_graph(graph, {'1', '4'}, {'6', '9'})))


def find_size_and_cut_min_vertex_cut(grph, S, T):
    st_g = create_s_t_graph(grph, S, T)
    res_g = create_residual_graph(st_g)

    N = len(res_g)
    size = 0
    cut = set()
    s_area = set()

    while True:
        par = {}
        vis = set()

        q = Queue(maxsize=N)
        q.put('s')
        vis.add('s')

        while not q.empty():
            u = q.get()

            for v in res_g[u]:
                if v not in vis and res_g[u][v] > 0:
                    vis.add(v)
                    q.put(v)
                    par[v] = u
                    if v == 't_':
                        break
            if 't_' in vis:
                break

        if 't_' not in vis:
            for u in res_g:
                if u[-1] != '_' and u not in {'s', 't'}:
                    v = u + '_'
                    if (u in vis) ^ (v in vis):
                        cut.add(u)
                    if u in vis and v in vis:
                        s_area.add(u)
            break

        size += 1
        last = 't_'
        while last in par:
            res_g[par[last]][last] -= 1
            if par[last] not in res_g[last]:
                res_g[last][par[last]] = 0
            res_g[last][par[last]] += 1
            last = par[last]

    return size, cut, s_area


print(find_size_and_cut_min_vertex_cut(graph, {'1', '4'}, {'6', '9'}))
print(find_size_and_cut_min_vertex_cut(graph, {'7'}, {'3'}))

'''
def verify_min_separator(gr, S, T):
    gph = create_s_t_graph(gr, S, T)
    size, cut = find_size_and_cut_min_vertex_cut(gph)
    sep = set()

    for w in cut:
        vis = set()

        q = ['s']
        vis.add('s')

        while q:
            u = q.pop()
            for v in gph[u]:
                if v not in vis and (v not in cut or v == w):
                    q.append(v)
                    vis.add(v)
                    if v == 't':
                        sep.add(w)
                        break
            if 't' in vis:
                break

        if len(sep) == size:
            break

    if len(sep) != size:
        raise ValueError('Incompatibility Size/Cut')

    return sep
'''


def eliminate_set(gr, S):
    g = deepcopy(gr)
    for u in S:
        for v in gr[u]:
            g[v].remove(u)
    for u in S:
        del g[u]
    return g


print(eliminate_set(graph, {'1', '2', '4'}))


def find_all_partitions(W, k):
    all = [(set(), set(), set())]
    M = int(2 * len(W) / 3.)
    for u in W:
        nextAll = []
        for (AW, SW, BW) in all:
            if len(SW) <= k:
                nSW = set(SW)
                nSW.add(u)
                nextAll.append((AW, nSW, BW))
            if len(AW) < M:
                nAW = set(AW)
                nAW.add(u)
                nextAll.append((nAW, SW, BW))
            if len(BW) < M:
                nBW = set(BW)
                nBW.add(u)
                nextAll.append((AW, SW, nBW))
        all = nextAll

    all = [(AW, SW, BW) for (AW, SW, BW) in all if min(len(AW), len(SW), len(BW)) > 0 and len(BW) <= len(AW)]

    return all


print(find_all_partitions({1, 2, 3, 4}, 0))


def find_balanced_partition(gr, W, k):
    allPartitions = find_all_partitions(W, k)
    for (AW, SW, BW) in allPartitions:
        grph = eliminate_set(gr, SW)
        size, cut, s_area = find_size_and_cut_min_vertex_cut(grph, AW, BW)
        if size + len(SW) > k + 1:
            continue

        t_area = set()
        for u in grph:
            if u not in s_area and u not in cut:
                t_area.add(u)

        return True, AW | s_area, SW | cut, BW | t_area
    return False, [], [], []


def build_tree_decomposition_with_separator(gr, W, k):
    V = list(gr.keys())
    if W == set(V):
        return Tree(Node(V))
    t, A, S, B = find_balanced_partition(gr, W, k)
    if not t:
        raise ValueError('Tree Width is larger than ' + str(k))
    treeA = build_tree_decomposition_with_separator(eliminate_set(gr, B), S | (W & A))
    treeB = build_tree_decomposition_with_separator(eliminate_set(gr, A), S | (W & B))
    root_bag = Node(list(S | W))
    root_bag.add_children([treeA.root, treeB.root])
    return Tree(root_bag)
