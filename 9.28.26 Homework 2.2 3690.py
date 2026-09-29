from collections import deque


def bfs(start, goal):
    queue = deque([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()

        print("Visiting:", current)

        if current == goal:
            print("Goal found:", goal)
            break

        left_child = 2 * current
        right_child = 2 * current + 1

        queue.append(left_child)
        queue.append(right_child)

        parent[left_child] = current
        parent[right_child] = current

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse() #added later because the tab auto did this line and i forgot why, its to put the list back in the right order to display
    return path


start = 1
goal = 11

path = bfs(start, goal)

print("\nPath from start to goal:")
print(" -> ".join(map(str, path)))