# Errors

Command failures and integration errors.

---
## [ERR-20260407-001] pytest

**Logged**: 2026-04-07T00:00:00+08:00
**Priority**: low
**Status**: pending
**Area**: tests

### Summary
`pytest` shell entrypoint is unavailable in PATH even though the `pytest` Python module is installed.

### Error
```
/bin/bash: line 1: pytest: command not found
```

### Context
- Command attempted: `pytest -q fusion/tests/test_merge_all_banks.py`
- Fallback: use `python3 -m pytest ...`

### Suggested Fix
Prefer `python3 -m pytest` in this workspace when invoking pytest.

### Metadata
- Reproducible: yes
- Related Files: fusion/tests/test_merge_all_banks.py

---
## [ERR-20260407-002] sudo-apt

**Logged**: 2026-04-07T00:00:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Automatic Node.js/npm installation is blocked because this WSL environment requires an interactive sudo password.

### Error
```
sudo: a password is required
```

### Context
- Command attempted: `sudo apt update`
- Trigger: `node` and `npm` were both missing

### Suggested Fix
Run the apt install commands manually in a terminal where the user can enter the sudo password, or configure passwordless sudo if appropriate.

### Metadata
- Reproducible: yes
- Related Files: DTCUP-Quiz/package.json

---
## [ERR-20260407-003] npm-install

**Logged**: 2026-04-07T00:00:00+08:00
**Priority**: medium
**Status**: pending
**Area**: frontend

### Summary
`DTCUP-Quiz` dependency installation is blocked by both an unsupported Node runtime from Ubuntu apt and a transient npm registry network reset.

### Error
```
npm WARN EBADENGINE ... vite@7.3.1 requires node '^20.19.0 || >=22.12.0'
npm ERR! code ECONNRESET
npm ERR! network request to https://registry.npmjs.org/source-map-js/-/source-map-js-1.2.1.tgz failed
```

### Context
- Command attempted: `npm install`
- Current runtime after `apt install`: Node v12.22.9, npm 8.5.1
- Project: `DTCUP-Quiz` uses Vite 7 and `@vitejs/plugin-vue` 6

### Suggested Fix
Upgrade Node to a supported major version such as 22, then retry `npm install` with network retries.

### Metadata
- Reproducible: yes
- Related Files: DTCUP-Quiz/package.json

---
