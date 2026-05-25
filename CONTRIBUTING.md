# Contributing to ASB-Skill-Collections

We welcome community contributions of curated, evidence-grounded scientific skills,
tools, and benchmarks. All contributions are reviewed for scientific quality,
evidence provenance, and FAIR metadata completeness.

## How to contribute a review

1. **Prerequisites:** You must be listed in `contributors.jsonld` with at least
   Reviewer tier. If you are not yet listed, complete Step 0 below first.

2. **Open a PR** adding your review attestation at
   `collections/<slug>/v<N>/reviews/<paper-doi-slug>.yaml`.
   Use `templates/attestation.yaml.template` as your starting point.

3. **CI runs automatically:**
   - COI detection via `verify-coi.yml`
   - Schema validation via `validate.yml`
   - If `is_coauthor: true`, you must also add a `co_reviewer` block (see COI_POLICY.md)

4. **A maintainer merges** your PR. You cannot self-merge.

5. **Tier update happens automatically** via `tier-update.yml` on merge.

## Step 0 — Become a verified contributor (Reviewer tier)

1. **Open a PR** adding `candidates/<your-github-handle>.yaml`.
   Use this format:

   ```yaml
   github: your-github-handle
   orcid: "0000-0000-0000-0000"
   intended_collections: [metabolomics]   # one or more slugs
   proof_publications:
     - doi: 10.xxxx/your-paper-1
     - doi: 10.xxxx/your-paper-2
   ```

2. **Add your GitHub URL to your ORCID public profile** (Websites & Social Links).
   This is the L1 identity check.

3. **CI runs `vet-curator.yml`** automatically:
   - L1: GitHub URL found in ORCID public record
   - L2: ORCID matches author on each `proof_publications` DOI (via OpenAlex)

4. **A maintainer merges** your candidacy PR, adding you to `contributors.jsonld`.

## How to propose a new collection

1. Open a GitHub Issue using the "Propose collection" template.
2. Include: domain name, short description, 3-5 seed papers (DOIs), proposed Lead Curator.
3. After maintainer go-ahead, open a PR adding `staged-collections/<domain>/v1/`.

## Tier progression

| Tier | Requirement |
|---|---|
| Reviewer | 1+ reviews, L1 identity verified |
| Domain Contributor | 5-9 reviews OR >=10 domain pubs (verified L1+L2) |
| Curator | >=10 reviews + >=5 domain pubs (L1+L2) |
| Lead Curator | >=30 reviews (>=20 external) + >=10 domain pubs + h-index >=5 + maintainer approval |

Tiers are per-collection-release. Career totals are tracked in `leaderboard/career.jsonld`.

## How the ASB pipeline runs (local-only for now)

AgenticScienceBuilder (the agent that consumes papers and produces skills /
tools / capsules / workflows) **runs only on a maintainer's machine** — not
in CI. The asb-skill-collections workflows are validation + plumbing only:

| Workflow | Trigger | What it does |
|---|---|---|
| `validate.yml` | every PR + push | LinkML/structural checks, description lint, DOI resolve, EDAM IRI check |
| `verify-paper.yml` | PRs touching `corpus.yaml` | Crossref retraction check + Unpaywall access tier verification |
| `release.yml` | tag `<slug>-v<N>` | pytest → regen catalogue → Zenodo deposit → CITATION.{cff,bib} DOI patch → HF mirror trigger |
| `mirror-to-hf.yml` | release tag | Pushes the collection to HuggingFace |
| `pages.yml` | push to main | Rebuilds the static docs site |

What this means for contributors:

- A "Propose paper" PR adds the paper to `corpus.yaml` with `status: proposed`.
- After Lead Curator + maintainer approval, the status flips to `accepted`.
- A maintainer then runs `asb build` + `asb collection promote` locally and
  opens a **follow-up PR** with the derived `skills/<slug>/SKILL.md`,
  `tools/<slug>.yaml`, `benchmark/tasks/<paper>/`, and the
  `corpus.yaml`-status transition to `included`. This is reviewed by the
  Lead Curator before merge.
- Once merged, a tag triggers the Zenodo deposition + HF mirror via CI.

