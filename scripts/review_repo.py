#!/usr/bin/env python3
"""
Repository Review Script for EasyPost MCP Project
Comprehensive analysis of project structure, code health, and potential issues.
Generates Markdown report for easy viewing in Cursor.
"""

import os
import json
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# --- Configuration ---
ROOT = Path(__file__).resolve().parents[1]
IGNORE = {
    "node_modules", "__pycache__", ".venv", "venv", ".cursor", ".git", 
    ".DS_Store", "dist", "build", "coverage", "htmlcov", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "logs", "data", ".direnv", "htmlcov",
    "*.egg-info", ".coverage"
}

# Detect project structure (normalized or legacy)
BACKEND_PATH = ROOT / "apps" / "backend" if (ROOT / "apps" / "backend").exists() else ROOT / "backend"
FRONTEND_PATH = ROOT / "apps" / "frontend" if (ROOT / "apps" / "frontend").exists() else ROOT / "frontend"
DOCKER_PATH = ROOT / "deploy" if (ROOT / "deploy").exists() else ROOT / "docker"

IS_NORMALIZED = (ROOT / "apps").exists()

# --- Helpers ---

def hash_file(path: Path) -> str:
    """Hash file for duplication detection."""
    h = hashlib.md5()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    except Exception:
        return "ERR"
    return h.hexdigest()[:8]


