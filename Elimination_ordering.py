from Verification import *
import copy

def eliminate(u, g):
    '''

    :param g: a graph represented using a dictionary of sets
    :param u: a node in 'g'
    :return: None
             Eliminates the node 'u' from the graph 'g' after linking together all couples of neighbors of 'u' in 'g'
    '''
    for v in g[u]:
        for w in g[u]:
            if v != w:
                g[w].add(v)
        if u in g[v]:
            g[v].remove(u)
    del(g[u])
    return

def sub_tree(l, bag_of, g):
    '''

    :param g: is a graph that has a node eliminated with "eliminate" after each call of the recursive function,
              it is represented using a dictionary of sets
    :param l: is an elimination ordering that has its first element popped after each call of the recursive function
    :param bag_of: 'bag_of[u]', with 'u' a Node element in the returned tree decomposition, is the first vertice/bag
                    of nodes of the said tree in which 'u' appears in its recursive construction
    :return: Recursively constructs a tree decomposition of 'g' out of a "shriking" elimination ordering 'l' and a "growing" dictionary of bags 'bag_of'
    '''
    if len(l) == 1:
        bag_of[l[0]] = Node(l[0])
        return Tree(bag_of[l[0]])

    u = l[0]
    v = l[1] # v is the neighbor of 'u' that has the lowest order in 'l'
    u_bag = Node([u]+list(g[u]))
    bag_of[u] = u_bag
    for w in l:
        if w in g[u]:
            v = w # here, we extract the said neighbor
            break

    eliminate(u,g)
    t = sub_tree(l[1:], bag_of, g)

    v_bag = bag_of[v]
    v_bag.add_children([u_bag]) # linking the bags of 'u' and 'v'
    return t

def tree_decomposition_by_elimination(elim_ordering, graph):
    '''

    :param elim_ordering: The elimination ordering following which the recursive construction of the tree decomposition is prioritizing the elimination of nodes
    :param graph: A graph represented using a dictionary of sets
    :return: A tree decomposition of 'graph' that has a tree width bounded by the maximum clique size encountered following 'elim_ordering'
    '''
    g = copy.deepcopy(graph)
    return sub_tree(elim_ordering, {}, g)

'''
graph = {}
graph['1'] = {'9', '2', '3'}
graph['9'] = {'1', '6', '7'}
graph['6'] = {'9'}
graph['7'] = {'9'}
graph['2'] = {'1', '8'}
graph['8'] = {'2'}
graph['3'] = {'1', '4', '5'}
graph['4'] = {'3', '5'}
graph['5'] = {'3', '4'}

print(tree_decomposition_by_elimination(['1','2','3','4','5','6','7','8','9'], graph))
print(tree_decomposition_by_elimination(['8','2','7','6','5','4','3','9','1'], graph))

graph = {}
graph['1'] = {'2', '3'}
graph['2'] = {'1', '3', '4'}
graph['3'] = {'1', '2', '5'}
graph['4'] = {'2', '5'}
graph['5'] = {'3', '4'}

print(tree_decomposition_by_elimination(['2', '3', '1', '4', '5'], graph))
print(tree_decomposition_by_elimination(['1', '4', '5', '2', '3'], graph))

graph = {}
graph['1'] = {'2'}
graph['2'] = {'1', '3'}
graph['3'] = {'2'}

print(tree_decomposition_by_elimination(['1', '2', '3'], graph))
print(tree_decomposition_by_elimination(['2', '3', '1'], graph))
'''
graph = {}
graph['7'] = {'4', '8'}
graph['8'] = {'7', '4', '6', '9', '2'}
graph['9'] = {'8', '6'}
graph['4'] = {'7', '8', '1', '2'}
graph['6'] = {'8', '9', '2', '3'}
graph['1'] = {'4', '2'}
graph['2'] = {'1', '4', '3', '6', '8'}
graph['3'] = {'2', '6'}

print(tree_decomposition_by_elimination(['1', '3', '7', '9', '4', '6', '2', '8'], graph))
print(tree_decomposition_by_elimination(['1', '2', '3', '4', '6', '7', '8', '9'], graph))