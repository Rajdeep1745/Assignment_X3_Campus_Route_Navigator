import json
from pathlib import Path

class CampusMap:
    def __init__(self, file_path="campus.json"):
        with open(file_path, "r", encoding="utf-8") as source:
            data = json.load(source)
        self.locations = data["locations"]
        self.adjacency = {place: {} for place in self.locations}
        for first, second, cost in data["edges"]:
            self.adjacency[first][second] = cost
            self.adjacency[second][first] = cost
        self.cse_zone = {
            "CSE Laboratory", "CSE_AKC Seminar Hall", "CSE_Reflxon Room"
        }
        self.tower_entries = {"Tower 2 Front Entry", "Tower 2 Rear Entry"}

    def neighbors(self, place):
        return self.adjacency[place].items()

    def distance(self, first, second):
        return self.adjacency[first][second]

    def heuristic(self, place, goal):
        return self.coordinates_distance(place, goal)

    def coordinates_distance(self, place, goal):
        return self._landmark_distance(place, goal)

    def _landmark_distance(self, place, goal):
        # Consistent map-based estimate derived from the supplied graph.
        # It is a lower-bound graph distance, computed without a pathfinding package.
        distances = {node: float("inf") for node in self.locations}
        distances[goal] = 0
        pending = set(self.locations)
        while pending:
            current = min(pending, key=lambda node: distances[node])
            pending.remove(current)
            if distances[current] == float("inf") or current == place:
                break
            for nxt, weight in self.neighbors(current):
                candidate = distances[current] + weight
                if candidate < distances[nxt]:
                    distances[nxt] = candidate
        return distances[place]

    def allowed_neighbors(self, node, previous, phase, goal):
        for nxt, cost in self.neighbors(node):
            if goal in self.cse_zone:
                if phase == "cse-entry":
                    if nxt in self.cse_zone:
                        yield nxt, cost, "cse"
                    continue
                if phase == "cse":
                    if nxt in self.cse_zone:
                        yield nxt, cost, "cse"
                    elif nxt == "Lift Area":
                        yield nxt, cost, "cse-exit"
                    continue
                if nxt in self.cse_zone:
                    if node == "Lift Area" and previous in self.tower_entries:
                        yield nxt, cost, "cse"
                    continue
                if node in self.tower_entries and nxt == "Lift Area":
                    yield nxt, cost, "cse-entry"
                else:
                    yield nxt, cost, "outside"
            elif phase == "cse":
                if nxt in self.cse_zone:
                    yield nxt, cost, "cse"
                elif nxt == "Lift Area":
                    yield nxt, cost, "cse-exit"
            elif phase == "cse-exit":
                if nxt in self.tower_entries:
                    yield nxt, cost, "outside"
            else:
                if nxt in self.cse_zone:
                    continue
                if node in self.tower_entries and nxt == "Lift Area":
                    yield nxt, cost, "cse-exit"
                else:
                    yield nxt, cost, "outside"

    def initial_phase(self, start, goal):
        if start in self.cse_zone:
            return "cse"
        return "outside"
