# ai-eval-tasks

Three small, self-authored coding tasks for evaluating AI agents, written in the styles of
**Terminal-Bench**, **Harbor**, and **SWE-bench**. Each task has an instruction, an environment,
a reference solution, and hidden tests/verifier. This is self-directed practice, not work for a company.

| Style | Task | What the agent must do | How correctness is checked |
|---|---|---|---|
| Terminal-Bench | `terminal-bench/top-ips` | Find the top 3 IPs by *successful* (2xx) requests in a log and write them to a file | pytest compares the output file to values recomputed from the log; also checks the log wasn't modified (SHA-256) |
| Harbor | `harbor/wordstat-fix` | Fix a buggy Python CLI (case, punctuation, apostrophes, tie-break order, `--top` off-by-one, missing-file exit code) | Hidden pytest suite runs the CLI on freshly written inputs; verifier writes reward `1`/`0` |
| SWE-bench style | `swebench-style/slugger` | Resolve an issue in a tiny repo (`slugify` leaves repeated/trailing hyphens) by producing a patch | `FAIL_TO_PASS` tests must pass and `PASS_TO_PASS` tests must still pass |

## Design choices

- **Hidden tests are not in the agent's environment.** They are copied in only at verification time.
- **Anti-gaming:** the Terminal-Bench log is built so naive `sort | uniq -c` gives the wrong order, and
  the input log is hash-checked. The Harbor tests write their own inputs, so hardcoding the sample output fails.
- **Task validity checks:** each task was checked three ways: unsolved fails, reference solution passes,
  and (for TB) a plausible wrong attempt fails.
- **SWE-bench style:** `run_eval.py --validate` confirms the F2P tests fail on the base snapshot and pass
  with the gold patch, and that the P2P tests pass in both cases.

## Running

```bash
# SWE-bench style (needs only python + pytest)
cd swebench-style/slugger
python run_eval.py --validate
python run_eval.py --model-patch gold.patch
```

The Terminal-Bench and Harbor tasks are meant to run through their harnesses (`tb run` / `harbor run`).
`solution.sh` / `solution/solve.sh` are the reference solutions the harness uses to confirm solvability.

## Status / caveats

- The task logic and tests were verified by running each task's reference solution against its tests
  in a simulated `/app` environment, but **not inside Docker or the official harnesses**.
- Task file layouts (`task.yaml` + `docker-compose.yaml` for Terminal-Bench, `task.toml` +
  `environment/` + `solution/` + `tests/` for Harbor) follow the formats as I know them and may need small
  tweaks (e.g. base image name, compose env vars) to match the current harness versions.
- `swebench-style` is a simplified local imitation of the SWE-bench format, not the official harness.
