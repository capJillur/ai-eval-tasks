"""Generate a deterministic access log.

Design note: the busiest IP by RAW request count (10.0.0.5) is NOT the busiest by
SUCCESSFUL request count, so `awk '{print $1}' | sort | uniq -c` gives the wrong order.
"""
import random
import sys

random.seed(1337)

# ip: (successful_requests, failed_requests)
PROFILE = {
    "10.0.0.5": (60, 90),
    "192.168.1.20": (90, 10),
    "172.16.4.9": (80, 5),
    "10.0.0.77": (58, 12),
    "203.0.113.8": (40, 30),
    "198.51.100.14": (27, 3),
}
PATHS = ["/", "/login", "/api/items", "/api/items/42", "/static/app.js", "/health"]
OK = [200, 200, 200, 204]
BAD = [301, 403, 404, 500]


def line(ip, status):
    return (
        f'{ip} - - [05/Nov/2026:10:{random.randint(0, 59):02d}:{random.randint(0, 59):02d} +0000] '
        f'"GET {random.choice(PATHS)} HTTP/1.1" {status} {random.randint(100, 5000)}'
    )


lines = []
for ip, (ok, bad) in PROFILE.items():
    lines += [line(ip, random.choice(OK)) for _ in range(ok)]
    lines += [line(ip, random.choice(BAD)) for _ in range(bad)]
random.shuffle(lines)
lines.insert(10, "# rotated by logrotate")
lines.insert(50, "")
lines.insert(90, "malformed line without a status")

with open(sys.argv[1], "w") as f:
    f.write("\n".join(lines) + "\n")
