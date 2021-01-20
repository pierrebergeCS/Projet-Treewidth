from Classes import Node, Tree
from Path_decomposition import nice_path
from Tree_decomposition import adding_join_subtree, adding_empty_leaves, adding_join_subtree, canonical_tree

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
a=Node('a')
b=Node('b')
c=Node('c')
d=Node('d')
e=Node('e')
a.add_children([b,c,d,e])
t=Tree(a)
tree.append(t)

if True:
    t=tree[3]
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