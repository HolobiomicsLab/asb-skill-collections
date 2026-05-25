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

## Code of Conduct

We follow the Contributor Covenant v2.1. Scientific integrity and respectful review
are non-negotiable. Fabricated citations or identity fraud result in permanent banning.

## Questions

Open a GitHub Discussion or email the lead maintainer listed in `MAINTAINERS.md`.
