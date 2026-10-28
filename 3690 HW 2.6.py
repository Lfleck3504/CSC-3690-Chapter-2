graph = {
    "A": ["B", "C", "U"],
    "B": ["E", "G"],
    "C": ["G", "I", "J"],
    "U": ["K", "Y"],
    "E": ["G", "M"],
    "G": ["M"],
    "I": ["M"],
    "J": ["K"],
    "K": ["J"],
    "Y": ["M"],
    "M": []
}
heuristic = {
    "A": 7,
    "B": 5,
    "C": 3,
    "U": 4,
    "E": 2,
    "G": 3,
    "I": 6,
    "J": 4,  # change 2 to 4 to prevent the local minimum found before (causes new local minimum)
    "K": 1,
    "Y": 2,
    "M": 0
}
def hillClimbing(start, goal):
    current = start
    path = [current]
    while current != goal:
        neighbors = graph[current]
        if not neighbors:
            break
        nextNode = min(neighbors, key=lambda node: heuristic[node])
        if heuristic[nextNode] >= heuristic[current]:
            break
        current = nextNode
        path.append(current)

    print("Path:", " -> ".join(path))

    if current == goal:
        print("Goal located")
    else:
        print("Trapped in local minimum:", current)


hillClimbing("A", "M")