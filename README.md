# AI Campus Route Navigator — Assignment 03

An object-oriented campus route planner comparing **PATHFINDER** (Greedy Best-First Search) and **ORBIT** (A* Search).

## Requirements
- Python 3.9 or newer
- Standard library only; no external pathfinding package

## Run
From this directory:

```bash
python main.py
```

Enter a start and destination exactly as listed in `campus.json`, or run directly:

```bash
python main.py --start "Reception" --goal "Library"
```

Run all predefined comparisons and write the measurements to CSV:

```bash
python main.py --experiment
```

The generated table is saved to `results/results.csv`.

## Project layout
- `campus.json` — campus locations and approximate undirected walking costs, separate from search code
- `campus_map.py` — graph loading, heuristic calculation, and CSE-zone route-state rules
- `search.py` — priority-queue-based Greedy Best-First and A* implementations
- `agents.py` — PATHFINDER and ORBIT agent classes
- `experiment.py` — route test cases and CSV reporting
- `main.py` — command-line interaction and experiment entry point
- `REPORT.md` — brief implementation and observation report

## Graph assumptions
The assignment map is the source of the allowed location names. Edge connectivity and weights are approximate walking-cost estimates based on the visible campus layout, not surveyed measurements. They are editable in `campus.json`. No additional campus locations are introduced.

The CSE zone is limited to CSE Laboratory, CSE_AKC Seminar Hall, and CSE_Reflxon Room. For routes entering this zone from outside, the search state enforces a Tower 2 entry → Lift Area → CSE location sequence and prevents visiting non-CSE locations before returning to the Lift Area. For routes leaving the zone, the reverse sequence is enforced.

## Reproducibility
Execution time varies by machine and system load. Run `python main.py --experiment` to regenerate results on your system. The supplied CSV is a sample run, not a hard-coded route answer.
