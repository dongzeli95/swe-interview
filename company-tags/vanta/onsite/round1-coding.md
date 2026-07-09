# Round 1 — Practical Coding

Same "uniq" family as the phone screen. Reports suggest the followup may include reading from a file rather than a fixed literal in the source. Have your local Python dev loop rehearsed so you can pipe input in:

```bash
cat input.txt | python solution.py
# or
python solution.py < input.txt
# or
python solution.py input.txt   # if the interviewer wants argv
```

## What to warm up

- `sys.stdin.read()` / `sys.stdin.readlines()` / iterating `sys.stdin` line by line.
- `json.load(sys.stdin)` if the input is JSON.
- `csv.reader` if tabular.
- `argparse` — but for a 25-min problem, `sys.argv[1]` is fine.

## Likely follow-ups on top of the phone screen problems

- **Task Dependency variant:** input is a JSON blob `[{id, dependencies}]`. Parse, then run Q1/Q2.
- **Employee Training variant:** input is a CSV of `employee_id,group_id,start_day,training_days_required`. Parse, build the group tree, run aggregation.

## Practice loop

Take your phone-screen solutions and wrap them with:

```python
import json, sys
if __name__ == "__main__":
    data = json.load(sys.stdin)
    tasks = [Task(**t) for t in data["tasks"]]
    targets = data["targets"]
    print(dependencies_of_targets(tasks, targets))
```

Then feed them a JSON file and confirm output. That's the muscle memory you need.

## Common failure modes

- Reaching for `pandas` for a 20-line CSV. Overkill; `csv.reader` is enough.
- Not handling trailing newlines / BOM in the input.
- Forgetting that `input()` returns `str`, not `int`. `int(input())` when needed.
