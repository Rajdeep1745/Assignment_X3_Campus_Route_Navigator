import argparse
import textwrap

from campus_map import CampusMap
from agents import Pathfinder, Orbit
from experiment import run_experiments


def print_locations(locations):
    print("\nAvailable locations:")
    i=1
    for location in locations:
        print(f'{i}. {location}', end="\n")
        i = i + 1



def display(agent, start, goal):
    result = agent.navigate(start, goal)

    print(f"  {agent.name}")

    if result.path:
        print("Route          :", " -> ".join(result.path))
        print(f"Total cost     : {result.cost} m")
    else:
        print("Route          : No valid route found")
        print("Total cost     : N/A")

    print(f"Nodes explored : {result.explored}")
    print(f"Execution time : {result.elapsed:.6f} seconds")
    print("-" * 60)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="AI Campus Route Navigator"
    )
    parser.add_argument("--start", help="Starting location")
    parser.add_argument("--goal", help="Destination")
    parser.add_argument(
        "--experiment",
        action="store_true",
        help="Run predefined route comparisons and save CSV"
    )
    args = parser.parse_args()

    campus = CampusMap()
    agents = [Pathfinder(campus), Orbit(campus)]

    if args.experiment:
        rows = run_experiments(campus, agents)
        print("  CAMPUS ROUTE EXPERIMENT")
        print(f"Completed comparisons : {len(rows)}")
        print("Results saved to      : results/results.csv")
        print("-" * 60)
        print("Start -> Destination | Agent | Cost | Nodes explored")
        print("-" * 60)
        for row in rows:
            print(
                f'{row["start"]} -> {row["destination"]} | '
                f'{row["agent"]} | {row["cost_m"]} m | '
                f'{row["nodes_explored"]}'
            )
        return

    print("  AI CAMPUS ROUTE NAVIGATOR")
    print_locations(campus.locations)

    start = args.start or input("\nEnter starting location: ").strip()
    goal = args.goal or input("Enter destination: ").strip()

    if start not in campus.locations or goal not in campus.locations:
        print("\nInvalid location. Please use a name from the list above.")
        return

    print("\n" + "#" * 60)
    print(f"  Journey: {start} -> {goal}")
    print("#" * 60)

    for agent in agents:
        display(agent, start, goal)


if __name__ == "__main__":
    main()
