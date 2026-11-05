"""Identity files: Wikidata ids, coherent dates, picture credits, aliases, no motorcycle results for GP Explorer drivers."""
import json
import os
import re

ROOT = os.path.expanduser(os.environ.get("MSDB_ROOT", "~/clone-motorsportdb"))
BIKE = re.compile(r"^(Grand_Prix_\d+cc|MotoGP|Moto2|Moto3|MotoE)$")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_identity(kind, ident, data, errors):
    where = f"{kind}/{ident}.json"
    wd = data.get("wikidata")
    if wd is not None and not re.fullmatch(r"Q\d+", str(wd)):
        errors.append(f"[WIKIDATA] {where}: '{wd}' is not a Wikidata id")
    dob, dod = data.get("dateOfBirth"), data.get("dateOfDeath")
    if dob and dod and str(dod) < str(dob):
        errors.append(f"[DATES] {where}: died ({dod}) before being born ({dob})")
    credit = data.get("pictureCredit")
    if credit is not None:
        if not isinstance(credit, dict) or not credit.get("license") or not credit.get("author"):
            errors.append(f"[CREDIT] {where}: pictureCredit needs an author and a license")
        elif not str(credit.get("source", "")).startswith("https://"):
            errors.append(f"[CREDIT] {where}: pictureCredit source must be an https URL")
    aliases = data.get("aliases")
    if aliases is not None and (not isinstance(aliases, list) or not all(isinstance(a, str) and a.strip() for a in aliases)):
        errors.append(f"[ALIASES] {where}: aliases must be a list of names")


def main():
    errors = []
    for kind in ("drivers", "teams"):
        folder = os.path.join(ROOT, kind)
        seen_wd = {}
        for f in sorted(os.listdir(folder)):
            if f.endswith(".json"):
                data = load(os.path.join(folder, f))
                check_identity(kind, f[:-5], data, errors)
                if kind == "drivers" and data.get("wikidata"):
                    if data["wikidata"] in seen_wd:
                        errors.append(f"[WIKIDATA] {data['wikidata']} is linked to {seen_wd[data['wikidata']]} and {f[:-5]} (same person twice?)")
                    seen_wd[data["wikidata"]] = f[:-5]

    # GP Explorer drivers are influencers: a motorcycle result means a homonym was merged (Maxime / Max Biaggi)
    races = os.path.join(ROOT, "races")
    gpx, bike = set(), set()
    for champ in os.listdir(races):
        path = os.path.join(races, champ)
        if not os.path.isdir(path) or not (champ == "GP_Explorer" or BIKE.match(champ)):
            continue
        for f in os.listdir(path):
            if f.endswith(".json"):
                for sessions in load(os.path.join(path, f)).get("events", {}).values():
                    for cars in sessions.values():
                        for e in cars.values():
                            (gpx if champ == "GP_Explorer" else bike).update(e.get("drivers", []))
    for d in sorted(gpx & bike):
        errors.append(f"[HOMONYM] {d} has GP Explorer and motorcycle Grand Prix results")

    if errors:
        print("❌ identities-motorsportdb")
        for e in errors:
            print("-", e)
        exit(1)
    print("✅ identities-motorsportdb passed successfully!")


if __name__ == "__main__":
    main()
