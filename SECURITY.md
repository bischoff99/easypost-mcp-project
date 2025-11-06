# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

**DO NOT** open a public issue for security vulnerabilities.

Instead, email: andrejs@example.com

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

Response time: 24-48 hours

## Security Best Practices

This project follows security best practices:

- ✅ No API keys in code (use environment variables)
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ XSS prevention (React automatic escaping)
- ✅ Pre-commit hooks with security scanning (bandit)
- ✅ Dependency auditing (npm audit, pip audit)
- ✅ Rate limiting on API endpoints
- ✅ Secure headers (CORS, CSP)

## Dependencies

Regular security audits:
```bash
make audit           # Audit all dependencies
make security        # Run security scans
```

## Development Environment

- Use `.env` files (gitignored)
- Never commit secrets
- Test API keys only (EZTK* prefix)
- Production keys in secure vault

## Questions?

Contact: andrejs@example.com