def count_lines(path: Path) -> int:
    """Count lines in file."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def get_file_size(path: Path) -> int:
    """Get file size in bytes."""
    try:
        return path.stat().st_size
    except Exception:
        return 0


def detect_language(path: Path) -> str:
    """Detect programming language from file extension."""
    ext_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript (React)",
        ".ts": "TypeScript",
        ".tsx": "TypeScript (React)",
        ".json": "JSON",
        ".yml": "YAML",
        ".yaml": "YAML",
        ".md": "Markdown",
        ".sh": "Shell",
        ".sql": "SQL",
        ".css": "CSS",
        ".html": "HTML",
    }
    return ext_map.get(path.suffix, "Other")


# --- Collect repository data ---

print("🔍 Scanning repository...")

summary = defaultdict(lambda: {"files": 0, "lines": 0, "size": 0})
hashes = defaultdict(list)
languages = defaultdict(lambda: {"files": 0, "lines": 0})
structure_data = {}
issues = []
warnings = []
recommendations = []

# Walk repository
for dirpath, dirnames, filenames in os.walk(ROOT):
    # Filter ignored directories
    dirnames[:] = [d for d in dirnames if d not in IGNORE]
    
    # Skip entire directory trees that are ignored
    rel_dir = Path(dirpath).relative_to(ROOT)
    if any(part in IGNORE for part in rel_dir.parts):
        dirnames[:] = []  # Don't descend into ignored directories
        continue
    
    for f in filenames:
        if f.startswith(".") and f not in [".gitignore", ".env.example"]:
            continue
            
        path = Path(dirpath) / f
        rel = path.relative_to(ROOT)
        
        # Skip ignored paths (double-check)
        if any(part in IGNORE for part in rel.parts):
            continue
        
        # Skip files in venv directories (even if not in IGNORE)
        if "venv" in rel.parts or ".venv" in rel.parts or ".direnv" in rel.parts:
            continue
        
        ext = path.suffix
        lines = count_lines(path)
        size = get_file_size(path)
        lang = detect_language(path)
        
        summary[ext]["files"] += 1
        summary[ext]["lines"] += lines
        summary[ext]["size"] += size
        
        languages[lang]["files"] += 1
        languages[lang]["lines"] += lines
        
        file_hash = hash_file(path)
        hashes[file_hash].append(str(rel))

# --- Calculate metrics ---

total_files = sum(v["files"] for v in summary.values())
total_lines = sum(v["lines"] for v in summary.values())
total_size = sum(v["size"] for v in summary.values())

# --- Structure analysis ---

def analyze_structure(base: Path, max_depth: int = 3) -> Dict:
    """Analyze directory structure."""
    result = {}
    if not base.exists():
        return result
    
    try:
        for item in sorted(base.iterdir()):
            if item.name.startswith(".") and item.name not in [".gitignore", ".env.example"]:
                continue
            if item.name in IGNORE:
                continue
            
            if item.is_dir():
                if max_depth > 0:
                    result[item.name] = analyze_structure(item, max_depth - 1)
                else:
                    result[item.name] = "..."
            else:
                result.setdefault("_files", []).append(item.name)
    except PermissionError:
        pass
    
    return result

structure_data = analyze_structure(ROOT, max_depth=2)

# --- Project-specific checks ---

# Check backend structure
if BACKEND_PATH.exists():
    backend_src = BACKEND_PATH / "src"
    if backend_src.exists():
        mcp_server = backend_src / "mcp_server"
        if not mcp_server.exists():
            issues.append("Missing MCP server directory: expected src/mcp_server/")
        else:
            if not (mcp_server / "tools").exists():
                warnings.append("MCP tools directory missing: src/mcp_server/tools/")
            if not (mcp_server / "resources").exists():
                warnings.append("MCP resources directory missing: src/mcp_server/resources/")
        
        if not (backend_src / "routers").exists():
            warnings.append("FastAPI routers directory missing: src/routers/")
        if not (backend_src / "services").exists():
            warnings.append("Services directory missing: src/services/")
else:
    issues.append(f"Backend directory not found: {BACKEND_PATH}")

# Check frontend structure
if FRONTEND_PATH.exists():
    frontend_src = FRONTEND_PATH / "src"
    if frontend_src.exists():
        if not (frontend_src / "components").exists():
            warnings.append("React components directory missing: src/components/")
        if not (frontend_src / "pages").exists():
            warnings.append("Pages directory missing: src/pages/")
        if not (frontend_src / "services").exists():
            warnings.append("API services directory missing: src/services/")
else:
    issues.append(f"Frontend directory not found: {FRONTEND_PATH}")

# Check Docker configuration
if not DOCKER_PATH.exists():
    issues.append(f"Docker configuration directory not found: {DOCKER_PATH}")
elif not (DOCKER_PATH / "docker-compose.yml").exists():
    warnings.append("docker-compose.yml not found in Docker directory")

# Check key configuration files
if not (ROOT / "Makefile").exists():
    warnings.append("Makefile not found")
if not (ROOT / ".cursor" / "config.json").exists():
    warnings.append(".cursor/config.json not found (affects Cursor indexing)")
if not (ROOT / ".gitignore").exists():
    warnings.append(".gitignore not found")

# Check for security issues
env_files = list(ROOT.glob(".env")) + list(ROOT.glob("**/.env"))
if env_files:
    warnings.append(f"Found {len(env_files)} .env file(s) - ensure they're in .gitignore")

# Check for test coverage
if BACKEND_PATH.exists():
    test_dir = BACKEND_PATH / "tests"
    if test_dir.exists():
        test_files = list(test_dir.rglob("test_*.py"))
        if len(test_files) < 5:
            warnings.append(f"Low test file count: {len(test_files)} test files found")
    else:
        warnings.append("Backend tests directory missing: tests/")

if FRONTEND_PATH.exists():
    test_files = list((FRONTEND_PATH / "src").rglob("*.test.{js,jsx,ts,tsx}"))
    if len(test_files) < 3:
        warnings.append(f"Low frontend test file count: {len(test_files)} test files found")

# Check for duplicate files
dupes = {k: v for k, v in hashes.items() if len(v) > 1 and k != "ERR"}
if dupes:
    warnings.append(f"Found {len(dupes)} potential duplicate file groups")

# --- Generate recommendations ---

if not IS_NORMALIZED:
    recommendations.append("Consider running normalization script: bash scripts/normalize_project.sh")

if BACKEND_PATH.exists():
    requirements = BACKEND_PATH / "requirements.txt"
    if requirements.exists():
        with open(requirements, "r") as f:
            req_count = len([l for l in f if l.strip() and not l.startswith("#")])
        if req_count > 50:
            recommendations.append(f"Backend has {req_count} dependencies - consider reviewing for unused packages")

if FRONTEND_PATH.exists():
    package_json = FRONTEND_PATH / "package.json"
    if package_json.exists():
        with open(package_json, "r") as f:
            pkg_data = json.load(f)
            dep_count = len(pkg_data.get("dependencies", {})) + len(pkg_data.get("devDependencies", {}))
        if dep_count > 100:
            recommendations.append(f"Frontend has {dep_count} dependencies - consider reviewing for unused packages")

# --- Generate Markdown Report ---

report = f"""# Repository Review: EasyPost MCP Project

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Root:** `{ROOT}`  
**Structure:** {'Normalized (apps/backend, apps/frontend)' if IS_NORMALIZED else 'Legacy (backend/, frontend/)'}

---

## 📊 Overview

