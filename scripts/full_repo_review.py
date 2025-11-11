#!/usr/bin/env python3

"""
Full Repository Review for EasyPost MCP Monorepo

------------------------------------------------

Performs a deep, read-only structural and configuration audit.

Checks:
  - Directory and module integrity
  - Missing or duplicate critical files
  - Dependency lists (Python + Node)
  - Environment configuration sanity
  - Docker + Compose consistency
  - Project metadata (README, License)
  - Code metrics (file count, LOC, largest files)
  - Security checks (secrets or tokens in .env)

Outputs:
  - Human-readable summary to stdout
  - Optional JSON report for CI/CD integration
"""

import os
import re
import sys
import json
import hashlib
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
IGNORE_DIRS = {
    "node_modules", "__pycache__", ".venv", ".cursor", ".git", ".DS_Store", ".mypy_cache",
    ".normalize_backup", ".pytest_cache", ".ruff_cache", "htmlcov", "coverage", "dist",
    "build", ".next", ".vite"
}
CRITICAL_PATHS = [
    "apps/backend/src/server.py",
    "apps/frontend/src/App.jsx",
    "deploy/docker-compose.yml",
    ".cursor/config.json",
    "Makefile",
]
ENV_PATHS = [".env", ".env.development", ".env.production"]
RESULTS = defaultdict(list)


# ---------------------- Utility Functions ----------------------

def line_count(path: Path) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()[:10]
    except Exception:
        return "ERR"


def list_files(base: Path):
    for dirpath, dirnames, filenames in os.walk(base):
        # Filter ignored directories
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        # Skip entire directory trees that are ignored
        rel_dir = Path(dirpath).relative_to(base)
        if any(part in IGNORE_DIRS for part in rel_dir.parts):
            dirnames[:] = []
            continue
        # Skip backup directories
        if ".normalize_backup" in rel_dir.parts or "venv" in rel_dir.parts:
            dirnames[:] = []
            continue
        for f in filenames:
            yield Path(dirpath) / f


def read_env_file(path: Path) -> dict:
    data = {}
    if not path.exists():
        return data
    for line in path.read_text().splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.strip()
    return data


# ---------------------- 1. Basic Repo Stats ----------------------

def repo_stats():
    summary = defaultdict(lambda: {"files": 0, "lines": 0})
    file_sizes = []
    for f in list_files(ROOT):
        ext = f.suffix.lower()
        lines = line_count(f)
        size = f.stat().st_size
        summary[ext]["files"] += 1
        summary[ext]["lines"] += lines
        file_sizes.append((f, size))
    largest = sorted(file_sizes, key=lambda x: x[1], reverse=True)[:5]
    return summary, largest


# ---------------------- 2. Check Critical Paths ----------------------

def check_structure():
    for path in CRITICAL_PATHS:
        if not (ROOT / path).exists():
            RESULTS["missing"].append(path)
    for d in ["apps/backend", "apps/frontend", "deploy"]:
        if not (ROOT / d).exists():
            RESULTS["missing"].append(d)


# ---------------------- 3. Dependency Analysis ----------------------

def analyze_dependencies():
    py_reqs = ROOT / "apps/backend/requirements.txt"
    node_pkg = ROOT / "apps/frontend/package.json"
    if py_reqs.exists():
        pkgs = [ln.strip().split("==")[0] for ln in py_reqs.read_text().splitlines() if ln and not ln.startswith("#")]
        RESULTS["python_deps"] = pkgs
    if node_pkg.exists():
        pkg_data = json.loads(node_pkg.read_text())
        RESULTS["node_deps"] = list(pkg_data.get("dependencies", {}).keys())


# ---------------------- 4. Environment Audit ----------------------

def check_env_files():
    for env_path in ENV_PATHS:
        p = ROOT / env_path
        if p.exists():
            vars_ = read_env_file(p)
            RESULTS["env_files"].append({
                "file": env_path,
                "vars": list(vars_.keys())
            })
            secrets = [k for k in vars_ if re.search(r"KEY|SECRET|TOKEN", k, re.I)]
            if secrets:
                RESULTS["env_secrets"].append({env_path: secrets})
        else:
            RESULTS["missing_env"].append(env_path)


# ---------------------- 5. Docker Audit ----------------------

def check_docker():
    compose = ROOT / "deploy/docker-compose.yml"
    if not compose.exists():
        RESULTS["docker_issues"].append("docker-compose.yml missing")
        return
    text = compose.read_text()
    if "backend" not in text or "frontend" not in text:
        RESULTS["docker_issues"].append("compose missing backend/frontend services")
    # Note: Checking for redis/postgres is optional - postgres exists, redis may not
    if "postgres" not in text:
        RESULTS["docker_issues"].append("compose missing postgres service")


# ---------------------- 6. Duplicate Files ----------------------

