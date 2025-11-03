# Universal Slash Commands - Improvement Roadmap

**Based on:** Comprehensive Review (7.5/10 → 9.5/10 target)
**Timeline:** 8-12 weeks
**Goal:** Production-ready system for teams and enterprises

---

## 🎯 ROADMAP OVERVIEW

```
Week 1-3: Phase 1 (Security & Reliability) 🔴 CRITICAL
Week 4-5: Phase 2 (Testing & Quality) 🟡 HIGH
Week 6-7: Phase 3 (Language Expansion) 🟢 MEDIUM
Week 8-10: Phase 4 (Monitoring & UX) 🟢 MEDIUM
Week 11-12: Phase 5 (Polish & Documentation) 🟢 LOW
```

---

## 📅 PHASE 1: SECURITY & RELIABILITY (Weeks 1-3)

**Goal:** Safe for team production use
**Priority:** 🔴 CRITICAL
**Effort:** 3 weeks, 1 developer

### Week 1: Input Validation & Security

**Day 1-2: Input Validation**
- [ ] Create `validation.py` with input sanitizers
- [ ] Validate command arguments (paths, methods, names)
- [ ] Prevent command injection attacks
- [ ] Add regex pattern matching
- [ ] Test with malicious inputs

**Files to Create:**
```python
# .cursor/engine/validation.py
import re
from typing import Any, Dict

class InputValidator:
    """Validate and sanitize command inputs."""

    SAFE_PATH = r'^[a-zA-Z0-9_/.-]+$'
    SAFE_NAME = r'^[a-zA-Z0-9_-]+$'
    HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

    @staticmethod
    def validate_path(path: str) -> str:
        """Validate file path is safe."""
        if not re.match(InputValidator.SAFE_PATH, path):
            raise ValueError(f"Invalid path: {path}")
        # Prevent directory traversal
        if '..' in path:
            raise ValueError("Directory traversal not allowed")
        return path

    @staticmethod
    def validate_command_name(name: str) -> str:
        """Validate component/service name."""
        if not re.match(InputValidator.SAFE_NAME, name):
            raise ValueError(f"Invalid name: {name}")
        if len(name) > 100:
            raise ValueError("Name too long")
        return name

    @staticmethod
    def validate_http_method(method: str) -> str:
        """Validate HTTP method."""
        method = method.upper()
        if method not in InputValidator.HTTP_METHODS:
            raise ValueError(f"Invalid HTTP method: {method}")
        return method
```

**Day 3-4: Audit Logging**
- [ ] Create audit log system
- [ ] Log all command executions
- [ ] Structured JSON format
- [ ] Log rotation policy
- [ ] Query interface

**Files to Create:**
```python
# .cursor/engine/audit.py
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

class AuditLogger:
    """Audit logging for all command executions."""

    def __init__(self, log_path: str = ".cursor/audit.log"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger('audit')
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler(self.log_path)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

    def log_command(
        self,
        command: str,
        args: Dict[str, Any],
        result: Dict[str, Any],
        user: str = None,
        duration_ms: float = None
    ):
        """Log command execution."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user": user or self._get_current_user(),
            "command": command,
            "args": args,
            "result": {
                "status": result.get("status"),
                "duration_ms": duration_ms
            },
            "success": result.get("status") == "success"
        }

        self.logger.info(json.dumps(entry))

    def _get_current_user(self) -> str:
        """Get current system user."""
        import getpass
        return getpass.getuser()

    def query(self, filters: Dict[str, Any]) -> list:
        """Query audit log."""
        results = []
        with open(self.log_path) as f:
            for line in f:
                entry = json.loads(line)
                if self._matches_filters(entry, filters):
                    results.append(entry)
        return results

    def _matches_filters(self, entry: Dict, filters: Dict) -> bool:
        """Check if entry matches filters."""
        for key, value in filters.items():
            if entry.get(key) != value:
                return False
        return True
```