- **Total Files:** {total_files:,}
- **Total Lines of Code:** {total_lines:,}
- **Total Size:** {total_size / 1024 / 1024:.2f} MB
- **Languages Detected:** {len(languages)}

---

## 📁 File Statistics by Extension

| Extension | Files | Lines | Size |
|-----------|-------|-------|------|
"""

for ext, stats in sorted(summary.items(), key=lambda kv: kv[1]["lines"], reverse=True):
    ext_display = ext if ext else "[no ext]"
    size_mb = stats["size"] / 1024 / 1024
    report += f"| `{ext_display}` | {stats['files']:,} | {stats['lines']:,} | {size_mb:.2f} MB |\n"

report += f"""
---

## 🔤 Languages Breakdown

| Language | Files | Lines |
|----------|-------|-------|
"""

for lang, stats in sorted(languages.items(), key=lambda kv: kv[1]["lines"], reverse=True):
    report += f"| {lang} | {stats['files']:,} | {stats['lines']:,} |\n"

structure_json = json.dumps(structure_data, indent=2)
report += """
## 🏗️ Project Structure

```json
""" + structure_json + """
```

---

## ✅ Health Check

"""

if issues:
    report += "### ❌ Critical Issues\n\n"
    for issue in issues:
        report += f"- {issue}\n"
    report += "\n"
else:
    report += "### ✅ No Critical Issues Found\n\n"

if warnings:
    report += "### ⚠️ Warnings\n\n"
    for warning in warnings[:10]:  # Limit to 10 warnings
        report += f"- {warning}\n"
    if len(warnings) > 10:
        report += f"\n*... and {len(warnings) - 10} more warnings*\n"
    report += "\n"

if recommendations:
    report += "### 💡 Recommendations\n\n"
    for rec in recommendations:
        report += f"- {rec}\n"
    report += "\n"

if dupes:
    report += "### 🔄 Potential Duplicate Files\n\n"
    for i, (hash_val, paths) in enumerate(list(dupes.items())[:5], 1):
        report += f"**Group {i}:**\n"
        for path in paths:
            report += f"- `{path}`\n"
        report += "\n"
    if len(dupes) > 5:
        report += f"*... and {len(dupes) - 5} more duplicate groups*\n"

report += f"""
---

## 📍 Key Paths

- **Backend:** `{BACKEND_PATH.relative_to(ROOT)}`
- **Frontend:** `{FRONTEND_PATH.relative_to(ROOT)}`
- **Docker:** `{DOCKER_PATH.relative_to(ROOT)}`

---

## 🔍 Detailed Analysis

### Backend Structure
"""

if BACKEND_PATH.exists():
    backend_files = list(BACKEND_PATH.rglob("*.py"))
    backend_tests = list((BACKEND_PATH / "tests").rglob("test_*.py")) if (BACKEND_PATH / "tests").exists() else []
    report += f"""
- Python files: {len(backend_files)}
- Test files: {len(backend_tests)}
- Test coverage: {len(backend_tests) / len(backend_files) * 100:.1f}% (if all files tested)
"""
else:
    report += "- Backend directory not found\n"

report += "\n### Frontend Structure\n"

if FRONTEND_PATH.exists():
    frontend_jsx = list((FRONTEND_PATH / "src").rglob("*.jsx")) if (FRONTEND_PATH / "src").exists() else []
    frontend_tsx = list((FRONTEND_PATH / "src").rglob("*.tsx")) if (FRONTEND_PATH / "src").exists() else []
    report += f"""
- React components (.jsx): {len(frontend_jsx)}
- TypeScript components (.tsx): {len(frontend_tsx)}
- Total components: {len(frontend_jsx) + len(frontend_tsx)}
"""
else:
    report += "- Frontend directory not found\n"

report += f"""
---

## 📝 Next Steps

1. Review critical issues above
2. Address warnings as needed
3. Consider recommendations for improvements
4. Run tests: `make test`
5. Check linting: `make lint`

---

*Report generated by `scripts/review_repo.py`*
"""

# --- Output ---

output_file = ROOT / "docs" / "reviews" / f"REPO_REVIEW_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(report)

print(f"\n✅ Repository review complete!")
print(f"📄 Report saved to: {output_file.relative_to(ROOT)}")
print(f"\n📊 Summary:")
print(f"   Files: {total_files:,}")
print(f"   Lines: {total_lines:,}")
print(f"   Issues: {len(issues)}")
print(f"   Warnings: {len(warnings)}")
print(f"   Recommendations: {len(recommendations)}")

if issues:
    print(f"\n❌ Critical issues found - please review the report!")

