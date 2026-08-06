#!/usr/bin/env python3
"""validate_caveat.py — structural gate for the CAVEaT STIX corpus.

Why this exists
---------------
PR #3 (2026-08-05) added a file at the repository root carrying
`"id": "attack-pattern--temp-id-placeholder"`, no mitigation, no relationship,
and CVE details that contradicted the MITRE record — while its own checklist
asserted "[x] STIX 2.1 format compliance". Nothing in the repo could contradict
that claim, so it reached human review on formatting alone. Everything this
script checks is something that submission would have failed automatically.

It cannot check whether a claim is TRUE — no tool can. It checks that every
claim carries a citation, sits in the right place, and joins the graph, so a
reviewer's attention goes to the substance instead of the shape.

Modes
-----
  --changed FILE...   validate only these paths (what CI runs on a PR)
  --all               validate the whole corpus (audit; legacy drift = warning)
  --strict            warnings become errors

Graph integrity always loads the full corpus, whatever is being validated.

Exit: 0 clean (warnings allowed unless --strict), 1 errors found.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "caveat"
SCHEMA_DIR = REPO / "schema"

OBJECT_TYPES = ("attack-pattern", "course-of-action", "relationship")
UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")

# Files legitimately outside caveat/ — everything else at top level is suspect.
ALLOWED_NON_DATA = {
    "README.md", "CLAUDE.md", "CONTRIBUTING.md", "LICENSE", ".gitignore",
}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path, msg: str) -> None:
        self.errors.append(f"{path}: {msg}")

    def warn(self, path, msg: str) -> None:
        self.warnings.append(f"{path}: {msg}")


def load_schemas() -> dict:
    out = {}
    for t in OBJECT_TYPES:
        p = SCHEMA_DIR / f"{t}.schema.json"
        if p.exists():
            out[t] = json.loads(p.read_text())
    return out


def corpus_ids() -> set[str]:
    """Every STIX id in the corpus, including those nested inside bundles."""
    ids: set[str] = set()
    for f in sorted(DATA_DIR.rglob("*")):
        if not f.is_file():
            continue
        try:
            doc = json.loads(f.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if isinstance(doc, dict):
            if doc.get("id"):
                ids.add(doc["id"])
            for obj in doc.get("objects", []) or []:
                if isinstance(obj, dict) and obj.get("id"):
                    ids.add(obj["id"])
    return ids


def check_placement(path: Path, rel: str, rep: Report) -> bool:
    """Data must live in caveat/<type>/. Returns False if placement is wrong."""
    parts = Path(rel).parts
    if parts[0] != "caveat":
        if len(parts) == 1 and parts[0] in ALLOWED_NON_DATA:
            return False
        rep.error(rel,
                  "data files must live under caveat/<object-type>/ — a STIX object at "
                  "the repository root is not part of the corpus")
        return False
    if len(parts) != 3 or parts[1] not in OBJECT_TYPES:
        rep.error(rel, f"expected caveat/<{'|'.join(OBJECT_TYPES)}>/<filename>")
        return False
    return True


def check_one(path: Path, rel: str, schemas: dict, ids: set[str],
              rep: Report, legacy_ok: bool) -> None:
    if not check_placement(path, rel, rep):
        return
    dir_type = Path(rel).parts[1]
    fname = Path(rel).name

    if fname.endswith(".json"):
        rep.error(rel, "filenames carry no extension — use the STIX id with '--' collapsed "
                       f"to '-' (e.g. {dir_type}-<uuid>)")

    try:
        doc = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        rep.error(rel, f"invalid JSON: {e}")
        return
    if not isinstance(doc, dict):
        rep.error(rel, "top level must be a JSON object")
        return

    if "objects" in doc:
        msg = ("bundle detected. New data files must be bare STIX objects, one per file, "
               "not bundles")
        rep.warn(rel, msg + " (pre-existing)") if legacy_ok else rep.error(rel, msg)
        return

    obj_type = doc.get("type")
    if obj_type != dir_type:
        rep.error(rel, f'type is "{obj_type}" but the file sits in caveat/{dir_type}/')
        return

    # id ↔ filename. The single check that would have caught the placeholder id.
    oid = doc.get("id", "")
    if not isinstance(oid, str) or "--" not in oid:
        rep.error(rel, f'id must look like "{dir_type}--<uuid>", got {oid!r}')
    else:
        suffix = oid.split("--", 1)[1]
        if not UUID_RE.match(suffix):
            rep.error(rel, f'id suffix is not a UUID: {suffix!r} '
                           f'(a placeholder or descriptive id is never valid)')
        expected = oid.replace("--", "-")
        if fname != expected:
            msg = f"filename does not match id — expected {expected!r}"
            rep.warn(rel, msg + " (pre-existing)") if legacy_ok else rep.error(rel, msg)

    schema = schemas.get(dir_type)
    if schema:
        try:
            import jsonschema
        except ImportError:
            rep.warn(rel, "jsonschema not installed — skipped schema validation "
                          "(pip install jsonschema)")
        else:
            validator = jsonschema.Draft202012Validator(schema)
            for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
                loc = "/".join(str(p) for p in err.path) or "(root)"
                rep.error(rel, f"schema: {loc}: {err.message}")

    if dir_type == "relationship":
        for ref in ("source_ref", "target_ref"):
            val = doc.get(ref)
            if val and val not in ids:
                rep.error(rel, f"{ref} points at {val}, which is not in the corpus — "
                               "add the referenced object in the same change")


def orphan_check(rep: Report) -> None:
    """Every attack-pattern should be the target of at least one mitigation.

    CAVEaT's value is the course-of-action -> attack-pattern graph; a technique
    with no mitigation is half an entry. Advisory, not fatal.
    """
    targets, patterns = set(), {}
    for f in sorted(DATA_DIR.rglob("*")):
        if not f.is_file():
            continue
        try:
            doc = json.loads(f.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not isinstance(doc, dict):
            continue
        for o in ([doc] + list(doc.get("objects", []) or [])):
            if not isinstance(o, dict):
                continue
            if o.get("type") == "relationship" and o.get("target_ref"):
                targets.add(o["target_ref"])
            elif o.get("type") == "attack-pattern" and o.get("id"):
                patterns[o["id"]] = str(f.relative_to(REPO))
    for pid, loc in sorted(patterns.items()):
        if pid not in targets:
            rep.warn(loc, f"attack-pattern {pid} has no course-of-action mitigating it")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--changed", nargs="*", metavar="FILE",
                    help="validate only these paths (CI mode)")
    ap.add_argument("--all", action="store_true", help="validate the whole corpus")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args(argv)

    schemas = load_schemas()
    if not schemas:
        print(f"error: no schemas found in {SCHEMA_DIR}", file=sys.stderr)
        return 1
    ids = corpus_ids()
    rep = Report()

    if args.all or not args.changed:
        targets = [p for p in sorted(DATA_DIR.rglob("*")) if p.is_file()]
        legacy_ok = True          # audit mode: existing drift reports as warnings
    else:
        targets = [REPO / c for c in args.changed]
        legacy_ok = False         # a changed file is held to the full standard

    checked = 0
    for path in targets:
        if not path.exists() or not path.is_file():
            continue              # deletions, directories, blank args
        try:
            rel = str(path.resolve().relative_to(REPO))
        except ValueError:
            rep.warn(str(path), "outside the repository — skipped")
            continue
        parts = Path(rel).parts
        if not parts:
            continue
        # Only data files are our business. Anything under caveat/ counts, as does
        # a stray top-level file that isn't a known doc — that's the root-dump case.
        is_data = parts[0] == "caveat"
        is_stray_root = len(parts) == 1 and parts[0] not in ALLOWED_NON_DATA
        if not (is_data or is_stray_root):
            continue              # skip schema/, scripts/, .github/, known docs
        check_one(path, rel, schemas, ids, rep, legacy_ok)
        checked += 1

    if args.all or not args.changed:
        orphan_check(rep)

    for w in rep.warnings:
        print(f"WARN  {w}")
    for e in rep.errors:
        print(f"ERROR {e}")

    failed = bool(rep.errors) or (args.strict and bool(rep.warnings))
    print(f"\n{checked} file(s) checked · {len(rep.errors)} error(s) · "
          f"{len(rep.warnings)} warning(s) — {'FAIL' if failed else 'OK'}")
    if rep.errors:
        print("\nSee CONTRIBUTING.md for the data model and filename convention.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
