class Node:
    def __init__(self, value=''):
        '''takes the value of type string as input and returns a Node object 
        with neither a parent nor children.'''
        #note to myself: index
        self.value=value #string
        self.parent=None
        self.children=[]#list of Node objects

    def add_children(self,list_children):
        '''takes a list of nodes as input 
        and make them children of the node self'''
        if self.children is None:
            self.children=list_children
        else:
            self.children.extend(list_children)
        #making self a parent to every node in list_nodes
        for child in list_children:
            child.parent=self

    def add_parent(self,node):
        self.parent=node
        (node.children).append(self)

    def delete_edge(self,node):
        '''takes a single node object as input 
        and deletes it from self.children or self.parent'''
        if node==self.parent:
            self.parent=None
            node.children.remove(self)
        elif node in self.children:
            self.children.remove(node)
            node.parent=None
    
    def __str__(self):
        '''a method that displays the node, its parent and its children 
        (if they exist) on three separate lines'''
        string=''
        if self.parent is not None:
            string+=self.parent.value+'\n|\n'
        string+=self.value+'\n|\n'
        for child in self.children:
            string+=child.value+' '
        return string

class Tree:
    def __init__(self,root):
        '''Tree object given the root (Node object)'''
        self.root=root

    def __str__(self):
        '''gives an ugly vizualization of the tree, example:
        0|
        1-2|
        3|4-5|
        means nodes 1 and 2 are both children of 0, 3 is the child of 1
        and 4 and 5 are children of 2
         '''
        def represent(t,list_of_lists):
            '''aux function that use BFS to print all nodes on a "level" 
            and calls itself on the next one '''
            if any(list_of_lists): #if the level is not empty
                next=[]
                result=''
                for group in list_of_lists: # a group is a list of children of a specific node
                    if any(group): #to check if there is any children left
                        level=[]
                        for node in group:
                            if node.value!='':
                                level.append(str(node.value))
                            else:
                                level.append(str("Ø"))
                            next+=[node.children]
                        result+="-".join(level) #children of the same node are separated by '-'
                    result+="|" #separates children of two differents nodes
                result+="\n" 
                return result+represent(t,next) # to go from the actual level to the next one

            else: # checks if the level is empty to end recursion
                return ''

        return represent(self,[[self.root]])