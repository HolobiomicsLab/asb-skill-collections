# The contribution loop

How using a collection turns into credit — and how credit turns into authorship on
the next citable release. This documents the end-to-end flywheel and the exact
tool at each step. Every step is open, anonymized where it touches people, and
reviewable.

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │  1. USE        an agent/human exercises a skill or workflow          │
   │  2. FIND       they spot a fix: wrong default, missing step,         │
   │                outdated tool, a better procedure                     │
   │  3. REPORT     an ANONYMIZED improvement report → a pre-filled issue │
   │  4. TRIAGE     maintainers label / discuss / request a PR            │
   │  5. REVIEW     a PR + a signed review attestation (COI-checked)      │
   │  6. CREDIT     merged work updates the contributor leaderboard       │
   │  7. AUTHORSHIP top contributors are proposed as co-authors on the    │
   │                next versioned release DOI                            │
   └───────────────────────────────┬─────────────────────────────────────┘
                                    └── back to 1 on the next release
```

## 1–2. Use & find

Skills/workflows are read where the agent runs them (`/plugin install`, `asbb
install --runtime …`, `asbb search/get`, or the MCP skill-server). When you find
something to improve, you don't need write access — go to step 3.

## 3. Report (anonymized)

Two equivalent surfaces, same scrubbing rules:

- **Web:** the [Contribute](https://holobiomicslab.github.io/asb-skill-collections/contribute.html)
  page (`docs-site/contribute.html`). Fill the form; your text is scrubbed of file
  paths, emails, IPs, and secrets **in your browser** before it builds the issue.
- **CLI / agent:** `python scripts/make_improvement_report.py --collection … --skill …
  --kind correction --summary "…" --print-url` — emits the same anonymized Markdown
  body + a pre-filled GitHub issue URL.

Both apply identical redaction (bounded, ReDoS-safe regexes; `[email]`, `[ip]`,
`[path]`, `[secret]` incl. underscore-prefixed key names and common token shapes).
The report records redaction counts for transparency. Privacy stance:
`docs/design/skill-load-telemetry.md` (no user IDs, no prompt content, no paths).

## 4–5. Triage & review

Maintainers triage `improvement` / `needs-triage` issues and shepherd a PR. A
content change lands with a **review attestation** (`collections/<slug>/v<N>/reviews/
<doi>.yaml`) — see `paper.html`'s verify flow. Conflict-of-interest is auto-checked
(`verify-coi.yml`, `governance/COI_POLICY.md`): self-review is allowed with
disclosure + a second reviewer; `self_authored_reviews` and `external_reviews` are
tracked separately and both public.

## 6. Credit (leaderboard + rank)

On merge, `career-stats-regen.yml` runs `scripts/regen_career_stats.py` to rebuild
`leaderboard/` from `contributors.jsonld` + the merged attestations:

- `career.jsonld` — all-time, with a numeric **rank** (by total reviews),
  `external_reviews`, tier, and per-collection roles.
- `annual-<year>.jsonld`, `by-domain/<slug>.jsonld` — windowed / scoped views.

These render on the site's [contributor leaderboard](https://holobiomicslab.github.io/asb-skill-collections/).
Tiers: reviewer → domain_contributor → curator → lead_curator
(`tier-update.yml`, `governance/MAINTAINERS.md`).

## 7. Authorship on the next release

When a new version is cut, `scripts/select_release_coauthors.py` turns the measured
record into a **proposed** author list (transparent, declarative policy: ORCID
required, tier gate, substantive `external_reviews`, optional recency window;
ranked "recently and over time"). `release.yml` posts this proposal to the release
job summary — **advisory only**. A maintainer reviews it and injects the agreed
authors via `select_release_coauthors.py --apply` (into `CITATION.cff` +
`.zenodo.json`, deduped by ORCID) in a normal PR before tagging.

The tagged release then mints a **new version DOI under the stable concept DOI**
(`release.yml` → Zenodo `newversion`), citing those co-authors. The loop restarts.

## Design notes

- **Nothing auto-publishes.** Improvement reports open issues you submit;
  co-authorship is proposed, never auto-written; the Zenodo deposit stays a draft
  until a maintainer publishes. Humans stay in the loop at every people-facing step.
- **Anonymization is non-negotiable** and identical across the web and CLI paths
  (single rule set, tested two-sided).
- **No contributor is named in code.** Selection runs on declarative fields from
  the leaderboard, never on identities (the `generalize-or-stop` guardrail).
