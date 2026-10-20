# GitHub Setup Checklist

## 1) Branch protection (manual, GitHub UI)

Repository settings > Branches > Add rule:

### Rule for `main`
- Require a pull request before merging
- Require approvals: 1
- Dismiss stale approvals when new commits are pushed
- Require status checks to pass before merging
- Required checks: `backend` (from CI workflow)
- Restrict force pushes
- Restrict deletions

### Rule for `develop`
- Require a pull request before merging
- Require status checks to pass
- Allow auto-merge (optional)

## 2) Security baseline

- Enable Dependabot alerts
- Enable secret scanning (if available)
- Add private vulnerability reporting

## 3) Collaboration baseline

- Use issue templates (added)
- Use PR template (added)
- Prefer feature branches from `develop`

## 4) Branch naming standard

- `feature/<short-topic>`
- `fix/<short-topic>`
- `chore/<short-topic>`
- `docs/<short-topic>`

## 5) Commit style

Conventional commits:
- `feat: ...`
- `fix: ...`
- `chore: ...`
- `docs: ...`
- `test: ...`

## 6) Local flow

1. Branch from `develop`
2. Implement + test
3. Open PR to `develop`
4. After validation, periodic PR from `develop` to `main`
