from Classes import Node, Tree

def sym_difference(node1,node2):
    '''returns the symmetric difference between the values (of type string) 
    of two nodes in the form of a list of strings'''
    sym_diff=[]
    for char in node1.value:
        if char not in node2.value:
            sym_diff.append(char)
    return sym_diff

def canonical_path(parent,child,tree): #the path is considered as a tree object here
    ''' adds forget and add nodes to the path/tree
    between parent and its child '''
    starting_sym_diff=sym_difference(parent,child) 
    #list of char that we should get rid of as they don't appear in child.value
    arrival_sym_diff=sym_difference(child,parent)
    #list of char that we should add to reach the child
    tree.delete_edge(parent,child)
    #we substitude this edge by the new nodes

    string=parent.value
    former_node=parent

    #first step: adding forget nodes until reaching the node with value node1.value intersect node2.value
    for char in starting_sym_diff:
        string=string.replace(char,"")
        actual_node=Node(0,string)
        former_node.add_children([actual_node])
        actual_node.add_parent(former_node)
        tree.add_node(actual_node)
        former_node=actual_node
    
    if len(arrival_sym_diff)==0: 
        #if node2.value included in node1.value then the former_node.value=node2.value
        #so no need to have the two in the tree/path
        (former_node.parent).add_children([child])
        child.add_parent(former_node.parent)
        tree.delete_edge(former_node,former_node.parent)


    if len(arrival_sym_diff)>=1: 
        # because the arrival node aka node2 is already in the tree/path:
        # no need to add a node that has the same value
        arrival_sym_diff=arrival_sym_diff[:-1]
    
        #second step: add nodes until reaching the node2
        for char in arrival_sym_diff:
            string=string+char
            actual_node=Node(0,string)
            former_node.add_children([actual_node])
            actual_node.add_parent(former_node)
            tree.add_node(actual_node)
            former_node=actual_node
        
        child.add_parent(former_node)
        former_node.add_children([child])

    

def nice_path(path):#type(path)==tree
    if path.root.value!="":
        empty_node=Node(0,"")
        empty_node.add_children([path.root])
        path.root.add_parent(empty_node)
        path.add_node(empty_node)
        path.root=empty_node
    
    actual_node=path.root
    while actual_node.children!=[]:
        former_node=actual_node
        actual_node=former_node.children[0] #there is only a child
        canonical_path(former_node,actual_node,path)
    if actual_node.value!="":
        former_node=actual_node
        empty_node=Node(0,"")
        former_node.add_children([empty_node])
        empty_node.add_parent(former_node)
        path.add_node(empty_node)
        canonical_path(former_node,empty_node,path)

a=Node(0,"abcdef")
b=Node(0,"abcxyz")
a.add_children([b])
b.add_parent(a)
t=Tree(a,[a,b])
print(t)

print("\n next\n")
nice_path(t)
print(t)