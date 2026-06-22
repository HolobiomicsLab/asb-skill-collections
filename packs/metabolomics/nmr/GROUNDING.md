# Grounding — nmr

Every skill here is distilled from one peer-reviewed paper (`derived_from` DOI in its SKILL.md frontmatter). Grounding is **optional** — skills work without it.

Two backends (KB-primary, local fallback):

- **kb (Perspicacité):** RAG over full text + SI, persistent, citable. Needs a server at `PERSPICACITE_BASE` (default http://127.0.0.1:8000). First use auto-creates + ingests the `asb-paper-<doi>` KB.
- **local (serverless):** `git clone` the source repo + best-effort OA paper fetch; read files directly. No server.

Use `/ground [skill|doi] [question]`, or call `bin/perspicacite_kb_bind.py` (`query` / `local`) directly.