def detect_duplicates():
    hashes = defaultdict(list)
    for f in list_files(ROOT):
        # Skip empty files and common placeholders
        if f.stat().st_size == 0:
            continue
        # Skip binary files
        if f.suffix.lower() in ['.so', '.dylib', '.exe', '.png', '.zip']:
            continue
        h = hash_file(f)
        if h != "ERR":
            hashes[h].append(str(f.relative_to(ROOT)))
    dupes = {h: v for h, v in hashes.items() if len(v) > 1}
    if dupes:
        # Filter out expected duplicates (empty files, etc.)
        filtered_dupes = {}
        for h, paths in dupes.items():
            # Skip if all paths are empty placeholders
            if all('__init__.py' in p or '.gitkeep' in p or 'py.typed' in p for p in paths):
                continue
            filtered_dupes[h] = paths
        if filtered_dupes:
            RESULTS["duplicates"] = dict(list(filtered_dupes.items())[:10])


# ---------------------- 7. Security Scan ----------------------

def security_scan():
    suspicious = []
    pattern = re.compile(r"(EASYPOST_|SECRET|TOKEN|PASSWORD)[^=]*=\s*['\"]?[A-Za-z0-9\-_]{16,}")
    for env in list_files(ROOT):
        if env.name.startswith(".env") and not env.name.endswith(".example"):
            try:
                text = env.read_text()
                if pattern.search(text):
                    suspicious.append(str(env.relative_to(ROOT)))
            except Exception:
                pass
    if suspicious:
        RESULTS["secrets_found"] = suspicious


# ---------------------- 8. Summary & Reporting ----------------------

def print_summary(summary, largest):
    print(f"\n📁 Repository Root: {ROOT}")
    total_files = sum(v["files"] for v in summary.values())
    total_lines = sum(v["lines"] for v in summary.values())
    print(f"Total files: {total_files:,}")
    print(f"Total lines: {total_lines:,}")
    
    # Filter out binary/compiled files for cleaner output
    code_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.md', '.json', '.yml', '.yaml', '.sh', '.css', '.html'}
    code_files = sum(v["files"] for ext, v in summary.items() if ext in code_extensions or ext == '')
    code_lines = sum(v["lines"] for ext, v in summary.items() if ext in code_extensions or ext == '')
    print(f"Code files (excluding binaries): {code_files:,}")
    print(f"Code lines (excluding binaries): {code_lines:,}")
    
    print("\n📊 Languages / File Extensions:")
    for ext, stats in sorted(summary.items(), key=lambda kv: kv[1]["lines"], reverse=True)[:20]:
        if stats['files'] > 0:
            print(f"  {ext or '[none]':>8}: {stats['files']:>5} files, {stats['lines']:>8} lines")

    if largest:
        print("\n📦 Largest Files (excluding binaries):")
        # Filter out binaries
        text_files = [(f, s) for f, s in largest if f.suffix.lower() not in ['.so', '.dylib', '.exe', '.zip']]
        for f, s in text_files[:5]:
            print(f"  {f.relative_to(ROOT)} ({s/1024:.1f} KB)")

    if RESULTS["missing"]:
        print("\n⚠️  Missing Critical Files:")
        for m in RESULTS["missing"]:
            print(f"   - {m}")
    else:
        print("\n✅ All critical files present")

    if RESULTS.get("docker_issues"):
        print("\n🐳 Docker Issues:")
        for i in RESULTS["docker_issues"]:
            print(f"   - {i}")
    else:
        print("\n✅ Docker configuration valid")

    if RESULTS.get("env_secrets"):
        print("\n🔐 Secrets Detected in .env:")
        for e in RESULTS["env_secrets"]:
            print(f"   - {e}")
        print("   ⚠️  Ensure .env files are in .gitignore")

    if RESULTS.get("duplicates"):
        print("\n⚠️  Duplicate Files (by hash):")
        for h, paths in list(RESULTS["duplicates"].items())[:5]:
            print(f"   [{h}]")
            for p in paths[:3]:
                print(f"      - {p}")
            if len(paths) > 3:
                print(f"      ... and {len(paths) - 3} more")
    else:
        print("\n✅ No significant duplicate files found")

    # Dependency summary
    if RESULTS.get("python_deps"):
        print(f"\n📦 Python Dependencies: {len(RESULTS['python_deps'])} packages")
    if RESULTS.get("node_deps"):
        print(f"📦 Node Dependencies: {len(RESULTS['node_deps'])} packages")

    print("\n✅ Review complete.")
    print("\nTo export results as JSON: python3 scripts/full_repo_review.py --json > repo_report.json")


# ---------------------- Main ----------------------

def main():
    summary, largest = repo_stats()
    check_structure()
    analyze_dependencies()
    check_env_files()
    check_docker()
    detect_duplicates()
    security_scan()

    if "--json" in sys.argv:
        output = {
            "summary": summary,
            "results": RESULTS,
            "largest": [(str(f), s) for f, s in largest],
        }
        print(json.dumps(output, indent=2))
    else:
        print_summary(summary, largest)


if __name__ == "__main__":
    main()

