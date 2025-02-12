from flask import Flask, redirect, url_for, render_template, jsonify, request
from flask_cors import CORS
from graph import Graph
from collections import deque as queue

app = Flask(__name__)
CORS(app)


def convert_edges_to_tuples(edges):
    return [(edge["from"], edge["to"]) for edge in edges]


def convert_edges_to_dict(edges):
    return {(edge["from"], edge["to"]): int(edge["label"]) for edge in edges}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/vis.html")
def graph():
    return render_template("vis.html")


@app.route("/about.html")
def about():
    return render_template("about.html")


@app.route("/call_function", methods=["POST"])
def call_function():
    data = request.get_json()
    edge = data.get("edge")
    edge = convert_edges_to_tuples(edge)
    cost = data.get("cost")
    cost = convert_edges_to_dict(cost)
    heuristic = data.get("heuristic")
    strategy = data.get("strategy")
    start = data.get("start")
    goal = data.get("goal")
    result, visited = calling_function(edge, cost, heuristic, strategy, start, goal)
    print(visited)
    return jsonify(result=result, visited=visited)


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


if __name__ == "__main__":
    app.run(debug=True)
