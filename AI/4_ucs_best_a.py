
## My handwritten code:

import math 
import heapq


class Node:
    def __init__(self, val, huristics=0):
        self.val = val 
        self.neighbours = []
        self.huristics = huristics
        
        

def take_input():
    
    # node + huristics:
    nodes = {}
    print("Enter node and huristics: (write done after finished)")
    while True:
        data = input().split()
        
        if data[0] == "done":
            break
        if len(data) != 2:
            print("invalid input")
            continue  # Use continue instead of break
        
        val, huris = int(data[0]), int(data[1])
        nodes[val] = Node(val, huris)
        
    
    # node1,node2,cost:
    print("Enter node1, node2, cost")
    while True:
        data = input().split()
        if data[0] == "done":
            break
        if len(data) != 3:
            print("invalid value")
            continue  # Use continue instead of break
        
        u, v, w = int(data[0]), int(data[1]), int(data[2])
        if u not in nodes:
            nodes[u] = Node(u, 0)
        if v not in nodes:
            nodes[v] = Node(v, 0)
            
        nodes[u].neighbours.append((nodes[v], w))
        
    # start, target:
    start = int(input("start node: "))
    target = int(input("target node: "))
    
    if start not in nodes or target not in nodes:
        print("start or target node is invalid")
        return None, None, None
    
    return nodes[start], nodes[target], nodes


#UCS
def UCS(start,target):
    if not start or not target:
        return None
    
    # queue: cost,node,edge:
    queue = [(0,start,[start.val])]
    visited = set()
    costs = {start:0}
    
    while queue:
        cost,node,path = heapq.heappop(queue)
        if node==target:
            return cost,path
        if node in visited:
            continue
        visited.add(node)
        
        for neighbor,weight in node.neighbours:
            if neighbor not in visited:
                new_cost = cost+weight
                new_path = path + [neighbor.val]
                
                if neighbor not in costs or new_cost<cost[neighbor]:
                    heapq.heappush(queue,(new_cost,neighbor,new_path))
    return None


#Best First Search:
def bestFirstSearch(start,target):
    
    if not start or not target:
        return None 
    
    # huristics,node,path
    queue = [(start.huristics,start,[start.val])] 
    visited = set()
    
    while queue:
        _,node,path = heapq.heappop(queue)
        if node==target:
            return path 
        if node in visited:
            continue
        visited.add(node)
        for neighbour,weight in node.neighbours:
            if neighbour is not visited:
                new_path = path + [neighbour.val]
                heapq.heappush(queue, (neighbour.huristics, neighbour, new_path))

    return None 



# A* algorithrm:
def a_start(start,target):
    """A* algorithrm"""
    if not start or not target:
        return None
    
    #f_cost,node,path,g_cost
    # f(n)  = h(n) + g(n)
    queue = [(start.huristics,start,[start.val],0)]
    visited = set()
    costs = {start:0}
    
    while queue:
        f_cost,node,path,g_cost = heapq.heappop(queue)
        
        if node==target:
            return path,g_cost
        
        if node in visited:
            continue
        
        visited.add(node)

        for neighbour,weight in node.neighbours:
            new_g_cost = g_cost + weight
            new_path = path + [neighbour.val]
            new_f_cost = new_g_cost + neighbour.huristics 
            if neighbour not in costs or new_g_cost<cost[neighbour]:
                costs[neighbour] = new_g_cost
                heapq.heappush(queue,(new_f_cost,neighbour,new_path,new_g_cost))
    return None 
#<---------------------Test all the algorithrm--------------------->
""" 
Enter node and huristics: (write done after finished)
1 5
2 3
3 2
4 0
done
Enter node1, node2, cost
1 2 4
1 3 2
2 4 5
3 4 1
done
start node: 1
target node: 4

Output: 
    Path: [1, 3, 4]
    Total Cost: 3 (2 + 1)
"""
start_node, target_node, all_nodes = take_input()
if start_node and target_node:
    cost, path = UCS(start_node, target_node)
    if path:
        print(f"UCS Path: {path}")
        print(f"Total Cost: {cost}")
    else:
        print("No path found")
        
        
if start_node and target_node:
    path = bestFirstSearch(start_node,target_node)
    if path:
        print("best first searh path: {}".format(path))
    else:
        print("Target is not found")


if start_node and target_node:
    path = a_start(start_node,target_node)
    if path:
        print("A* Search-> ",path)
    else:
        print("target is not found")
        
    