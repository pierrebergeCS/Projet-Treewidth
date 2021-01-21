from Classes import Tree, Node
from Tree_decomposition import canonical_tree
from collections import defaultdict

# hash pour être rigoureux

def fill_dict(tree):
    adj_list=defaultdict(lambda: [])
    def bfs(node):
        for i in node.value:
            if i not in adj_list[i]:
                adj_list[i].append(i)
            for j in node.value:
                if j not in adj_list[i]:
                    adj_list[i].append(j)
                    adj_list[j].append(i)
        for child in node.children:
            bfs(child)
    bfs(tree.root)
    return adj_list

def check_vertices_edges(tree,graph):
    adj_list=fill_dict(tree)
    for vertice in graph.keys():
        if vertice not in adj_list:
            return False
    for vertice_1 in graph.keys():
        for vertice_2 in graph[vertice_1]:
            if vertice_2 not in adj_list[vertice_1]:
                return False
    return True

def is_connex(tree,graph):
    def is_in(index,node):
        '''input: index: str - node: Node object
        returns True if index is in the nodes of the subtree rooted at node'''
        if index in node.value:
            return True
        else:
            for child in node.children:
                if is_in(index,child):
                    return True
            return False
    
    def aux(index):
        def bfs(node,boolean_parent):
            if node.children==[]:
                return True
            else:
                occurence=boolean_parent
                for child in node.children:
                    if is_in(index,child):
                        occurence+=1
                        break
                if occurence>=2 and index not in node.value:
                    return False
                else:
                    for child in node.children:
                        if not bfs(child,boolean_parent or (index in node.value)):
                            return False
                    return True
        return bfs(tree.root,False)

    for vertice in graph.keys():
        if not aux(vertice):
            return False
        return True

def is_tree_decomposition(tree,graph):
    if not is_connex(tree,graph) or not check_vertices_edges(tree,graph):
        return False
    return True