**Day 5: Secrets Management**
- [ ] Remove secrets from `.dev-config.json`
- [ ] Use environment variables only
- [ ] Add `.env` file support
- [ ] Document secret management

**Update `.dev-config.template.json`:**
```json
{
  "secrets": {
    "_warning": "NEVER put secrets here! Use environment variables.",
    "required": [
      "EASYPOST_API_KEY",
      "GITHUB_TOKEN",
      "CONTEXT7_API_KEY"
    ],
    "optional": [
      "AWS_ACCESS_KEY",
      "DATADOG_API_KEY"
    ]
  },
  "security": {
    "auditLog": {
      "enabled": true,
      "path": ".cursor/audit.log",
      "rotation": "daily",
      "retention": "90days"
    },
    "inputValidation": {
      "enabled": true,
      "strict": true
    }
  }
}
```

### Week 2: Reliability & Error Handling

**Day 1-2: Retry Logic**
- [ ] Create retry decorator
- [ ] Exponential backoff
- [ ] Configurable max attempts
- [ ] Per-MCP server configuration

**Files to Create:**
```python
# .cursor/engine/retry.py
import asyncio
import functools
from typing import Callable, Type

class RetryConfig:
    """Configuration for retry behavior."""
    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        exceptions: tuple = (Exception,)
    ):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.exceptions = exceptions

def retry_async(config: RetryConfig = None):
    """Async retry decorator with exponential backoff."""
    config = config or RetryConfig()

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(config.max_attempts):
                try:
                    return await func(*args, **kwargs)
                except config.exceptions as e:
                    last_exception = e

                    if attempt < config.max_attempts - 1:
                        delay = min(
                            config.initial_delay * (config.exponential_base ** attempt),
                            config.max_delay
                        )
                        print(f"Retry {attempt + 1}/{config.max_attempts} after {delay}s")
                        await asyncio.sleep(delay)

            raise last_exception

        return wrapper
    return decorator
```

**Day 3-4: Circuit Breaker**
- [ ] Implement circuit breaker pattern
- [ ] Track failure rates
- [ ] Auto-recovery
- [ ] Fallback strategies

**Files to Create:**
```python
# .cursor/engine/circuit_breaker.py
import time
from enum import Enum
from typing import Callable

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject calls
    HALF_OPEN = "half_open"  # Testing if recovered

class CircuitBreaker:
    """Circuit breaker for MCP server calls."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: Type[Exception] = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """Reset on successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        """Track failure."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to retry."""
        return (
            self.last_failure_time and
            time.time() - self.last_failure_time >= self.recovery_timeout
        )
```

**Day 5: Rollback Capability**
- [ ] Snapshot system before changes
- [ ] Rollback command
- [ ] Transaction management
- [ ] Auto-backup for destructive ops

**Files to Create:**
```python
# .cursor/engine/rollback.py
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional

class RollbackManager:
    """Manage rollback for destructive operations."""

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.backup_dir = self.workspace_root / ".cursor" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.current_snapshot = None

    def create_snapshot(self, files: List[str], operation: str) -> str:
        """Create backup snapshot before operation."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_id = f"{operation}_{timestamp}"
        snapshot_path = self.backup_dir / snapshot_id
        snapshot_path.mkdir()

        for file_path in files:
            src = self.workspace_root / file_path
            if src.exists():
                dst = snapshot_path / file_path
                dst.parent.mkdir(parents=True, exist_ok=True)

                if src.is_file():
                    shutil.copy2(src, dst)
                elif src.is_dir():
                    shutil.copytree(src, dst)

        self.current_snapshot = snapshot_id
        return snapshot_id

    def rollback(self, snapshot_id: Optional[str] = None):
        """Restore from snapshot."""
        snapshot_id = snapshot_id or self.current_snapshot
        if not snapshot_id:
            raise ValueError("No snapshot to rollback to")

        snapshot_path = self.backup_dir / snapshot_id
        if not snapshot_path.exists():
            raise ValueError(f"Snapshot not found: {snapshot_id}")

        # Restore all files
        for item in snapshot_path.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(snapshot_path)
                dst = self.workspace_root / rel_path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst)

        print(f"Rolled back to snapshot: {snapshot_id}")

    def list_snapshots(self) -> List[str]:
        """List available snapshots."""
        return [d.name for d in self.backup_dir.iterdir() if d.is_dir()]
```

