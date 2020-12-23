from Classes import Node, Tree

def sym_difference(node1,node2):
    sym_diff=[]
    for char in node1.value:
        if char not in node2.value:
            sym_diff.append(char)
    return sym_diff

def canonical_path(parent,child,tree):
    starting_sym_diff=sym_difference(parent,child)
    arrival_sym_diff=sym_difference(child,parent)
    tree.delete_edge(parent,child)
    string=parent.value
    former_node=parent
    for char in starting_sym_diff:
        string=string.replace(char,"")
        actual_node=Node(0,string)
        former_node.add_children([actual_node])
        actual_node.add_parent(former_node)
        tree.add_node(actual_node)
        former_node=actual_node
    if len(arrival_sym_diff)>1:
        arrival_sym_diff=arrival_sym_diff[:-1]
    for char in arrival_sym_diff:
        string=string+char
        actual_node=Node(0,string)
        former_node.add_children([actual_node])
        actual_node.add_parent(former_node)
        tree.add_node(actual_node)
        former_node=actual_node
    if child.value!="":
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

a=Node(0,"a")
b=Node(0,"ab")
a.add_children([b])
b.add_parent(a)
t=Tree(a,[a,b])
print(t)

print("\n next\n")

nice_path(t)

print(t)
