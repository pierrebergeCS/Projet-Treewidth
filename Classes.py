class Node:
    def __init__(self, index, value=''):
        self.index=index
        self.value=value #string
        self.parent=None
        self.children=[]#list of Node objects

    def __str__(self):
        string=''
        if self.parent is not None:
            string+=str(self.parent)+'\n|\n'
        string+=str((self.index))+'\n|\n'
        for child in self.children:
            string+=str(child.index)+' '
        return string

    def add_children(self,list_nodes):
        if self.children is None:
            self.children=list_nodes
        else:
            self.children.extend(list_nodes)

    def add_parent(self,node):
        self.parent=node

    def delete_edge(self,node):
        if node==self.parent:
            self.parent=None
        else:
            self.children.remove(node)
class Tree:
    def __init__(self,root,list_nodes):
        self.list=list_nodes
        self.root=root
        self.index_list=[node.index for node in self.list] 
        self.slot=max(self.index_list)+1
        self.width=max([len(node.value) for node in self.list])

    def add_edge(self,parent,child):
        parent.add_children([child])
        child.add_parent(parent)

    def add_node(self, node):
        node.index=self.slot
        self.slot+=1
        self.list.append(node)
        self.index_list.append(node.index)

    def delete_node(self,node):
        (node.parent).delete_edge(node)
        for child in node.children:
            child.delete_edge(node)
        self.list.remove(node)
        self.index_list.remove(node.index)

    def delete_edge(self,u,v):
        u.delete_edge(v)
        v.delete_edge(u)

    def __str__(self):
        def represent(t,list_of_lists,number):
            if not any(list_of_lists):
                return ''
            else:
                next=[]
                result=''
                for group in list_of_lists:
                    if any(group):
                        level=[]
                        for node in group:
                            node.index=number
                            number+=1
                            level.append(str(node.value))
                            next+=[node.children]
                        result+="-".join(level)
                    result+="|"
                result+="\n"
                return result+represent(t,next,number)

        return represent(self,[[self.root]],0)+"\n\n"+"   |||   ".join([str(node.index)+":"+str(node.value) for node in self.list])