import hashlib
import re
from pathlib import Path

LOG = Path("/app/access.log")
OUT = Path("/app/top_ips.txt")
LOG_SHA256 = "78a20b3349898091622271e269c57fdf6fc5563de3b4bb51b01ba75eee436486"  # guards against the agent editing the input


def expected_top3():
    counts = {}
    for raw in LOG.read_text().splitlines():
        m = re.match(r'^(\S+) .*" (\d{3}) \d+$', raw)
        if not m:
            continue
        ip, status = m.groups()
        if 200 <= int(status) <= 299:
            counts[ip] = counts.get(ip, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:3]


def test_log_unmodified():
    assert hashlib.sha256(LOG.read_bytes()).hexdigest() == LOG_SHA256


def test_output_exists():
    assert OUT.exists(), "/app/top_ips.txt was not created"


def test_format_and_line_count():
    lines = OUT.read_text().strip().splitlines()
    assert len(lines) == 3
    for ln in lines:
        assert re.fullmatch(r"\d+\.\d+\.\d+\.\d+ \d+", ln), f"bad line: {ln!r}"


def test_correct_ips_counts_and_order():
    got = [(l.split()[0], int(l.split()[1])) for l in OUT.read_text().strip().splitlines()]
    assert got == expected_top3()
