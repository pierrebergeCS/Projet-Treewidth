from Classes import Node, Tree
from Path_decomposition import canonical_path

def join_subtree(parent, children,tree,flag):#flag is here just for us to know if we still need to remove the edges between the "original" children and their parent
    children=children[:]    #ne marche pas sinon
    if not flag:
        flag=True
        for child in children:
            tree.delete_edge(parent,child)
    if len(children)==1:
        parent.add_children(children)
        children[0].add_parent(parent)
        tree.add_node(parent)
    else:
        #left
        parent_left=Node(0,parent.value)

        parent.add_children([parent_left])
        parent_left.add_parent(parent)

        parent_left.add_children([children[0]])
        children[0].add_parent(parent_left)
        tree.add_node(parent_left)
            
        #right
        parent_right=Node(0,parent.value)

        parent.add_children([parent_right])
        parent_right.add_parent(parent)
        tree.add_node(parent_right)
        
        join_subtree(parent_right,children[1:],tree,flag)

a=Node(0,"père")
b=Node(0,"b")
c=Node(0,"c")
d=Node(0,"d")
e=Node(0,"e")
a.add_children([b,c,d])
b.add_parent(a)
c.add_parent(a)
d.add_parent(a)
#e.add_parent(a)

t=Tree(a,[a,b,c,d])
print(t)
print()
join_subtree(a,a.children,t,False)
print(t)

#function below is to be fixed
def adding_join_subtree(tree, parent, children):
    if any(children):
        next=[]
        for child in children:
            next.append((child,child.children))
        join_subtree(parent,children,tree,False)
        for (a,b) in next:
            join_subtree(a,b,tree,False)


def canonical_tree(tree):
    #first step:
    adding_join_subtree(tree,tree.root,tree.root.children)
    #adding canonical paths


canonical_tree(t)
print(t)