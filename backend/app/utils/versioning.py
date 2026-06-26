# Model versioning utilities -- 2026-06-26 09:28:01
from typing import Tuple

def parse_version(version: str) -> Tuple[int, int, int]:
    parts = version.split('.')
    return tuple(int(p) for p in parts[:3])  # type: ignore

def bump_major(version: str) -> str:
    major, minor, patch = parse_version(version)
    return f'{major + 1}.0.0'

def bump_minor(version: str) -> str:
    major, minor, patch = parse_version(version)
    return f'{major}.{minor + 1}.0'

def bump_patch(version: str) -> str:
    major, minor, patch = parse_version(version)
    return f'{major}.{minor}.{patch + 1}'

def compare_versions(a: str, b: str) -> int:
    av = parse_version(a)
    bv = parse_version(b)
    if av > bv: return 1
    if av < bv: return -1
    return 0

def is_stable(version: str) -> bool:
    return not any(tag in version.lower() for tag in ['alpha','beta','rc','dev'])