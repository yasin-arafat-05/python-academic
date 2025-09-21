

class Node:
    def __init__(self,val):
        self.val = val 
        self.neighbours = []
        


def take_input():
    print("give the node value: (node1,node2,node3...)")
    node_values = list(map(int,input().split()))
    nodes = {val:Node(val) for val in node_values}
    
    print("gime us edge value if finished type 0 0 : ")
    
    while True:
        u,v = map(int,input().split())
        if u==0 and v==0:
            break
        if u not in nodes:
            nodes[u] = Node(u)
        if v not in nodes:
            nodes[v] = Node(v)
            
        nodes[u].neighbours.append(nodes[v])
        
    start = int(input("Enter the start node: "))
    
    if start not in nodes:
        print("invalid starting node")
        return 
    return nodes[start]


# BFS:
def BFS(root):
    if not root:
        print("invalid root")
        return None
    
    queue = [root]
    visited = set()
    results = [root.val]
    
    visited.add(root)
    
    while queue:
        node = queue.pop(0)
        for neighbour in node.neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                results.append(neighbour.val)
                queue.append(neighbour)
                
    return results


#DFS 
def DFS(root):
    if not root:
        print("invalid root")
        return None
    
    stack = []
    visited =  set()
    results = []
    
    stack.append(root)
    while stack:
        node = stack.pop()
        
        # remember: reversed korar age value add kora lagbe:
        if node is not visited:
            visited.add(node)
            results.append(node.val)
            for neighbour in reversed(node.neighbours):
                stack.append(neighbour)
    return results


# DLS:
def DLS(root,limit_depth):
    if not root:
        print("root is not correct")
        return 
    
    def depth_limited(depth,visited,node,result):
        if depth>limit_depth:
            return 
        
        if node is visited:
            return 
        
        visited.add(node)
        result.append(node.val)
        
        for neighbour in node.neighbours:
            depth_limited(depth+1,visited,neighbour,result)
            
        
    visited = set()
    result = []
    depth_limited(0,visited,root,result)
    return result


def IDDFS(root,max_limit):
    for i in range(max_limit+1):
        print("*"*20)
        print("limit: {}".format(i))
        result = DLS(root,i)
        print("Results: {}".format(result))
        
    
# expamle:
# 10 15 100 20 25 30
""" 
10 15 
10 100
15 20
15 25 
20 30 
0 0 
"""
root = take_input()
bfs = BFS(root)
print("bfs: ",bfs)

dfs = DFS(root)
print("dfs: ", dfs)


dls = DLS(root,2)
print("DLS : ",dls)

idds = IDDFS(root,3)