### Week 3: Permissions & Dry-Run

**Day 1-2: Permission System**
- [ ] Define roles (developer, senior, admin)
- [ ] Command-level permissions
- [ ] User authentication
- [ ] Permission checks

**Update `universal-commands.json`:**
```json
{
  "permissions": {
    "roles": {
      "developer": {
        "allowed": ["test", "lint", "format", "explain", "api", "component"]
      },
      "senior": {
        "allowed": ["all", "!deploy:production"]
      },
      "admin": {
        "allowed": ["all"]
      }
    },
    "commands": {
      "deploy": {
        "production": ["admin"],
        "staging": ["senior", "admin"],
        "development": ["developer", "senior", "admin"]
      },
      "optimize": ["senior", "admin"],
      "bench": ["all"]
    }
  }
}
```

**Day 3-4: Dry-Run Mode**
- [ ] Add `--dry-run` flag
- [ ] Preview without execution
- [ ] Show estimated time/resources
- [ ] Confirm before proceed

**Day 5: Integration & Testing**
- [ ] Integration test all security features
- [ ] Performance testing with retry/circuit breaker
- [ ] Documentation update
- [ ] Security audit

---

## 📅 PHASE 2: TESTING & QUALITY (Weeks 4-5)

**Goal:** Confidence in system reliability
**Priority:** 🟡 HIGH
**Effort:** 2 weeks

### Week 4: Core Testing

- [ ] Unit tests for validation
- [ ] Unit tests for retry logic
- [ ] Unit tests for circuit breaker
- [ ] Unit tests for audit logging
- [ ] Integration tests for MCP chains
- [ ] Target: 80%+ coverage

### Week 5: Schema & Validation

- [ ] JSON schema for universal-commands.json
- [ ] JSON schema for .dev-config.json
- [ ] Config validator CLI tool
- [ ] Command linter
- [ ] Smoke test suite

---

## 📅 PHASE 3-5 (Abbreviated)

See full roadmap in COMPREHENSIVE_REVIEW.md

---

## 🎯 QUICK WINS (This Week)

### Priority 1: Input Validation (Day 1)
Copy the `validation.py` code above and add to all commands.

### Priority 2: Audit Logging (Day 1)
Copy the `audit.py` code and integrate.

### Priority 3: Dry-Run Flag (Day 2)
Add `--dry-run` support to all commands.

### Priority 4: Schema Validation (Day 2)
Validate `.dev-config.json` on startup.

---

## 📊 SUCCESS METRICS

| Phase | Target Score | Key Metrics |
|-------|--------------|-------------|
| Current | 7.5/10 | Good MVP |
| Phase 1 | 8.5/10 | Security ✅, Reliability ✅ |
| Phase 2 | 9.0/10 | Testing ✅, Quality ✅ |
| Phase 3 | 9.2/10 | More languages ✅ |
| Phase 4 | 9.5/10 | UX ✅, Monitoring ✅ |
| Phase 5 | 9.7/10 | Polish ✅, Enterprise-ready ✅ |

---

## 🚀 GET STARTED

```bash
# 1. Create engine directory
mkdir -p .cursor/engine

# 2. Add validation module
# Copy validation.py code above

# 3. Add audit logging
# Copy audit.py code above

# 4. Add retry logic
# Copy retry.py code above

# 5. Test it
/test backend/tests/ --dry-run
```

---

**Roadmap Version:** 1.0
**Created:** 2025-11-03
**Next Review:** After Phase 1 completion

