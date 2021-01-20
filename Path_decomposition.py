from Classes import Node, Tree

def sym_difference(node1,node2):
    '''inputs: two Node objects
    output: a list of strings
    returns the symmetric difference between the values
    of two nodes in the form of a list of strings'''
    sym_diff=[]
    for char in node1.value:
        if char not in node2.value:
            sym_diff.append(char)
    return sym_diff

def canonical_path(path,parent,child): 
    ''' inputs: path (Tree object) - parent (Node object) - child (Node object)
    output: nothing 
    adds forget nodes and add nodes to the path between parent and its child '''
    starting_sym_diff=sym_difference(parent,child) 
    #list of char that we should get rid of as they don't appear in child.value
    arrival_sym_diff=sym_difference(child,parent)
    #list of char that we should add to reach the child
    parent.delete_edge(child)
    #we substitude this edge by the new nodes

    string=parent.value
    former_node=parent

    #first step: adding forget nodes until reaching the node with value (node1.value intersect node2.value)
    for char in starting_sym_diff:
        string=string.replace(char,"",1)
        actual_node=Node(string)
        actual_node.add_parent(former_node)
        former_node=actual_node
    
    #second step: forget nodes
    if len(arrival_sym_diff)==0:
        #if node2.value included in node1.value then the former_node.value=node2.value
        #so no need to have the two in the path
        former_node.add_children(child.children)
        #beware, the child is no longer part of the path

    if len(arrival_sym_diff)>=1: 
        # because the arrival node aka node2 is already in the tree/path:
        # no need to add a node that has the same value
        arrival_sym_diff=arrival_sym_diff[:-1]
    
        #second step: add nodes until reaching the node2
        for char in arrival_sym_diff:
            string=string+char
            actual_node=Node(string)
            actual_node.add_parent(former_node)
            former_node=actual_node
        
        child.add_parent(former_node)

    

def nice_path(path):
    '''takes a path (Tree object) as input, and makes it a nice path (Tree object)'''
    if path.root.value!="": 
        #in case the root is non empty, we add an empty node as a root
        empty_node=Node()
        path.root.add_parent(empty_node)
        path.root=empty_node
    
    actual_node=path.root
    while actual_node.children!=[]:
        former_node=actual_node
        actual_node=former_node.children[0] #there is only a child each time
        canonical_path(path,former_node,actual_node)
    if actual_node.value!="":
        #in case the last node of the path is non empty, we add an empty node at the end
        former_node=actual_node
        empty_node=Node('')
        empty_node.add_parent(former_node)
        canonical_path(path,former_node,empty_node)