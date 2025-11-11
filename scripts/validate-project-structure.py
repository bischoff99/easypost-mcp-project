#!/usr/bin/env python3
"""
Project structure validation script.

Enforces directory structure and file organization standards.
Run before commits to ensure compliance.
"""

import os
import sys
from pathlib import Path

# Expected directory structure
REQUIRED_DIRS = [
    "backend/src",
    "backend/tests/unit",
    "backend/tests/integration",
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/src/services",
    "docs/architecture",
    "docs/guides",
    "scripts",
    ".cursor/commands",
    ".cursor/rules",
]

REQUIRED_FILES = [
    "README.md",
    "CLAUDE.md",
    "Makefile",
    "docker/docker-compose.yml",
    "backend/requirements.txt",
    "backend/pytest.ini",
    "frontend/package.json",
    "frontend/vite.config.js",
    "docs/README.md",
]

# Files that should NOT be in root
FORBIDDEN_ROOT_FILES = [
    "test.py",
    "temp.py",
    "debug.py",
    "*.pyc",
    "__pycache__",
]

# Directories that should be clean (no .py files except __init__.py)
CLEAN_DIRS = [
    "docs",
    "scripts",  # Should only have .sh files
]


def validate_structure():
    """Validate project structure compliance."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    errors = []
    warnings = []

    print("🔍 Validating project structure...")
    print(f"   Project root: {project_root}")
    print()

    # Check required directories exist
    print("📁 Checking required directories...")
    for dir_path in REQUIRED_DIRS:
        full_path = project_root / dir_path
        if not full_path.exists():
            errors.append(f"Missing required directory: {dir_path}")
        elif not full_path.is_dir():
            errors.append(f"Path exists but is not a directory: {dir_path}")
        else:
            print(f"   ✓ {dir_path}")

    print()

    # Check required files exist
    print("📄 Checking required files...")
    for file_path in REQUIRED_FILES:
        full_path = project_root / file_path
        if not full_path.exists():
            errors.append(f"Missing required file: {file_path}")
        else:
            print(f"   ✓ {file_path}")

    print()

    # Check for forbidden root files
    print("🚫 Checking for forbidden root files...")
    root_files = [f for f in os.listdir(project_root) if os.path.isfile(f)]
    forbidden_found = []

    for file in root_files:
        if file.startswith("test_") or file.startswith("temp") or file.startswith("debug"):
            forbidden_found.append(file)
        elif file.endswith(".pyc"):
            forbidden_found.append(file)

    if forbidden_found:
        warnings.extend([f"Forbidden file in root: {f}" for f in forbidden_found])
    else:
        print("   ✓ No forbidden files in root")

    print()

    # Check test organization
    print("🧪 Checking test organization...")
    backend_tests = project_root / "backend/tests"
    if backend_tests.exists():
        # Should have unit/ and integration/ directories
        if not (backend_tests / "unit").exists():
            warnings.append("Missing backend/tests/unit/ directory")
        else:
            print("   ✓ backend/tests/unit/ exists")

        if not (backend_tests / "integration").exists():
            warnings.append("Missing backend/tests/integration/ directory")
        else:
            print("   ✓ backend/tests/integration/ exists")

        # Check for test files in wrong places
        test_files_in_root = list(backend_tests.glob("test_*.py"))
        if test_files_in_root:
            warnings.extend([f"Test file in tests/ root: {f.name}" for f in test_files_in_root])

    print()

    # Check documentation organization
    print("📚 Checking documentation...")
    docs_dir = project_root / "docs"
    if docs_dir.exists():
        if not (docs_dir / "README.md").exists():
            warnings.append("Missing docs/README.md index file")
        else:
            print("   ✓ docs/README.md exists")

        if not (docs_dir / "architecture").exists():
            warnings.append("Missing docs/architecture/ directory")
        else:
            print("   ✓ docs/architecture/ exists")

    print()

    # Check for large files (>5MB)
    print("📦 Checking for large files...")
    large_files = []
    for root, dirs, files in os.walk(project_root):
        # Skip venv, node_modules, .git
        dirs[:] = [d for d in dirs if d not in ["venv", "node_modules", ".git", "__pycache__"]]

        for file in files:
            file_path = Path(root) / file
            try:
                size = file_path.stat().st_size
                if size > 5 * 1024 * 1024:  # 5MB
                    large_files.append((file_path.relative_to(project_root), size / 1024 / 1024))
            except OSError:
                pass

    if large_files:
        for file, size_mb in large_files:
            warnings.append(f"Large file ({size_mb:.1f} MB): {file}")
    else:
        print("   ✓ No large files found")

    print()

    # Print results
    print("=" * 60)
    if errors:
        print("❌ VALIDATION FAILED")
        print()
        print("Errors:")
        for error in errors:
            print(f"  • {error}")
        print()

    if warnings:
        print("⚠️  Warnings:")
        for warning in warnings:
            print(f"  • {warning}")
        print()

    if not errors and not warnings:
        print("✅ PROJECT STRUCTURE VALID")
        print()
        print("All required directories and files present.")
        print("No structure violations detected.")
        return 0

    if errors:
        return 1
    else:
        print()
        print("Structure is valid but has minor warnings.")
        return 0


if __name__ == "__main__":
    sys.exit(validate_structure())

