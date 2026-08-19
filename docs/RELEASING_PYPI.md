# Releasing `asb-skill-collections` to PyPI

This is the **Python distribution** release (the `asbb` CLI + the `asb-mcp`
server). It is separate from a *collection* release (`release.yml` → Zenodo /
HuggingFace on `<slug>-v<N>` tags). The distribution name is
**`asb-skill-collections`**; it installs the `asb_skill_collections` package and
two console scripts (`asbb`, `asb-mcp`). (The repo's `scripts/` directory holds
path-invoked CI/dev tools and is intentionally not part of the wheel.)

> The wheel is tiny (~110 KB — just `scripts/`). It does **not** bundle the skill
> corpus; the CLI reads collections from a checkout / `ASB_COLLECTIONS_ROOT` /
> `--repo` at run time. The sdist is constrained in `pyproject.toml` so it stays
> small too.

There are three ways the package can be published. Pick based on where you are:

| Path | Auth | When |
| --- | --- | --- |
| **A. From the repo (recommended)** | Trusted Publishing (OIDC, no token) | normal releases |
| **B. From your computer** | API token (`uv publish`) | first publish / hotfix / offline |
| **C. TestPyPI dry run** | trusted or token | validate before real PyPI |

---

## One-time setup

### Bump the version
Edit `version` in `pyproject.toml` (currently `0.2.0`). PyPI refuses to overwrite
an existing version — every publish needs a new number.

### A. Configure Trusted Publishing (do this once, no secrets stored)
Trusted Publishing lets GitHub Actions upload **without any API token**. It works
even before the project exists on PyPI ("pending publisher").

1. Sign in at <https://pypi.org/manage/account/publishing/> → **Add a pending publisher**.
2. Fill in:
   - **PyPI Project Name:** `asb-skill-collections`
   - **Owner:** `HolobiomicsLab`
   - **Repository name:** `asb-skill-collections`
   - **Workflow name:** `publish-pypi.yml`
   - **Environment name:** `pypi`
3. Repeat at <https://test.pypi.org/manage/account/publishing/> with
   **Environment name:** `testpypi` (for the dry-run path).
4. In the GitHub repo → **Settings → Environments**, create environments named
   `pypi` and `testpypi` (optionally add required reviewers on `pypi` so a human
   approves each real release).

That's it — no `PYPI_TOKEN` secret is ever added to the repo.

### B. Configure a local token (only for publishing from your computer)
1. <https://pypi.org/manage/account/token/> → create a token. For the **first**
   upload (project doesn't exist yet) use an **account-scoped** token; afterwards
   replace it with a **project-scoped** `asb-skill-collections` token.
2. Add it to `~/.zshrc` (your preferred plain-export style):
   ```bash
   export UV_PUBLISH_TOKEN="pypi-AgEN...your-token..."
   # optional, for TestPyPI dry runs:
   export TEST_PYPI_TOKEN="pypi-AgEN...your-testpypi-token..."
   ```
   `then exec zsh` (or open a new shell) to load them. The token value is a
   secret — never commit it or paste it into the repo.

---

## Releasing

### Path A — from the repo (recommended)
The whole flow is a GitHub Release; CI builds, checks, and publishes via OIDC.

```bash
# from a clean main with the new version committed:
git tag v0.2.0
git push origin v0.2.0
gh release create v0.2.0 --title "asb-skill-collections 0.2.0" --generate-notes
```

Publishing the GitHub Release fires `publish-pypi.yml` → real PyPI. Watch it:
```bash
gh run watch
```
> Note: `v0.2.0` is the **package** tag. It will NOT trigger the collection
> release (`release.yml` only matches `<slug>-v<N>`, e.g. `metabolomics-v0.2.0`).

### Path B — from your computer
```bash
uv build                     # -> dist/asb_skill_collections-<ver>-py3-none-any.whl + .tar.gz
uvx twine check dist/*       # metadata sanity check
uv publish                   # reads UV_PUBLISH_TOKEN; uploads to real PyPI
```

### Path C — TestPyPI dry run (do this before your first real publish)
Repo:
```bash
gh workflow run publish-pypi.yml -f target=testpypi
gh run watch
```
Local:
```bash
uv build
uv publish --publish-url https://test.pypi.org/legacy/ --token "$TEST_PYPI_TOKEN"
```
Then verify a clean install from TestPyPI:
```bash
uvx --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    --from asb-skill-collections asbb --help
```

---

## After publishing — verify
```bash
uvx --from asb-skill-collections asbb --help
uvx --from "asb-skill-collections[mcp]" asb-mcp --help    # MCP server entry
pip index versions asb-skill-collections                  # confirms the new version is live
```

## Using it from a dev hub / another environment
Once on PyPI it's installable anywhere — no checkout required for the tooling:

```bash
pipx install asb-skill-collections                  # global `asbb` / `asb-mcp`
uv add asb-skill-collections                         # as a project dependency
uvx --from asb-skill-collections asbb search "<q>" --collection metabolomics
```

Wire the MCP server into any hub's MCP config (Claude Desktop/Code, Cursor,
Cline, Codex…):
```jsonc
{
  "asb-skills": {
    "command": "uvx",
    "args": ["--from", "asb-skill-collections[mcp]", "asb-mcp"],
    "env": { "ASB_COLLECTIONS_ROOT": "/path/to/asb-skill-collections" }
  }
}
```
The CLI/MCP tooling ships via PyPI; the **skill corpus** still comes from a
checkout (or `ASB_COLLECTIONS_ROOT`) — that separation keeps the package small
and lets the corpus update independently of the tool.

## Mistakes & recovery
- **Wrong/broken upload:** you cannot re-upload the same version. Bump the patch
  version and publish again. `pip`/`uv` will pick the newer one.
- **`yank`** a bad release on the PyPI project page to stop new installs while
  keeping it resolvable for anyone already pinned to it.
- **Name squat protection:** the names `asb-skill-collections`, `asbb`, and
  `asb-mcp` were all free as of 2026-06-29; publishing claims `asb-skill-collections`.
