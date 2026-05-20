import argparse
import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path


SERVICES = ["checkout", "login", "search", "payments", "profile"]
LEVELS = ["INFO", "INFO", "INFO", "WARN", "ERROR"]
USERS = ["alex", "sam", "jordan", "taylor", "casey", "morgan"]


MESSAGES = {
    "INFO": [
        "request completed",
        "user session refreshed",
        "cache hit",
        "background job completed",
    ],
    "WARN": [
        "slow response detected",
        "retrying external service",
        "high memory usage",
    ],
    "ERROR": [
        "database timeout",
        "payment authorization failed",
        "unexpected response from dependency",
    ],
}


def build_event() -> dict:
    level = random.choice(LEVELS)
    service = random.choice(SERVICES)

    if level == "ERROR":
        status_code = random.choice([500, 502, 503])
    elif level == "WARN":
        status_code = random.choice([200, 408, 429])
    else:
        status_code = random.choice([200, 200, 200, 201, 204])

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "service": service,
        "message": random.choice(MESSAGES[level]),
        "user": random.choice(USERS),
        "request_id": f"req-{random.randint(10000, 99999)}",
        "status_code": status_code,
        "response_ms": random.randint(20, 1800),
    }


def write_events(output_file: Path, count: int, interval: float) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("a", encoding="utf-8") as log_file:
        for event_number in range(1, count + 1):
            event = build_event()
            log_file.write(json.dumps(event) + "\n")
            log_file.flush()

            print(
                f"{event_number:>3}/{count} "
                f"{event['level']:<5} "
                f"{event['service']:<8} "
                f"{event['message']}"
            )

            if event_number < count and interval > 0:
                time.sleep(interval)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create simple JSON log events for Splunk practice."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=25,
        help="Number of log events to create. Default: 25",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.2,
        help="Seconds to wait between events. Default: 0.2",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("logs/app.log"),
        help="Log file path. Default: logs/app.log",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.count < 1:
        raise SystemExit("--count must be at least 1")

    write_events(args.output, args.count, args.interval)
    print(f"\nDone. Logs were written to: {args.output}")


if __name__ == "__main__":
    main()
