#!/usr/bin/env python3
"""Add remediation_plan section to environment-analysis-unified.json"""

import json
from pathlib import Path

# Load existing JSON
json_path = Path("/Users/andrejs/Projects/personal/easypost-mcp-project/environment-analysis-unified.json")
with open(json_path, 'r') as f:
    data = json.load(f)

# Create remediation plan
remediation_plan = {
    "summary": {
        "total_issues": 9,
        "critical": 1,
        "high": 1,
        "medium": 2,
        "low": 5,
        "estimated_time_minutes": 5,
        "disk_space_to_recover_mb": 880,
        "functional_fixes": 1,
        "cleanup_operations": 8
    },
    "script_file": "resolve_env.sh",
    "script_location": "/Users/andrejs/Projects/personal/easypost-mcp-project/resolve_env.sh",
    "config_changes": {
        "files_to_modify": [
            "~/.zshrc",
            "~/.zprofile"
        ],
        "unified_diff": """--- ~/.zshrc (original)
+++ ~/.zshrc (fixed)
@@ -5,9 +5,6 @@
 # For non-login interactive shells, ensure mise is available
-if ! command -v mise >/dev/null 2>&1 && [[ -x ~/.local/bin/mise ]]; then
-  eval "$($HOME/.local/bin/mise activate zsh)" 2>/dev/null || true
-fi

 # Note: Core PATH is set in .zprofile
 export PATH="$BUN_INSTALL/bin:$PATH"
@@ -18,9 +15,6 @@
 export OBSIDIAN_VAULT_PATH="$HOME/Developer/personal/obsidian-vault"
 export CHROMA_DOTENV_PATH="$HOME/.chroma_env"
-
-# Added by LM Studio CLI (lms)
-export PATH="$PATH:/Users/andrejs/.lmstudio/bin"
-# End of LM Studio CLI section

--- ~/.zprofile (original)
+++ ~/.zprofile (fixed)
@@ -1,7 +1,4 @@
 # macOS best practice: Set PATH here to override path_helper
-export PATH="$HOME/.local/bin:$PATH"
-
-# PostgreSQL (before Homebrew to ensure it takes precedence)
+# PostgreSQL
 export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"

 # Homebrew (this will add to PATH)
""",
        "backup_strategy": "All files backed up with .backup.YYYYMMDD_HHMMSS suffix",
        "rollback_command": "for f in ~/.zshrc ~/.zprofile; do [ -f \"$f.backup.*\" ] && cp \"$f.backup.*\" \"$f\"; done"
    },
    "actions": [
        {
            "id": "fix_pnpm",
            "phase": 1,
            "severity": "critical",
            "priority": 1,
            "title": "Fix pnpm version mismatch",
            "description": "Reinstall pnpm via mise to fix corrupted binary",
            "issue": "pnpm reports version 9.0.0 but path shows 10.20.0",
            "commands": [
                "mise uninstall pnpm",
                "mise install pnpm@latest",
                "pnpm --version  # verify correct version"
            ],
            "automated": True,
            "requires_confirmation": True,
            "estimated_time_seconds": 30,
            "risk_level": "low",
            "rollback": "mise install pnpm@9.0.0 if needed"
        },
        {
            "id": "remove_pyenv",
            "phase": 2,
            "severity": "high",
            "priority": 2,
            "title": "Remove pyenv (competing Python manager)",
            "description": "Remove pyenv and its installation directory",
            "issue": "pyenv conflicts with mise for Python management",
            "commands": [
                "brew uninstall pyenv",
                "rm -rf ~/.pyenv"
            ],
            "automated": True,
            "requires_confirmation": True,
            "estimated_time_seconds": 15,
            "disk_space_recovered_mb": 400,
            "risk_level": "medium",
            "pre_check": "Verify no critical virtual environments in ~/.pyenv/versions/",
            "rollback": "brew install pyenv && pyenv install 3.13.0"
        },
        {
            "id": "remove_nvm",
            "phase": 2,
            "severity": "medium",
            "priority": 3,
            "title": "Remove nvm directory",
            "description": "Remove unused nvm installation",
            "issue": "nvm directory present but not activated",
            "commands": [
                "rm -rf ~/.nvm"
            ],
            "automated": True,
            "requires_confirmation": True,
            "estimated_time_seconds": 5,
            "disk_space_recovered_mb": 50,
            "risk_level": "low",
            "rollback": "Reinstall nvm from https://github.com/nvm-sh/nvm"
        },
        {
            "id": "remove_homebrew_node",
            "phase": 3,
            "severity": "medium",
            "priority": 4,
            "title": "Remove Homebrew Node.js",
            "description": "Remove redundant Node.js installation from Homebrew",
            "issue": "Duplicate Node.js (mise + Homebrew)",
            "commands": [
                "brew uninstall node --ignore-dependencies"
            ],
            "automated": True,
            "requires_confirmation": True,
            "estimated_time_seconds": 10,
            "disk_space_recovered_mb": 80,
            "risk_level": "low",
            "note": "--ignore-dependencies keeps packages that depend on node, they'll use mise's node",
            "rollback": "brew install node"
        },
        {
            "id": "remove_old_python",
            "phase": 3,
            "severity": "low",
            "priority": 5,
            "title": "Remove old Homebrew Python versions",
            "description": "Remove Python 3.12 and 3.13, keep 3.14 for dependencies",
            "issue": "Multiple Homebrew Python versions wasting space",
            "commands": [
                "brew uninstall python@3.12 --ignore-dependencies",
                "brew uninstall python@3.13 --ignore-dependencies"
            ],
            "automated": True,
            "requires_confirmation": True,
            "estimated_time_seconds": 20,
            "disk_space_recovered_mb": 300,
            "risk_level": "low",
            "note": "Keep python@3.14 as some brew packages may depend on it",
            "rollback": "brew install python@3.12 python@3.13"
        },
        {
            "id": "fix_zshrc_duplicates",
            "phase": 4,
            "severity": "low",
            "priority": 6,
            "title": "Fix .zshrc duplicates",
            "description": "Remove duplicate LMStudio PATH and redundant mise activation",
            "issue": "Shell config has redundant entries",
            "commands": [
                "sed -i '.backup' '/lmstudio/d' ~/.zshrc",
                "sed -i '' '/if ! command -v mise/,/fi/d' ~/.zshrc"
            ],
            "automated": True,
            "requires_confirmation": False,
            "estimated_time_seconds": 5,
            "risk_level": "very_low",
            "note": "Backups created automatically",
            "rollback": "cp ~/.zshrc.backup ~/.zshrc"
        },
        {
            "id": "optimize_path",
            "phase": 4,
            "severity": "low",
            "priority": 7,
            "title": "Optimize PATH",
            "description": "Remove duplicate PATH entries from shell configs",
            "issue": "PATH has 3 duplicate entries",
            "commands": [
                "# PATH will be deduplicated after shell config fixes",
                "# Restart shell to apply: exec zsh"
            ],
            "automated": False,
            "requires_confirmation": False,
            "estimated_time_seconds": 0,
            "risk_level": "none",
            "note": "Automatic after fixing shell configs"
        }
    ],
    "execution_phases": [
        {
            "phase": 1,
            "name": "Critical Fixes",
            "description": "Fix functional issues that may cause immediate problems",
            "action_ids": ["fix_pnpm"],
            "can_skip": False,
            "estimated_time_seconds": 30
        },
        {
            "phase": 2,
            "name": "Remove Competing Managers",
            "description": "Remove version managers that conflict with mise",
            "action_ids": ["remove_pyenv", "remove_nvm"],
            "can_skip": False,
            "estimated_time_seconds": 20
        },
        {
            "phase": 3,
            "name": "Clean Redundant Installations",
            "description": "Remove duplicate package installations to free disk space",
            "action_ids": ["remove_homebrew_node", "remove_old_python"],
            "can_skip": True,
            "estimated_time_seconds": 30
        },
        {
            "phase": 4,
            "name": "Optimize Configuration",
            "description": "Clean up shell configuration files",
            "action_ids": ["fix_zshrc_duplicates", "optimize_path"],
            "can_skip": True,
            "estimated_time_seconds": 5
        }
    ],
    "maintenance_checklist": [
        "Run ./verify-package-managers.sh weekly to check for new conflicts",
        "Execute mise doctor monthly to check mise health",
        "Run mise upgrade && mise install monthly to update tools",
        "Check brew list --versions quarterly for redundant installations",
        "Run brew cleanup quarterly to remove old package versions",
        "Audit shell startup time: time zsh -i -c exit (should be <0.5s)",
        "Review PATH length: echo $PATH | tr ':' '\\n' | wc -l (target: <20)",
        "Monitor disk usage of package managers: du -sh ~/.local/share/mise /opt/homebrew",
        "Before installing new version managers, check if mise supports the tool",
        "Keep documentation updated: Update PACKAGE_CONFLICTS_SUMMARY.md after changes"
    ],
    "rollback_instructions": {
        "description": "Steps to undo all remediation actions",
        "prerequisites": [
            "Backup files exist (.backup.* suffix)",
            "Note which packages were removed"
        ],
        "steps": [
            "Restore shell configs: for f in ~/.zshrc ~/.zprofile; do cp $f.backup.* $f; done",
            "Reinstall pyenv: brew install pyenv && pyenv install 3.13.0",
            "Reinstall nvm: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash",
            "Reinstall Homebrew node: brew install node",
            "Reinstall old Python: brew install python@3.12 python@3.13",
            "Downgrade pnpm if needed: mise install pnpm@9.0.0",
            "Restart shell: exec zsh"
        ],
        "time_estimate_minutes": 10,
        "note": "Rollback is rarely needed but fully supported"
    },
    "verification_steps": [
        {
            "step": 1,
            "description": "Verify pnpm version",
            "command": "pnpm --version",
            "expected_output": "10.20.0 or higher"
        },
        {
            "step": 2,
            "description": "Verify pyenv removed",
            "command": "command -v pyenv || echo 'Not found (good)'",
            "expected_output": "Not found (good)"
        },
        {
            "step": 3,
            "description": "Verify nvm directory removed",
            "command": "[ -d ~/.nvm ] && echo 'Still exists' || echo 'Removed (good)'",
            "expected_output": "Removed (good)"
        },
        {
            "step": 4,
            "description": "Verify Homebrew node removed",
            "command": "brew list node 2>&1 || echo 'Not installed (good)'",
            "expected_output": "Not installed (good)"
        },
        {
            "step": 5,
            "description": "Verify old Python removed",
            "command": "brew list python@3.12 python@3.13 2>&1 || echo 'Not installed (good)'",
            "expected_output": "Not installed (good)"
        },
        {
            "step": 6,
            "description": "Verify PATH duplicates removed",
            "command": "echo $PATH | tr ':' '\\n' | sort | uniq -d | wc -l",
            "expected_output": "0"
        },
        {
            "step": 7,
            "description": "Run comprehensive verification",
            "command": "./verify-package-managers.sh",
            "expected_output": "No failures, reduced warnings"
        }
    ],
    "estimated_impact": {
        "disk_space_freed_mb": 880,
        "path_entries_before": 27,
        "path_entries_after": 24,
        "shell_startup_improvement_ms": 50,
        "conflicts_before": 9,
        "conflicts_after": 0,
        "time_to_complete_minutes": 5,
        "reboot_required": False,
        "shell_restart_required": True
    }
}

# Add remediation plan to data
data["remediation_plan"] = remediation_plan

# Write back to file
with open(json_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Added remediation_plan to {json_path}")
print(f"   Total sections: {len(data.keys())}")
print(f"   Actions: {len(remediation_plan['actions'])}")
print(f"   Phases: {len(remediation_plan['execution_phases'])}")
