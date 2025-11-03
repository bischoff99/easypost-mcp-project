Generate comprehensive tests for: {{file_path}}

Read .dev-config.json for:
- Backend: pytest + pytest-xdist (16 workers)
- Frontend: Vitest (20 threads)
- Coverage: 80% backend, 70% frontend

Generate:
1. Test file with fixtures/setup
2. Happy path tests
3. Edge cases and error handling
4. Validation tests
5. Mock external dependencies
6. Configure for parallel execution (pytest -n 16 or vitest maxThreads=20)

Include run commands at bottom of file.