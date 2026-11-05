"""Driverdle runs client-side: its data file must be served (cached, 304) and consistent."""
import json
import os
import zlib
from datetime import datetime, timezone

import requests


def base_url():
    with open(os.path.join(os.path.dirname(__file__), "../../config.json"), encoding="utf-8") as f:
        url = json.load(f).get("URL_LOCAL_TEST", "http://localhost:8080")
    return url if url.startswith(("http://", "https://")) else "http://" + url


def main():
    errors = []
    url = base_url() + "/api/driverdle.php"
    r = requests.get(url, timeout=30)
    if r.status_code != 200:
        print(f"[HTTP] {url}: {r.status_code}")
        print("1 error(s)")
        exit(1)
    data = r.json()
    etag = r.headers.get("ETag")
    if not etag:
        errors.append("[CACHE] no ETag header")
    elif requests.get(url, headers={"If-None-Match": etag}, timeout=30).status_code != 304:
        errors.append("[CACHE] conditional request is not answered with 304")

    for key, width in (("classic", 5), ("f1", 10), ("all", 9)):
        rows = data.get(key) or []
        if not rows:
            errors.append(f"[DATA] '{key}' is empty")
            continue
        if any(len(r) != width for r in rows):
            errors.append(f"[DATA] '{key}' rows must have {width} values")
        ids = [r[0] for r in rows]
        if ids != sorted(ids):
            errors.append(f"[DATA] '{key}' must be sorted by id (the daily pick is an index)")
    names = set(data.get("names") or [])
    if not names:
        errors.append("[DATA] 'names' is empty")

    # the classic answer of the day is a valid guess (same pick as the browser)
    year = datetime.now(timezone.utc).year
    pool = [r for r in data.get("classic", []) if r[4] >= year - 1]
    if pool:
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        pick = pool[zlib.crc32(day.encode()) % len(pool)]
        letters = "".join(c for c in pick[3] if "A" <= c <= "Z")
        if letters not in names:
            errors.append(f"[DATA] today's answer {pick[0]} ({letters}) is not an accepted guess")
    else:
        errors.append("[DATA] no driver can be the classic answer this year")

    # the per-guess endpoints were removed: the game no longer queries the server
    for old in ("validateGuess.php", "getDriverOfToday.php", "compareDriverF1.php"):
        code = requests.get(f"{base_url()}/assets/php/games/driverdle/{old}", timeout=30).status_code
        if code == 200:
            errors.append(f"[LEGACY] {old} still answers 200")

    for e in errors:
        print(e)
    print("OK" if not errors else f"{len(errors)} error(s)")
    exit(1 if errors else 0)


if __name__ == "__main__":
    main()