**Why local-only:** the ASB pipeline calls LLMs (~$0.10–$0.35 per paper at
economy tier) and depends on a reachable Perspicacité MCP server (currently
not deployed publicly because the Chroma vector store is single-writer).
Moving to hosted execution is tracked as a v1.1+ improvement and requires
(a) `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` configured as repo secrets with
cost guardrails, (b) public Perspicacité MCP endpoint, (c) `actions/cache`
wiring for the PDF / figure / LLM response caches.

## Budget-tier LLM mode for cost-constrained contributors

The default ASB pipeline runs at **economy tier** (~$0.10-$0.35 per paper),
which uses Sonnet for outline-level reasoning and Haiku for card-level
extraction. For contributors at lower-resource institutions, or for
first-pass dogfooding before committing real review time, this can still
be a barrier. We support a **budget tier** that brings per-paper cost down
to ~$0.02-$0.05.

### Invocation

```bash
asb build <paper-doi> --llm-tier=budget
asb collection promote <slug> --llm-tier=budget
```

The `--llm-tier=budget` flag is the intended interface. If your local
`asb` build does not yet expose it, see `docs/cli_reference.md` for the
current status and any environment-variable equivalents.

### Models used

| Agent | Economy tier (default) | Budget tier |
|---|---|---|
| Outline / decomposition | Sonnet | `openai/gpt-4o-mini` |
| Card extraction | Haiku | `openai/gpt-4o-mini` |
| Claim extraction | Haiku | `openai/gpt-4o-mini` |
| Description rewrite (discipline pass) | Haiku | Haiku — unchanged |

Budget tier uses one model (`openai/gpt-4o-mini`) for every agent except
the description-rewrite step, which stays on Haiku because consistency of
the EDAM-conformant skill descriptions is non-negotiable for the
collection's quality contract.

### Quality tradeoffs (observed, indicative)

- **Decomposition quality drops ~10-20%.** Budget tier produces fewer
  cards per paper and is more likely to merge distinct sub-methods into a
  single card.
- **Claim extraction quality drops more.** Both precision and recall
  decline noticeably. Budget-tier claim sets should be treated as a
  starting point for human curation, not as a final artifact.
- **Description discipline holds.** The rewrite step is identical
  between tiers, so the EDAM-aligned descriptions still pass the
  description linter.

### Acceptable use cases

- **First-pass dogfooding** before requesting Lead Curator review — get
  a sense of what the pipeline will produce, find obvious problems,
  iterate locally without burning a higher-tier budget.
- **Reviewer attestation work** that does **not** regenerate derived
  content — verifying an existing economy-tier artifact does not require
  re-running the pipeline at all, and budget tier is fine for any
  ancillary regeneration during review.
- **Educational and demonstration runs** — teaching how the pipeline
  works, showing a class, or producing reproducible examples for
  documentation.

### Quality gates

- Budget-tier outputs are flagged in the build manifest
  (`build_manifest.yaml`) with `tier: budget` on every derived artifact.
- The Lead Curator **must explicitly re-promote** budget-tier artifacts
  with `--llm-tier=economy` (or higher) before any `<slug>-v<N>` tag is
  cut. `release.yml` refuses to deposit a release whose manifest contains
  any `tier: budget` artifact.
- Reviewer attestations against budget-tier artifacts are allowed during
  staging review, but the artifacts they attest to must be re-derived at
  economy tier before release. The attestation is re-checked against the
  re-derived artifact; if the re-derivation changes the artifact
  materially, the attestation is invalidated and a fresh review is
  required.

### Cost ceiling

| Tier | Estimated cost / paper |
|---|---|
| Budget | $0.02 - $0.05 |
| Economy (default) | $0.10 - $0.35 |
| Premium (Opus everywhere, not used in routine builds) | $1 - $3 |

These numbers are indicative as of 2026 model pricing and will drift; the
flag itself is stable.

## Code of Conduct

We follow the Contributor Covenant v2.1. Scientific integrity and respectful review
are non-negotiable. Fabricated citations or identity fraud result in permanent banning.

## Questions

Open a GitHub Discussion or email the lead maintainer listed in `MAINTAINERS.md`.
