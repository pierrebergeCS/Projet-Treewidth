from Classes import Node, Tree
from Path_decomposition import nice_path
from Tree_decomposition import adding_join_subtree, adding_empty_leaves, adding_join_subtree, canonical_tree
from Verification import is_connex,is_connex2, check_vertices_edges, fill_dict

####### examples on path
path=[]

#case0
a=Node('abcdefg')
t=Tree(a)
path.append(t)

#case1
a=Node('')
b=Node('a')
b.add_parent(a)
c=Node('ab')
c.add_parent(b)
d=Node('abc')
d.add_parent(c)
e=Node('ab')
e.add_parent(d)
f=Node('a')
f.add_parent(e)
g=Node('')
g.add_parent(f)
t=Tree(a)
path.append(t)

#case2
a=Node('abc')
b=Node('d')
b.add_parent(a)
t=Tree(a)
path.append(t)

#abnormal case (due to the way symmetric diff is built, but that's not a big problem)
a=Node('')
b=Node('*')
b.add_parent(a)
c=Node('**')    
c.add_parent(b)
d=Node('***')
d.add_parent(c)
e=Node('**')
e.add_parent(d)
f=Node('*')
f.add_parent(e)
g=Node('')
g.add_parent(f)
t=Tree(a)
path.append(t)

if not True:
    t=path[0]
    print('printing the initial path:')
    print(t)
    
    print('printing the canonical path:')
    nice_path(t)
    print(t)

####### examples on tree

tree=[]

#case0
a=Node('1')
t=Tree(a)
tree.append(t)

#case1
a=Node()
b=Node()
c=Node()
a.add_children([b,c])
d=Node('a')
d.add_parent(b)
e=Node('b')
e.add_parent(c)
f=Node()
f.add_parent(d)
g=Node()
g.add_parent(e)
t=Tree(a)
tree.append(t)

#case2
a=Node('a')
b=Node('b')
c=Node('c')
a.add_children([b,c])
t=Tree(a)
tree.append(t)

#case3 redundant empty node but still a nice tree
a=Node('afg')
b=Node('bgh')
c=Node('c')
d=Node('d')
e=Node('e')
a.add_children([b,c,d,e])
t=Tree(a)
tree.append(t)

if not True:
    t=tree[0]
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
a=Node('a')
b=Node('b')
c=Node('c')
d=Node('d')
aa=Node('f')
a.add_children([b,c,d])
aa.add_parent(b)
t=Tree(a)
verification.append(t)
graphs.append({'a': [], 'b':[], 'c':[], 'd':[], 'f':[]})

#case1
a=Node('abf')
b=Node('bcf')
b.add_parent(a)
c=Node('cdf')
c.add_parent(b)
d=Node('edf')
d.add_parent(c)
t=Tree(a)
verification.append(t)
graphs.append({'a':['b','f'] , 'b': ['c','a'] , 'c':['b','d'] , 'd':['e','c'] , 'e':['d','f'] , 'f':['a','e']} )

if True:
    t=verification[1]
    graph=graphs[1]
    print('repr tree')
    print(t)
    print('\ndict of edges according to the tree')
    print( fill_dict(t) )
    print('\ndoes the tree cover all edges of the initial graph and all its vertices ?')
    print(check_vertices_edges(t,graph))
    print('\nare the different subgraphs of the tree containing each vertex connex ?')
    print(is_connex2(t,graph))