#!/usr/bin/env python3
"""Validate translations_ar.json with the same rules as the Arabic app.

The app drops malformed entries one by one at runtime; this validator is
stricter and fails on any problem so mistakes never reach users.

Usage: python tools/validate_translations.py [path]   (default: translations_ar.json)
Only the Python standard library is used.
"""
import json
import re
import sys
from pathlib import Path

SCHEMA_VERSION = 1
MAX_BYTES = 2 * 1024 * 1024
MAX_ENTRIES = 20000
MAX_TEXT_LENGTH = 8000
ARABIC = re.compile(r"[؀-ۿ]")


def _no_duplicates(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate key: {key!r}")
        seen[key] = value
    return seen


def validate(path):
    errors = []
    raw = Path(path).read_bytes()
    if len(raw) > MAX_BYTES:
        return [f"file is {len(raw)} bytes; limit is {MAX_BYTES}"]
    try:
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicates)
    except UnicodeDecodeError:
        return ["file is not valid UTF-8"]
    except ValueError as error:  # JSONDecodeError and duplicate keys
        return [f"invalid JSON: {error}"]
    if not isinstance(document, dict):
        return ["root must be a JSON object"]
    unknown = set(document) - {"schema_version", "updated_at", "translations"}
    if unknown:
        errors.append(f"unknown top-level fields: {sorted(unknown)}")
    if document.get("schema_version") != SCHEMA_VERSION or isinstance(
        document.get("schema_version"), bool
    ):
        errors.append(f"schema_version must be the number {SCHEMA_VERSION}")
    updated = document.get("updated_at")
    if not isinstance(updated, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", updated):
        errors.append("updated_at must be a YYYY-MM-DD string")
    translations = document.get("translations")
    if not isinstance(translations, dict):
        return errors + ["translations must be a JSON object"]
    if not translations:
        errors.append("translations is empty")
    if len(translations) > MAX_ENTRIES:
        errors.append(f"{len(translations)} entries; limit is {MAX_ENTRIES}")
    for key, value in translations.items():
        label = key if len(key) <= 60 else key[:57] + "..."
        if not key or key != key.strip():
            errors.append(f"key must be non-empty with no surrounding spaces: {label!r}")
        if len(key) > MAX_TEXT_LENGTH:
            errors.append(f"key longer than {MAX_TEXT_LENGTH} characters: {label!r}")
        if not isinstance(value, str) or not value.strip():
            errors.append(f"value must be a non-empty string: {label!r}")
            continue
        if len(value) > MAX_TEXT_LENGTH:
            errors.append(f"value longer than {MAX_TEXT_LENGTH} characters: {label!r}")
        if not ARABIC.search(value):
            errors.append(f"value contains no Arabic text: {label!r}")
    return errors


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "translations_ar.json"
    errors = validate(path)
    if errors:
        print(f"{path}: {len(errors)} problem(s)")
        for error in errors:
            print(f"  - {error}")
        return 1
    count = len(json.loads(Path(path).read_text(encoding="utf-8"))["translations"])
    print(f"{path}: OK ({count} translations)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
