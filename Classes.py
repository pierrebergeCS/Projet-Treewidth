class Node:
    def __init__(self, index, value=''):
        '''takes the index and the value as input and returns a Node object 
        with neither a parent nor children.'''
        self.index=index
        self.value=value #string
        self.parent=None
        self.children=[]#list of Node objects

    def __str__(self):
        '''a method that displays the node, its parent and its children 
        (if they exist) on three separate lines'''
        string=''
        if self.parent is not None:
            string+=str(self.parent)+'\n|\n'
        string+=str((self.index))+'\n|\n'
        for child in self.children:
            string+=str(child.index)+' '
        return string

    def add_children(self,list_nodes):
        '''takes a list of nodes as input 
        and make them children of the node self'''
        if self.children is None:
            self.children=list_nodes
        else:
            self.children.extend(list_nodes)

    def add_parent(self,node):
        '''takes a single node object as input
        and makes it the self parent''' 
        self.parent=node

    def delete_edge(self,node):
        '''takes a single node object as input 
        and deletes its from self.children or self.parent'''
        if node==self.parent:
            self.parent=None
        elif node in self.children:
            self.children.remove(node)
class Tree:
    def __init__(self,root,list_nodes):
        '''creates a Tree object with a root and a list of nodes'''
        self.list=list_nodes
        self.root=root
        self.index_list=[node.index for node in self.list] 
        self.slot=max(self.index_list)+1 #gives a possible index that has not been used yet
        self.width=max([len(node.value) for node in self.list])

    def add_edge(self,parent,child):
        '''adds an edge between two nodes
        with one of them being the (future) child of the other'''
        parent.add_children([child])
        child.add_parent(parent)
    
    def delete_edge(self,u,v):
        '''deletes the edges between two nodes u, v of the tree'''
        u.delete_edge(v)
        v.delete_edge(u)

    def add_node(self, node):
        '''adds a node to the tree
        and updates the slot'''
        node.index=self.slot
        self.slot+=1
        self.list.append(node)
        self.index_list.append(node.index)

    def delete_node(self,node):
        '''deletes a node from the tree.list 
        and every edge that connects it to other nodes of the tree'''
        (node.parent).delete_edge(node)
        for child in node.children:
            child.delete_edge(node)
        self.list.remove(node)
        self.index_list.remove(node.index)


    def __str__(self):
        '''gives an ugly vizualization of the tree, example:
        0|
        1-2|
        3|4-5|
        means nodes 1 and 2 are both children of 0, 3 is the child of 1
        and 4 and 5 are children of 2
         '''
        def represent(t,list_of_lists,number):
            '''aux function that use BFS to print all nodes on a "level" 
            and calls the function on the next one 
            This function changes the indexes to BFS ordering for easier readability'''

            if any(list_of_lists): #if the level is not empty
                next=[]
                result=''
                for group in list_of_lists: # a group is a list of children of a specific node
                    if any(group): #to check if there is any children left
                        level=[]
                        for node in group:
                            node.index=number #updating the index
                            number+=1 
                            level.append(str(node.index))
                            next+=[node.children]
                        result+="-".join(level) #children of the same node are separated by '-'
                    result+="|" # this symbol separates children of two differents nodes
                result+="\n" 
                return result+represent(t,next,number) # to go from tha actual level to next one

            else: # checks if the level is empty to end recursion
                t.slot=number #updating the slot
                return ''

        return represent(self,[[self.root]],0)+"\n\n"+"   |||   ".join([str(node.index)+":"+str(node.value) for node in self.list]) 
        # simple string representation + dictionnary with couples (node.index: node.value) are separated by |||