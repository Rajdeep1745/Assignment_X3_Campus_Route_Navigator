from search import RouteSearch

class RoutingAgent:
    def __init__(self, name, strategy, campus):
        self.name = name
        self.strategy = strategy
        self.searcher = RouteSearch(campus)

    def navigate(self, start, goal):
        return self.searcher.run(start, goal, self.strategy)

class Pathfinder(RoutingAgent):
    def __init__(self, campus):
        super().__init__("PATHFINDER", "greedy", campus)

class Orbit(RoutingAgent):
    def __init__(self, campus):
        super().__init__("ORBIT", "astar", campus)
