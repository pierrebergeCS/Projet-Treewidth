from Classes import Node, Tree
from Path_decomposition import nice_path, set_substraction
from Tree_decomposition import adding_join_subtree, adding_empty_leaves, adding_join_subtree, clean_tree, canonical_tree
from Verification import is_connected, check_vertices_edges, fill_dict, is_nice_tree


####### examples on path
path=[]

#case0
a=Node(['a','b','c','d','e','f','g'])
t=Tree(a)
path.append(t)

#case1
a=Node()
b=Node(['a','b'])
b.add_parent(a)
c=Node(['a'])
c.add_parent(b)
d=Node(['a','b','c'])
d.add_parent(c)
e=Node(['a','b'])
e.add_parent(d)
f=Node()
f.add_parent(e)
g=Node()
g.add_parent(f)
t=Tree(a)
path.append(t)

#case2
a=Node(['a','b','c'])
b=Node(['d'])
b.add_parent(a)
t=Tree(a)
path.append(t)

if True:
    t=path[2] 
    print('printing the initial path:')
    print('printing the canonical path:')   

    #clean_tree(t.root)
    print(t)
    nice_path(t)
    print(t)
    print(t.console())

####### examples on tree

tree=[]

#case0
a=Node(['1'])
t=Tree(a)
tree.append(t)

#case1
a=Node()
z=Node()
z.add_parent(a)
b=Node()
c=Node()
z.add_children([b,c])
d=Node(['a'])
d.add_parent(b)
e=Node(['a'])
e.add_parent(c)
f=Node()
f.add_parent(d)
g=Node()
g.add_parent(e)
t=Tree(a)
tree.append(t)

#case2
a=Node(['a'])
b=Node(['b'])
c=Node(['c'])
a.add_children([b,c])
t=Tree(a)
tree.append(t)

#case3 redundant empty node but still a nice tree
a=Node(['a','f','g'])
b=Node(['b','g','h'])
c=Node(['c'])
d=Node(['d'])
e=Node(['e'])
a.add_children([b,c,d,e])
t=Tree(a)
tree.append(t)

if True:
    t=tree[1]
    print('printing the initial tree:')
    print(t)

    print('the size of the tree is:')
    print(t.size())
    print()

    print('printing the canonical tree:')
    canonical_tree(t)
    print(t)

    print('the width of the tree is:')
    print(t.width())
    print()

    print('the size of the tree is:')
    print(t.size())

####### example on verification

verification=[]
graphs=[]

#case0
a=Node(['a'])
b=Node(['b'])
c=Node(['c'])
d=Node(['d'])
aa=Node(['f'])
a.add_children([b,c,d])
aa.add_parent(b)
t=Tree(a)
verification.append(t)
graphs.append({'a': [], 'b':[], 'c':[], 'd':[], 'f':[]})

#case1
a=Node(['a','b','f'])
b=Node(['b','c','f'])
b.add_parent(a)
c=Node(['c','d','f'])
c.add_parent(b)
d=Node(['e','d','f'])
d.add_parent(c)
t=Tree(a)
verification.append(t)
graphs.append({'a':['b','f'] , 'b': ['c','a'] , 'c':['b','d'] , 'd':['e','c'] , 'e':['d','f'] , 'f':['a','e']} )

if not True:
    case=0
    t=verification[case]
    graph=graphs[case]
    print('repr tree')
    print(t)
    print('\ndict of edges according to the tree')
    print( fill_dict(t) )
    print('\ndoes the tree cover all edges of the initial graph and all its vertices ?')
    print(check_vertices_edges(t,graph))
    print('\nare the different subgraphs of the tree containing each vertex connected ?')
    print(is_connected(t,graph))
    
    canonical_tree(t)
    print(t)
    print(is_nice_tree(t))

a=Node(['e','f'])
b=Node(['b','e','d'])
b.add_parent(a)
c=Node(['b','c','d'])
c.add_parent(b)
d=Node(['d','g'])
e=Node(['b','c','a'])
c.add_children([d,e])

if not True:
    t=Tree(a)

    canonical_tree(t)

    print(t)