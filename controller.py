from graph import Graph
from collections import deque as queue

edges = [
    ("Node 6", "Node 4"),
    ("Node 2", "Node 6"),
    ("Node 5", "Node 3"),
    ("Node 5", "Node 1"),
    ("Node 3", "Node 4"),
    ("Node 2", "Node 1"),
]
costs = {
    ("Node 6", "Node 4"): "1",
    ("Node 2", "Node 6"): "1",
    ("Node 5", "Node 3"): "1",
    ("Node 5", "Node 1"): "1",
    ("Node 3", "Node 4"): "1",
    ("Node 2", "Node 1"): "1",
}

heuristic = {"Node 1": 1, "Node 2": 1, "Node 3": 1, "Node 4": 1, "Node 5": 1, "Node 6": 1}


def calling_function(edge, cost, heuristic, strategy, start, goal):
    g = Graph(edge, cost, heuristic, goal)
    match strategy:
        case "UCS":
            visited, fringe, sortedVisit = set(), [(0, start, [])], []
            while fringe:
                ans = g.ucs(fringe, visited, sortedVisit)
                if ans:
                    break
            if ans:
                return ans, sortedVisit
            return None
        case "BFS":
            visited, fringe, sortedVisit = set(), queue([[start]]), []
            while fringe:
                ans = g.bfs(fringe, visited, sortedVisit)
                if ans:
                    break
            if ans:
                return ans, sortedVisit
            return ans
        case "DFS":
            visited, fringe, sortedVisit = set(), list([[start]]), []
            while fringe:
                ans = g.dfs(fringe, visited, sortedVisit)
                print(visited)
                if ans:
                    break
            if ans:
                return ans, sortedVisit
            return ans
        case "Greedy":
            visited, fringe, sortedVisit = set(), [], []
            fringe.append((g.heuristic_dict[start], start))
            while fringe:
                ans = g.greedy(fringe, visited, sortedVisit)
                if ans:
                    break
            if ans:
                return ans, sortedVisit
            return None
        case "A*":
            visited, fringe, sortedVisit = set(), [], []
            fringe.append((g.heuristic_dict[start] + 0, start))
            while fringe:
                ans = g.astar(fringe, visited, sortedVisit)
                if ans:
                    break
            if ans:
                return ans, sortedVisit
            return None


print(calling_function(edges, costs, heuristic, "BFS", "Node 1", "Node 4"))
