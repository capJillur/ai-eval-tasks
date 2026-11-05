#!/usr/bin/env python3
"""Tiny SWE-bench-style evaluator.

  python run_eval.py --validate                 # sanity-check the instance itself
  python run_eval.py --model-patch my_fix.patch # grade a candidate patch

Resolved = every FAIL_TO_PASS test passes AND every PASS_TO_PASS test still passes.
The test patch is applied AFTER the model patch, so the model never sees the new tests
and cannot overwrite them.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent.resolve()
GIT = ["git", "-c", "user.name=eval", "-c", "user.email=eval@example.com"]


def sh(cmd, cwd, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)}\n{r.stdout}\n{r.stderr}")
    return r


def fresh_repo(tmp):
    repo = Path(tmp) / "repo"
    shutil.copytree(HERE / "base", repo)
    sh(["git", "init", "-q"], repo)
    sh(["git", "add", "-A"], repo)
    sh(GIT + ["commit", "-q", "-m", "base"], repo)
    return repo


def apply_patch(repo, patch_file):
    sh(["git", "apply", "--whitespace=nowarn", str(Path(patch_file).resolve())], repo)


def run_tests(repo, test_ids):
    r = sh([sys.executable, "-m", "pytest", "-q", "-rA", "-p", "no:cacheprovider", *test_ids],
           repo, check=False)
    status = {}
    for line in r.stdout.splitlines():
        for word in ("PASSED", "FAILED", "ERROR"):
            if line.startswith(word + " "):
                status[line.split()[1]] = (word == "PASSED")
    return {t: status.get(t, False) for t in test_ids}


def evaluate(inst, model_patch=None):
    with tempfile.TemporaryDirectory() as tmp:
        repo = fresh_repo(tmp)
        if model_patch and Path(model_patch).read_text().strip():
            apply_patch(repo, model_patch)
        apply_patch(repo, HERE / inst["test_patch"])
        f2p = run_tests(repo, inst["FAIL_TO_PASS"])
        p2p = run_tests(repo, inst["PASS_TO_PASS"])
    return f2p, p2p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", default=str(HERE / "instance.json"))
    ap.add_argument("--model-patch")
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()
    inst = json.loads(Path(args.instance).read_text())

    if args.validate:
        f2p, p2p = evaluate(inst, model_patch=None)
        ok1 = not any(f2p.values()) and all(p2p.values())
        print(f"[base + tests]  F2P all fail: {not any(f2p.values())}  P2P all pass: {all(p2p.values())}")
        f2p, p2p = evaluate(inst, model_patch=HERE / inst["patch"])
        ok2 = all(f2p.values()) and all(p2p.values())
        print(f"[gold + tests]  F2P all pass: {all(f2p.values())}  P2P all pass: {all(p2p.values())}")
        print("VALID" if ok1 and ok2 else "INVALID")
        sys.exit(0 if ok1 and ok2 else 1)

    if not args.model_patch:
        ap.error("--model-patch or --validate required")
    f2p, p2p = evaluate(inst, args.model_patch)
    resolved = all(f2p.values()) and all(p2p.values())
    print(json.dumps({"FAIL_TO_PASS": f2p, "PASS_TO_PASS": p2p, "resolved": resolved}, indent=2))
    sys.exit(0 if resolved else 1)


if __name__ == "__main__":
    main()
