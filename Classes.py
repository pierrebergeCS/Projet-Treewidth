class Node:
    ''' A class used to represent a node of a tree

    Attributes
    ----------
    value : str
    parent : a Node object
    children : a list of Node objects

    Methods
    -------
    add_children :  adds a list of children to the node
    add_parent : adds a parent to the node
    delete_edge : deletes the edge between the node and another
    ___str___: gives a basic visual representation of the node, together with its parent and children'''

    def __init__(self, value=''):
        ''' Initializes the Node object with the value given in parameters, otherwise it's just an empty Node.
        Parameters:
            value (str)'''

        self.value = value
        self.parent = None
        self.children = []

    def add_children(self, list_children):
        ''' Adds a list of Node objects to the already existing self.children, and adds self as a parent to these nodes.
        Parameters: 
            list_children (Node objects list)'''

        self.children.extend(list_children)
        for child in list_children:
            child.parent = self

    def add_parent(self, node):
        ''' Makes a node a parent to self, and adds self as a child to the list of children to the parent
        Parameters:
            node (Node object)'''

        self.parent = node
        (node.children).append(self)

    def delete_edge(self, node):
        ''' Deletes the edge between self and node (if it exists). 
        Parameters:
            node (Node object)'''
        if node == self.parent:
            self.parent = None
            node.children.remove(self)
        elif node in self.children:
            self.children.remove(node)
            node.parent = None

    def __str__(self):
        ''' gives a visual representation of the node, its parent and its children'''

        string = ''
        if self.parent is not None:
            string += self.parent.value+'\n|\n'
        string += self.value+'\n|\n'
        for child in self.children:
            string += child.value+' '
        return string


class Tree:
    ''' A class used to represent a tree, by knowing only its root

    Attributes
    ----------
        root (Node object)

    Methods
    -------
        width : gives the width of the tree
        size : gives the size of the tree
        ___str___ : gives a very basic and ugly representation of the tree'''

    def __init__(self, root):
        ''' Initializes the Tree object given its root.
        Parameters:
            root (Node object)'''

        self.root = root

    def width(self):
        ''' Gives the width of the tree.
        Returns:
            width (int)'''

        def bfs(level):
            ''' aux function that uses BFS to computes the largest width on a level and calls itself on the next one
            Parameters: 
                level (Node objects list)
            Returns:
                max_cardinal_sub_graph (int): the maximum cardinal of all the nodes in the subgraph starting from level'''

            if any(level):
                next = []
                result = 0
                for node in level:
                    result = max(result, len(node.value))
                    next.extend(node.children)
                return max(result, bfs(next))
            else:
                return 0
        
        return bfs([self.root])-1  # reminder: width=cardinal of a X -1

    def size(self):
        ''' Gives the size of the tree
        Returns:
            size (int)'''
    
        def bfs(level):
            '''aux function that use BFS to computes the number of nodes on a level, and calls itself on the next one.
            Parameters:
                level (Node object list)
            Returns:
                size_subgraph (int): size of the subgraph starting from level'''

            if any(level):
                next = []
                result = 0
                for node in level:
                    result += 1
                    next.extend(node.children)
                return result+bfs(next)
            else:
                return 0
    
        return bfs([self.root])


    def __str__(self):
        '''gives an ugly vizualization of the tree, example:
        0|
        1-2|
        3|4-5|
        means nodes 1 and 2 are both children of 0, 3 is the child of 1
        and 4 and 5 are children of 2
        
        Returns:
            representation (str)'''
        
        def represent(list_of_lists):
            '''aux function that use BFS to print all nodes on a level and calls itself on the next one.
            Parameters:
                list_of_lists ( (Node objects list) list) 
            Returns:
                sub_representation (str)'''

            if any(list_of_lists):  # if the level is not empty
                next = []
                result = ''
                for group in list_of_lists:  # a group is a list of children of a specific node
                    if any(group):  # to check if there is any children left
                        level = []
                        for node in group:
                            if node.value != '':
                                level.append(str(node.value))
                            else:
                                level.append(str("Ø"))
                            next += [node.children]
                        # children of the same node are separated by '-'
                        result += "-".join(level)
                    result += "|"  # separates children of two differents nodes
                result += "\n"
                # to go from the actual level to the next one
                return result+represent(next)

            else:  # checks if the level is empty to end recursion
                return ''

        return represent([[self.root]])