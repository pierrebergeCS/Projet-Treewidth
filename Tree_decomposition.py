from Classes import Node, Tree
from Path_decomposition import canonical_path

### All the functions below are in-place !

def join_subtree(parent, children,tree,flag):
    '''inputs: parent (Node object) - children (list of Node objects) - tree (Tree object) - flag (boolean)
    makes the tree satisfy the 3rd condition of nice td: 
    whenever a node has more than a child, the value of every child is the same as the value of the node'''
    #flag is here just for us to know if we still need to remove the edges between the "original" children and their parent
    children=children[:]    #won't work with deepcopy
    if not flag:
        flag=True
        for child in children:
            parent.delete_edge(child)
    if len(children)==1:
        parent.add_children(children)
    else:
        #left subtree: 
        # if the child is different from the parent,
        # we add a node of value parent.value between parent and child
        # else, we just (re)connect the child and the parent
        if children[0].value!=parent.value:
            parent_left=Node(parent.value)
            parent_left.add_parent(parent)
            children[0].add_parent(parent_left)
        else:
            children[0].add_parent(parent)
            
        #right subtree:
        #we start by adding the right child of the parent with the value parent.value
        parent_right=Node(parent.value)
        parent_right.add_parent(parent)
        #apply join_subtree on the parent_right and the remaining children
        join_subtree(parent_right,children[1:],tree,flag)

def adding_join_subtree(tree, parent, children):
    '''inputs: tree (Tree object) - parent (Node object) - children (list of Node objects)
    this function applies join_subtree between every non-lead node and its child/children
    #when a node has only a child, join_subtree don't change anything'''
    
    if any(children):
        next=[]
        for child in children:
            next.append((child,child.children))
        join_subtree(parent,children,tree,False)
        for (a,b) in next:
            adding_join_subtree(tree,a,b)

def adding_empty_leaves(tree):
    '''inputs: tree (Tree object) - node (Node object)
    look for the leaves of the tree, check if they are of empty value, 
    and if they are not, adds an empty node as child.
    This function will also adds an empty root if necessary.'''
    def aux(node):
        if node.children!=[]:
            for child in node.children:
                adding_empty_leaves(child)
        else:
            if node.value!='':
                empty_node=Node('')
                empty_node.add_parent(node)

    if tree.root.value!='':
        empty_node=Node("")
        tree.root.add_parent(empty_node)
        tree.root=empty_node
    aux(tree)
    


def adding_canonical_paths(tree,parent,children):
    '''inputs: tree (Tree object) - parent (Node Object) - children (list of Node objects)
    This function makes a path between every node in the tree and its child a canonical one if it's not already.'''
    if len(children)>1:
        #since in the function canonical_tree, we apply apply_join_subtree before this function, 
        #we know that whenever a node has multiple children, they are all the same.
        for child in children:
            adding_canonical_paths(tree,child,child.children)
    elif len(children)==1:
        child=children[0]
        canonical_path(tree,parent,child)
        adding_canonical_paths(tree,child,child.children)

def canonical_tree(tree):
    '''inputs: Tree object
    Transforms any tree decomposition into a nice one.'''
    adding_join_subtree(tree,tree.root,tree.root.children)
    adding_empty_leaves(tree)
    adding_canonical_paths(tree,tree.root,tree.root.children)