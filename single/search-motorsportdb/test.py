"""Client-side search: the index must be served, cached and contain drivers, teams and championships."""
import json
import os
import sys

import requests


def base_url():
    with open(os.path.join(os.path.dirname(__file__), "../../config.json"), encoding="utf-8") as f:
        url = json.load(f).get("URL_LOCAL_TEST", "http://localhost:8080")
    return url if url.startswith(("http://", "https://")) else "http://" + url


def main():
    url = base_url() + "/api/search-index.php"
    r = requests.get(url, timeout=30)
    errors = []
    if r.status_code != 200:
        errors.append(f"[HTTP] {url}: {r.status_code}")
    else:
        data = r.json()
        for key in ("d", "t", "c"):
            if not data.get(key):
                errors.append(f"[INDEX] missing or empty '{key}'")
        if "ETag" not in r.headers:
            errors.append("[CACHE] no ETag header")
        else:
            again = requests.get(url, headers={"If-None-Match": r.headers["ETag"]}, timeout=30)
            if again.status_code != 304:
                errors.append(f"[CACHE] conditional request returned {again.status_code}, expected 304")
        names = {row[1] for row in data.get("t", [])}
        aliases = {a for row in data.get("t", []) if len(row) > 7 for a in row[7]}
        if "Renault" not in aliases:
            errors.append("[ALIASES] 'Renault' alias of Alpine not found")
        if not names:
            errors.append("[INDEX] no team names")
    for e in errors:
        print(e)
    print("OK" if not errors else f"{len(errors)} error(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
