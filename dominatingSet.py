import networkx as nx
import matplotlib.pyplot as plt
from sidefunctions import hierarchy_pos

import Classes
from Tree_decomposition import canonical_tree
from Path_decomposition import set_substraction


class subNode(Classes.Node):
    def __init__(self,value=[],type_of=None,change=None):
        ''' type=1 iif it's an introduce node
            type=2 iif it's a forget node
            type=3 iif it's a join node
            type=4 iif it's leaf
            type=5 iif it's an introduce edge

            change= the difference between the node and it's child/children. (list of str)
            colors= dictionnary of ( tuple of (vertex:color) : size of dominating set)'''

        self.value = value
        self.parent = None
        self.children = []
        self.type_of=type_of
        self.change=change
        self.colors={}

class subTree(Classes.Tree):
    def __init__(self, root):
        self.root=root

    def __str__(self):
        ''' Using matplotlib and networkx, outputs a vizual representation of the tree, 
        and prints an empty string in the console.
        
        Returns:
            empty str'''

        def DFS_brute(node):
            for child in node.children:
                child.parent=node
                DFS_brute(child)
        DFS_brute(self.root)

        graph=nx.Graph()
        correspondance=[]
        graph.nodes(data=True)
        d={}
        def DFS(node):
            if correspondance==[]:
                graph.add_node(0)
                correspondance.append(node)
                if node.value==[]:
                    if node.type_of:
                        d[0]="Ø "+'\n'+str(node.type_of)
                    else:
                        d[0]="Ø "
                else:
                    if node.type_of==5:
                        d[0]=",".join(node.value)+'| ' + "".join(node.change)
                    elif node.type_of:
                        print('was here')
                        d[0]=",".join(node.value)+'\n'+str(node.type_of)
                    else:
                        d[0]=','.join(node.value)
                
                for child in node.children:
                    #the problem starts here, because child.parent =/= node (equality of memory adresses)
                    DFS(child)
            else:
                index_node=len(correspondance)
                graph.add_node( index_node )
                if node.value==[]:
                    if node.type_of:
                        d[index_node]="Ø "+'\n'+str(node.type_of)
                    else:
                        d[index_node]="Ø "
                else:
                    if node.type_of==5:
                        d[index_node]=",".join(node.value)+' | ' + ",".join(node.change)
                    elif node.type_of:
                        d[index_node]=",".join(node.value)+"\n"+str(node.type_of)
                    else:
                        d[index_node]=",".join(node.value)
                correspondance.append(node)
                index_father=correspondance.index(node.parent)
                graph.add_edge(index_father,index_node)
                for child in node.children:
                    DFS(child)
        
        DFS(self.root)
        pos=hierarchy_pos(graph,0)
        nx.draw(graph,pos,labels=d,with_labels=True,node_size=[200*len(node) for node in d.values()],node_color='red')
        plt.show()
        return ""

def usual_types(root):
    ''' given a nice tree, changes the types of node (altough we still need introduce edges)
    
    Parameters:
        root: Node Class'''
    next=[root]

    while next:
        tempo=[]
        for node in next:
            if len(node.children)==2:
                node.type_of=3
                node.change=None
                tempo.extend(node.children)
            else:
                if node.children==[]:
                    node.type_of=4
                    node.change=None
                else:
                    if node.children:
                        if len(node.value)>len(node.children[0].value):
                            node.type_of=1
                            node.change=set_substraction(node,node.children[0])
                        elif len(node.value) < len(node.children[0].value):
                            node.type_of=2
                            node.change=set_substraction(node.children[0],node)
                tempo.extend(node.children)
        next=tempo[:]

def introduce_edge_node(root,graph):
    ''' Adds introduce edge node.
    Parameters: 
        root: Class Node.
        graph: dictionnary representing adjacency list. '''
    next=[root]
    while next:
        tempo_search=[]
        for node in next:
            if node.type_of==2:
                vertex=node.change[0]
                start=node
                end=node.children[0]
                for potential_neighbor in node.value:
                    if potential_neighbor in graph[vertex]:
                        start.delete_edge(end)
                        tempo=subNode(end.value,type_of=5,change=[vertex,potential_neighbor])
                        tempo.add_parent(start)
                        end.add_parent(tempo)
                        start=tempo
                tempo_search.append(end)
            else:
                tempo_search.extend(node.children)
        next=tempo_search[:]

def very_canonical_tree(tree,graph):
    '''From tree, returns a very canonical one (in particular: all nodes are object of the class subNodes).

    Parameters: 
        tree: Tree object.
        graph: dictionnary representing adjacency list.
        
    Returns:
        root: subNode object'''

    canonical_tree(tree)
    root=tree.root
    usual_types(root)
    introduce_edge_node(root,graph)

    next = [root]
    while next:
        tempo=[]
        for node in next:
            subnode=subNode(node.value,node.type_of,node.change)
            parent=node.parent
            if parent:
                node.delete_edge(parent)
                subnode.add_parent(parent)
            
            list_children=node.children[:]
            for child in list_children:
                child.parent=subnode
            subnode.children=list_children[:]
            
            tempo.extend(list_children)
            if node==root:
                root=subnode
        next=tempo[:]
    return root

