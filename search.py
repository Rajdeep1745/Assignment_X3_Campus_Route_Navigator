import heapq
import itertools
import time

class SearchResult:
    def __init__(self, path, cost, explored, elapsed, expanded):
        self.path = path
        self.cost = cost
        self.explored = explored
        self.elapsed = elapsed
        self.expanded = expanded

class RouteSearch:
    def __init__(self, campus):
        self.campus = campus

    def run(self, start, goal, strategy):
        if start not in self.campus.locations or goal not in self.campus.locations:
            raise ValueError("Choose locations listed in campus.json.")
        if start == goal:
            return SearchResult([start], 0, 0, 0.0, 0)
        started = time.perf_counter()
        sequence = itertools.count()
        phase = self.campus.initial_phase(start, goal)
        start_state = (start, "", phase)
        frontier = [(self._priority(0, self.campus.heuristic(start, goal), strategy),
                     next(sequence), 0, start_state, [start])]
        best = {start_state: 0}
        explored = 0
        expanded = 0
        while frontier:
            _, _, travelled, state, path = heapq.heappop(frontier)
            node, previous, phase = state
            if travelled != best.get(state):
                continue
            explored += 1
            if node == goal:
                return SearchResult(path, travelled, explored,
                                    time.perf_counter() - started, expanded)
            expanded += 1
            for nxt, weight, next_phase in self.campus.allowed_neighbors(
                    node, previous, phase, goal):
                next_cost = travelled + weight
                next_state = (nxt, node, next_phase)
                if next_cost >= best.get(next_state, float("inf")):
                    continue
                best[next_state] = next_cost
                heuristic = self.campus.heuristic(nxt, goal)
                priority = self._priority(next_cost, heuristic, strategy)
                heapq.heappush(frontier, (priority, next(sequence), next_cost,
                                          next_state, path + [nxt]))
        return SearchResult([], float("inf"), explored,
                            time.perf_counter() - started, expanded)

    @staticmethod
    def _priority(cost, heuristic, strategy):
        return heuristic if strategy == "greedy" else cost + heuristic
