# ai-eval-tasks

Three small, original coding tasks for evaluating AI agents, written in the styles of
**Terminal-Bench**, **Harbor**, and **SWE-bench**. Each task includes an instruction, an environment,
a reference solution, and tests/a verifier. This is a personal portfolio project, not work for a company,
and it is not affiliated with those benchmarks.

## Tasks

| Style | Task | What the agent must do | How correctness is checked |
|---|---|---|---|
| Terminal-Bench | `terminal-bench/top-ips` | Find the top 3 IPs by *successful* (2xx) requests in an access log and write them to a file | pytest recomputes the expected result from the log and compares; a SHA-256 check ensures the log wasn't modified |
| Harbor | `harbor/wordstat-fix` | Fix a buggy Python CLI (case folding, punctuation, apostrophes, tie-break order, `--top` off-by-one, missing-file exit code) | Pytest suite runs the CLI on freshly generated inputs; the verifier writes reward `1`/`0` |
| SWE-bench style | `swebench-style/slugger` | Resolve an issue in a tiny repo (`slugify` leaves repeated and trailing hyphens) by producing a patch | `FAIL_TO_PASS` tests must pass and `PASS_TO_PASS` tests must still pass |

## Repository layout

```
terminal-bench/top-ips/      task.yaml, Dockerfile, docker-compose.yaml, solution.sh, run-tests.sh, tests/
harbor/wordstat-fix/         task.toml, instruction.md, environment/, solution/, tests/
swebench-style/slugger/      base/ (buggy snapshot), instance.json, gold.patch, test.patch, run_eval.py
```

## Design notes

- **Tests are hidden from the agent at run time.** They are copied into the environment only at
  verification time. They are published here for portfolio purposes; a real benchmark would keep them private.
- **Anti-gaming:** the Terminal-Bench log is constructed so a naive `sort | uniq -c` gives the wrong
  order, and the input log is hash-checked. The Harbor tests generate their own inputs, so hardcoding
  the sample output fails.
- **Validation:**
  - Terminal-Bench and Harbor: the unsolved environment fails the tests and the reference solution passes.
    For Terminal-Bench, a plausible naive attempt and a tampered log also fail.
  - SWE-bench style: `run_eval.py --validate` confirms the `FAIL_TO_PASS` tests fail on the base snapshot,
    pass with the gold patch, and that the `PASS_TO_PASS` tests pass in both cases.

## Running the SWE-bench-style task

Requires Python 3, `git`, and `pytest`.

```bash
cd swebench-style/slugger
python run_eval.py --validate
python run_eval.py --model-patch gold.patch
```

The Terminal-Bench and Harbor tasks are intended to run through their respective harnesses;
`solution.sh` and `solution/solve.sh` are the reference solutions.

## Status

- Task logic and tests are verified by running each reference solution against its tests in a simulated
  `/app` environment.
- Not yet run inside Docker or the official Terminal-Bench/Harbor harnesses, so harness-specific details
  (base image, compose variables, config fields) may need adjusting for current versions.
- `swebench-style` is a simplified local imitation of the SWE-bench format, not the official harness.