def solver(root):
    ''' Given a very canonical tree, solves the min-dominating set problem.
    Parameters:
        root: subNode object'''

    typeof=root.type_of
    if typeof==4:
        root.colors={():0}
    if root.children and root.children[0].colors=={}:
        solver(root.children[0])
    if typeof==3 and root.children[1].colors=={}:
        solver(root.children[1])

    if typeof==1:
        v=root.change[0]
        for color in root.children[0].colors:
            root.colors[color+((v,1),)]=1+root.children[0].colors[color]
            root.colors[color+((v,2),)]=root.children[0].colors[color]
            root.colors[color+((v,0),)]=float('inf')

    if typeof==2:
        v=root.change[0]
        for color in root.children[0].colors:
            i=0
            for c in color:
                if c[0]==v:
                    break
                i+=1
            break 
        for color in root.children[0].colors:
            if color[i][1]!=2:
                key, key_child = color[:i]+color[i+1:], color
                if key in root.colors:
                    root.colors[key]=min(root.colors[key], root.children[0].colors[key_child])
                else:
                    root.colors[key]=root.children[0].colors[key_child]

    if typeof==5:
        [u,v]=root.change
        for color in root.children[0].colors:
            i0,i1,i=len(color),len(color),0
            for c in color:
                if c[0]==v:
                    i0=i
                elif c[0]==u:
                    i1=i
                i+=1
            break 
        flag = False
        for color in root.children[0].colors:
            if not (color[i1][1]==0 and color[i0][1]==1) and not (color[i1][1]==1 and color[i0][1]==0):
                if color[i1][1]==1 and color[i0][1]==2: # couleur(u)=1 et couleur(v)=2
                    root.colors[color[:i0]+((v,0),)+color[i0+1:]]=root.children[0].colors[color]
                    root.colors[color]=root.children[0].colors[color] 
                elif color[i1][1]==2 and color[i0][1]==1:
                    root.colors[color[:i1]+((u,0),)+color[i1+1:]]=root.children[0].colors[color]
                    root.colors[color]=root.children[0].colors[color]
                else:
                    root.colors[color]=root.children[0].colors[color]

    if typeof==3:
        for color1 in root.children[0].colors:
            for color2 in root.children[1].colors:
                correspondance = [0 for _ in range(len(color1))]
                for i in range(len(color1)):
                    v=color1[i][0]
                    for j in range(len(color2)):
                        if color2[j][0]==v:
                            correspondance[i]=j
                            break
                break
            break

        for color1 in root.children[0].colors:
            for color2 in root.children[1].colors:
                new_color=[]
                flag=False
                for i in range(len(color1)):
                    if color1[i][1]==color2[correspondance[i]][1]==1:
                        new_color.append((color1[i][0],1))
                    elif [ color1[i][1], color2[correspondance[i]][1] ] in [ [2,0],[0,2] ]:
                        new_color.append( (color1[i][0],0) )
                    elif color1[i][1]==color1[correspondance[i]][1]==2:
                        new_color.append( (color1[i][0],2) )
                    else:
                        flag=True
                        break
                if not flag:
                    new_color=tuple(new_color)
                    number=0
                    for i in range(len(new_color)):
                        if new_color[i][1]==1:
                            number+=1

                    if new_color in root.colors:
                        root.colors[new_color]=min( root.colors[new_color], root.children[0].colors[color1]+root.children[1].colors[color2]-number )
                    else:
                        root.colors[new_color]=root.children[0].colors[color1]+root.children[1].colors[color2]-number


# Examples of graphs and the cardinal of their min-dominating set

a=subNode(['a','b','c'])
b=subNode(['c','d','e','f'])
c=subNode(['d','f','e'])
b.add_parent(a)
t=subTree(a)
graph={ "a":["b","c"], "b":["a","c"], "c":["a","b","d","e","f"], "e":["c","f"], "f":["e","d","c"], "d":["f","c"] }
t=subTree(very_canonical_tree(t,graph))
#solver(t.root)
#print(t.root.colors)

a=subNode(["1"])
b=subNode(["1","2"])
c=subNode(["1","3"])
a.add_children([b,c])
d=subNode(["2","4"])
e=subNode(["2","5"])
e.add_children([subNode(["10","5"])])
b.add_children([d,e])
f=subNode(["3","6"])
g=subNode(["3","7"])
c.add_children([f,g])
t=subTree(a)
graph={ "1":["2","3"], "2":["1","4","5"], "4":["2"], "5":["2", "10"], "10":["5"], "3":["1", "6", "7"], "6":["3"],  "7":["3"]}
t=subTree(very_canonical_tree(t,graph))

#solver(t.root)
#print(t.root.colors)

a=subNode(["1","2","3"])
b=subNode(["1","4","3","2"])
b.add_parent(a)
graph={ "1":["4","2"], "2":["1","3","4"], "3":["2","4"], "4":["3","1","2"] }
t=subTree(a)
t=subTree(very_canonical_tree(t,graph))
#solver(t.root)

a=subNode([str(i) for i in range(1,11)])
graph={ "1":["6","3","4"], "2":["7","5","4"], "3":["1","5","8"], "4":["2","1","9"], "5":["10", "2", "3"], "6":["10", "1","7"],
"7":["6","8","2"], "8":["7","9","3"], "9":["7","10","4"], "10":["1","9","5"]}
t=subTree(a)
t=subTree(very_canonical_tree(t,graph))
#solver(t.root)

a=subNode([str(i) for i in range(1,9) ])
graph={ "1":["2","3","4","5","6"], "2":["3","1"], "3":["1","2"], "4":["1","5"], "5":["1","4"], "6":["1","7"], "7":["6","8"], "8":["7"] }
t=subTree(a)
t=subTree(very_canonical_tree(t,graph))
#solver(t.root)