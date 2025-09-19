class Node:
    def __init__(self, val):
        self.val = val 
        self.neighbours = []
        
    
def create_graph():
    print("Enter the node value separated with space like: 30 20 30 :")
    node_values = list(map(int, input().split()))
    nodes = {value: Node(value) for value in node_values}
    
    # taking the value of edges:
    print("Enter the value of edges format(node1,node2), 0 0 finished")
    while True:
        u, v = map(int, input().split())
        if u == 0 and v == 0:
            break 
        if u not in nodes:
            nodes[u] = Node(u)
        if v not in nodes:
            nodes[v] = Node(v)
        
        nodes[u].neighbours.append(nodes[v])
    
    # select the starting node:
    start = int(input("Input the starting node: "))
    if start not in nodes:
        print("Wrong start")
        return None
    return nodes[start]


def BFS(root):
    if not root:
        print("Invalid root")
        return None 
    
    queue = [root]
    visited = set()
    results = []
    
    visited.add(root)
    results.append(root.val)
    
    while queue:
        node = queue.pop(0)
        for neighbour in node.neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                results.append(neighbour.val)
    return results


def DFS(root):
    if not root:
        print("Invalid root")
        return []
    
    stack = [root]
    visited = set()
    results = []
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            results.append(node.val)
            # Add neighbors in reverse order for proper DFS order
            for neighbour in reversed(node.neighbours):
                if neighbour not in visited:
                    stack.append(neighbour)
    
    return results


def DLS(root, depth_limit):
    """Depth-Limited Search within depth limit"""
    if not root:
        return []
    
    def dls_traverse(node, depth, visited, result):
        if depth > depth_limit or node in visited:
            return
        
        visited.add(node)
        result.append(node.val)
        
        for neighbour in node.neighbours:
            dls_traverse(neighbour, depth + 1, visited, result)
    
    visited = set()
    result = []
    dls_traverse(root, 0, visited, result)
    return result


def IDDFS(root, max_depth):
    """Iterative Deepening Depth-First Search without target"""
    if not root:
        return []
    
    full_result = []
    for depth in range(max_depth + 1):
        print(f"Depth limit: {depth}")
        result = DLS(root, depth)
        print(f"Nodes at depth {depth}: {result}")
        # If we found new nodes at this depth, add them to the full result
        for node_val in result:
            if node_val not in full_result:
                full_result.append(node_val)
    return full_result


# Test all algorithms
root = create_graph()
if root:
    dfs_result = DFS(root)
    bfs_result = BFS(root)
    
    print(f"DFS: {dfs_result}")
    print(f"BFS: {bfs_result}")
    
    # Test DLS
    depth_limit = int(input("Enter depth limit for DLS: "))
    dls_result = DLS(root, depth_limit)
    print(f"DLS (depth limit {depth_limit}): {dls_result}")
    
    # Test IDDFS
    max_depth = int(input("Enter maximum depth for IDDFS: "))
    iddfs_result = IDDFS(root, max_depth)
    print(f"IDDFS (max depth {max_depth}): {iddfs_result}")
    
    
    
