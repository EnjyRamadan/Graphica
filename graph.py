def make_edge_both_ways(edges):
    duplicated_edges = [(a, b) for a, b in edges]
    duplicated_edges.extend([(b, a) for a, b in edges])
    edges = duplicated_edges.copy()
    return edges


def reverse_and_copy(original_dict):
    reversed_dict = {(b, a): value for (a, b), value in original_dict.items()}
    copied_dict = original_dict.copy()
    original_dict.update(reversed_dict)
    return original_dict, copied_dict


class Graph:
    def __init__(self, edges, costs, heuristic, goals):
        self.graph_dict = {}
        self.heuristic_dict = {}
        self.edges = make_edge_both_ways(edges)
        self.costs = reverse_and_copy(costs)
        self.goals = goals
        for start, end in self.edges:
            if start not in self.graph_dict:
                self.graph_dict[start] = [end]
            else:
                self.graph_dict[start].append(end)
        for node, value in heuristic.items():
            self.heuristic_dict[node] = value

    def check_goal(self, node):
        return True if node in self.goals else False

    @staticmethod
    def expand_decorator(func):
        def wrapper(self, node, path):
            func(self, node, path)
            neighbors = self.graph_dict.get(str(node), [])
            new_path = [path + [element] for element in neighbors]
            return new_path

        return wrapper

    @staticmethod
    def expand_heuristic_decorator(func):
        def wrapper(self, node, path):
            neighbours = self.graph_dict.get(str(node), [])
            if func.__name__ == "expand_astar":
                new_path = [
                    (
                        self.heuristic_dict[element]
                        + self.path_cost(path)
                        + self.costs.get((node, element)),
                        [i for i in path] + [element],
                    )
                    for element in neighbours
                ]
            else:
                new_path = [
                    (self.heuristic_dict[element], [i for i in path] + [element])
                    for element in neighbours
                ]
            return new_path

        return wrapper

    @expand_decorator
    def expand_bfs(self, node, path):
        pass

    def bfs(self, fringe, visited, sortedVisit):
        if fringe:
            path = fringe.popleft()
            node = path[-1]
            if self.check_goal(node):
                return path
            else:
                if node not in visited:
                    sortedVisit.append(node)
                    visited.add(node)
                    fringe.extend(self.expand_bfs(node, path))
        return False

    @expand_decorator
    def expand_dfs(self, node, path):
        pass

    def dfs(self, fringe, visited, sortedVisit):
        if fringe:
            path = fringe.pop()
            node = path[-1]
            if self.check_goal(node):
                return path
            else:
                if node not in visited:
                    sortedVisit.append(node)
                    visited.add(node)
                    fringe.extend(self.expand_dfs(node, path))
        return False

    @expand_heuristic_decorator
    def expand_greedy(self, node, path):
        pass

    def greedy(self, fringe, visited, sortedVisit):
        path = []
        if fringe:
            h, node = min(fringe)
            fringe.remove((h, node))
            path = node
            node = node[-1]
            if self.check_goal(node):
                return path
            else:
                if node not in visited:
                    sortedVisit.append(node)
                    visited.add(node)
                    fringe.extend(self.expand_greedy(node, path))
        return False

    @expand_heuristic_decorator
    def expand_astar(self, node, path):
        pass

    def astar(self, fringe, visited, sortedVisit):
        path = []
        if fringe:
            h, node = min(fringe)
            fringe.remove((h, node))
            path = node
            node = node[-1]
            if self.check_goal(node):
                return path
            else:
                if node not in visited:
                    sortedVisit.append(node)
                    visited.add(node)
                    fringe.extend(self.expand_astar(node, path))
        return False

    def path_cost(self, path):
        return sum(
            self.costs.get((path[i], path[i + 1]), 1) for i in range(len(path) - 1)
        )

    def ucs(self, fringe, visited, sortedVisit):
        if fringe:
            cost, node, path = min(fringe, key=lambda x: x[0])
            fringe.remove((cost, node, path))
            if self.check_goal(node):
                return path + [node]
            else:
                if node not in visited:
                    sortedVisit.append(node)
                    visited.add(node)
                    for neighbor in self.graph_dict.get(node, []):
                        edge = (node, neighbor)
                        new_cost = cost + self.costs.get(edge, 1)
                        new_path = path + [node]
                        fringe.append((new_cost, neighbor, new_path))
        return False
