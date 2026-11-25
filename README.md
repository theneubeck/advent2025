# Advent of Code 2025

My solutions to [Advent of Code 2025](https://adventofcode.com/2025), written just for fun.

They aren't meant to be optimal, clever or production-ready. Some days have more than one version, because I tried a different approach.

## Layout

Each day is its own package:

```
dayN/
  solution.py       # main(data, version=...) plus helpers
  test_solution.py  # pytest tests, mostly built from the puzzle examples
  input.txt         # your puzzle input (not committed)
```

Puzzle inputs aren't committed. Put your own in `dayN/input.txt`.

## Running a day

Each day reads its own `input.txt` and prints the answer:

```sh
uv run python day4/solution.py    # run the file directly
uv run python -m day4.solution    # run it as a module
uv run day4                       # script entry from pyproject.toml
```

For `uv run day4` to work, the day needs a line under `[project.scripts]` in `pyproject.toml` and must be listed in `packages` under `[tool.hatch.build.targets.wheel]`. You may need to run `uv sync` after adding it.

This uses that day's default version (part 1 or part 2), which varies between days. To run the other part, change the default `version` in that day's `main`.

## Tests

```sh
uv run pytest                      # everything
uv run pytest day4                 # one day
uv run pytest day4 -k test_main_v2 # one test function
uv run pytest day4 -v              # list each case by its id
```

## Formatting and linting

[Ruff](https://docs.astral.sh/ruff/) handles both (Black-compatible formatting, PEP 8 checks, import sorting). In VS Code it runs on save via the Ruff extension (see `.vscode/`). From the terminal:

```sh
uv run ruff format .       # format
uv run ruff check . --fix  # lint and auto-fix
```
