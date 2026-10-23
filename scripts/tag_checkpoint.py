"""Create only the requested DEV2-001 draft tag, after verified main-branch CI.

No model calls, release publication, tag replacement or experiment freeze.
Local `--check` validates the checkpoint without any network request.
"""
import argparse
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = "dev2-001-v0.2-draft"
REPOSITORY = "enuminous/Devs2.0"


def check():
    bench = ROOT / "research/dev2-001"
    config = json.loads((bench / "CONFIG.json").read_text())
    thresholds = json.loads((bench / "THRESHOLDS.json").read_text())
    if config["status"] != "DRAFT_NOT_FROZEN" or thresholds["status"] != "DRAFT_NOT_FROZEN":
        raise ValueError("This tag is only for the unfrozen draft checkpoint")
    if config["stage_context_policy"] != "full_prior_outputs_v1":
        raise ValueError("Checkpoint context policy differs")
    if config["budget"]["total_tokens"] != 8192 or config["budget"]["generated_tokens"] != 1024:
        raise ValueError("Checkpoint common budgets differ")
    if config["budget"]["token_ratio_denominator"] != "observed_A_total_tokens_same_complete_roster":
        raise ValueError("Checkpoint denominator differs")
    if config["arms"]["A"] != [{"name": "answer", "prompt": "A-plain.txt", "output_cap": 1024}]:
        raise ValueError("Checkpoint Arm A differs")
    if thresholds["replication_effect_tolerance"] != .12 or thresholds["pass_absolute_improvement"] != .20:
        raise ValueError("Checkpoint thresholds differ")


def publish():
    check()
    if (os.environ.get("GITHUB_REPOSITORY") != REPOSITORY
            or os.environ.get("GITHUB_REF") != "refs/heads/main"
            or os.environ.get("GITHUB_EVENT_NAME") != "push"):
        raise ValueError("Tag publication requires the repository's main-branch push workflow")
    sha = os.environ["GITHUB_SHA"]
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    message = subprocess.check_output(["git", "log", "-1", "--format=%B"], cwd=ROOT, text=True)
    if not re.fullmatch(r"[0-9a-f]{40}", sha) or sha != head or f"[tag-{TAG}]" not in message:
        raise ValueError("Only the explicitly marked, checked-out workflow commit may be tagged")

    def api(path, payload=None):
        request = urllib.request.Request(
            f"https://api.github.com/repos/{REPOSITORY}/{path}",
            data=None if payload is None else json.dumps(payload).encode(),
            headers={"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
                     "Accept": "application/vnd.github+json", "Content-Type": "application/json",
                     "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "DEV2-001-draft-checkpoint"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)

    try:
        existing = api(f"git/ref/tags/{TAG}")
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise RuntimeError(f"Could not inspect tag (HTTP {exc.code})") from None
    else:
        if existing["object"]["type"] != "commit" or existing["object"]["sha"] != sha:
            raise ValueError("Tag already exists at another object; it will never be moved")
        print(f"Existing draft checkpoint {TAG} already identifies {sha}")
        return
    try:
        api("git/refs", {"ref": f"refs/tags/{TAG}", "sha": sha})
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Could not create draft tag (HTTP {exc.code}); no overwrite attempted") from None
    print(f"Created {TAG} at {sha}; DRAFT_NOT_FROZEN, no experimental result")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    if args.publish:
        publish()
    else:
        check()
        print(f"{TAG}: checkpoint settings valid; no network request or tag creation")
