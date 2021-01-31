from Classes import Tree, Node
from Tree_decomposition import canonical_tree
from collections import defaultdict

# hash pour être rigoureux

def fill_dict(tree):
    ''' Gives the adjcency list of the tree.
    Parameters:
        tree (Tree object)
    Returns:
        adj_list (defaultdict)'''

    adj_list=defaultdict(lambda: [])
    def bfs(node):
        ''' Using BFS to fills the dict adj_list with 
            the vertices and edges encountered starting
        Parameters:
            node (Node object)'''

        for i in node.value:
            if i not in adj_list:
                adj_list[i]=[]
            for j in node.value:
                if i!=j and j not in adj_list[i]:
                    adj_list[i].append(j)
                    adj_list[j].append(i)
        for child in node.children:
            bfs(child)

    bfs(tree.root)
    return adj_list


def check_vertices_edges(tree,graph):
    ''' Checks whether the tree contains every vertex and every edge of the initial graph.
    Parameters:
        tree (Tree object)
        graph (defaultdict)
    Returns:
        boolean'''
    
    adj_list=fill_dict(tree)
    for vertex in graph.keys():
        if vertex not in adj_list:
            return False
    for vertex_1 in graph.keys():
        for vertex_2 in graph[vertex_1]:
            if vertex_2 not in adj_list[vertex_1]:
                return False
    return True


def is_connex(tree, graph):
    ''' Checks if, for every vertex (v) of the graph, the subgraph containing (v) is connex,
        by comparing the size of some subtree where all nodes contain (v) 
        and the number of occurences of (v) in the whole tree.
    Parameters:
        tree (Tree object)
        graph (defaultdict)
    Returns:
        boolean '''

    def find_first(node,index):
        ''' Using DFS, finds the first node containing a vertex.
        Parameters:
            node (Node object)
            index (str)
        Returns:
            Node object or None'''

        if index in node.value:
            return node
        for child in node.children:
            if find_first(child,index) is not None:
                return find_first(child,index)
        return None

    def size_connected_subtree(node,index):
        ''' Using DFS and starting from (node), 
            computes the size of the subtree where each node contains (index).
        Parameters:
            node (Node object)
            index (str)
        Returns:
            size (int)'''

        size=0
        if index in node.value:
            size+=1
            for child in node.children:
                size+=size_connected_subtree(child,index)
            return size
        else:
            return 0

    def count_occurences(node,index):
        ''' Using DFS, counts the number of occurences of index starting from node.
        Parameters:
            node (Node object)
            index (str)
        Returns:
            occurences (int)'''

        occurence=0
        if index in node.value:
            occurence+=1
        for child in node.children:
            occurence+=count_occurences(child,index)
        return occurence

    def aux(tree,index):
        ''' For a given vertex (represented by index), 
            checks if the subgraph of the tree where all node contain index is connex.
        Parameters:
            tree (Tree object)
            index (int)
        Returns:
            boolean'''
        
        count_total=count_occurences(tree.root,index)

        count_subtree=size_connected_subtree( find_first(tree.root,index) ,index)

        return count_total==count_subtree
    
    for index in graph.keys():
        if not aux(tree,index):
            return False

    return True


def is_tree_decomposition(tree,graph):
    ''' Checks if tree is a tree decomposition of graph.
    Parameters: 
        tree (Tree object)
        graph (defaultdict)
    Returns:
        boolean'''

    if not is_connex(tree,graph) or not check_vertices_edges(tree,graph):
        return False
    return True