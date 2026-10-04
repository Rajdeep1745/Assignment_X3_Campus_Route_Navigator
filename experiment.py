import csv
from pathlib import Path

ROUTE_PAIRS = [
    ("Reception", "Library"),
    ("Canteen", "New Building 2"),
    ("Entry Gate 1", "CSE Laboratory"),
    ("Auditorium Hall", "CSE_AKC Seminar Hall"),
    ("Library", "Canteen"),
    ("CSE_Reflxon Room", "Entry Gate 2"),
    ("Parking Area", "New Building 1"),
    ("Entry Gate 2", "CSE_AKC Seminar Hall")
]

def run_experiments(campus, agents, output="results/results.csv"):
    rows = []
    for start, goal in ROUTE_PAIRS:
        for agent in agents:
            result = agent.navigate(start, goal)
            rows.append({
                "start": start, "destination": goal, "agent": agent.name,
                "path": " -> ".join(result.path) if result.path else "No route",
                "cost_m": result.cost, "nodes_explored": result.explored,
                "execution_seconds": f"{result.elapsed:.8f}"
            })
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows
