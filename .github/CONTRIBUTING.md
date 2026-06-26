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

## Propose or annotate a paper

ASB-Skills are distilled from peer-reviewed **method papers**. Before proposing,
skim the inclusion criteria in [`governance/SOURCES.md`](../governance/SOURCES.md)
so your suggestion self-screens. Anyone may suggest or annotate a paper; **a
maintainer always makes the final merge decision** (you cannot self-merge), and
COI/tier rules are unchanged.

There are three ways to contribute a paper:

### 1. Suggest via an issue (lightest)

Open a **Propose a paper, tool, or resource** issue using the
[`propose-paper`](ISSUE_TEMPLATE/propose-paper.md) template. Keep it short — just
what it is, a link (DOI, repo, or homepage), and a one-line rationale. A curator (or
the automated curation pass) then resolves the rest: DOI on Crossref, access via
Unpaywall, dedup against the collection's `corpus.yaml`, retraction check, category,
and thematic fit. Triaged proposals are staged in
`collections/<slug>/proposals/wave-*.yaml` (`status: hold`); at the next wave a
maintainer moves accepted entries into `collections/<slug>/v<N>/corpus.yaml` with
`status: included`.

### 2. Suggest via a pull request (Enveda-style, low-friction)

Prefer a PR? Add the paper directly to the target
`collections/<slug>/v<N>/corpus.yaml` under `papers:`, using the
`asb-corpus/1.0` schema, with `status: hold` (pending curator review):

```yaml
- name: ToolOrMethodName
  doi: 10.xxxx/xxxxx
  title: Full paper title
  category: <category from the review-series taxonomy>
  repo_url: owner/repo            # or full URL to code/data
  status: hold                    # maintainer flips to "included" after review
  wave: <curation batch — maintainer-assigned>
  access:
    type: gold-oa                 # CI (verify-paper.yml) verifies this
    is_oa: true
```

On the PR, `verify-paper.yml` checks access/OA and `validate.yml` checks the
schema. A maintainer reviews scientific fit against
[`governance/SOURCES.md`](../governance/SOURCES.md) and merges, flipping
`status` to `included`.

### 3. Annotate an existing or proposed paper

Improve a paper already in (or proposed to) the corpus by either:
- a small PR editing that paper's `corpus.yaml` entry, or
- a structured comment on the open `propose-paper` issue.

**Annotatable fields:** `category` (refine to the review-series taxonomy),
`repo_url`, and free-text rationale/fit/tags. **Not annotatable** (maintainer/CI-
owned): `doi`, the `access` block, and `status` — these are set by verification
and curation, not by annotation.

## Propose a skill (community tier)

Beyond papers, you can contribute a **skill** directly — a community-tier skill is
one curated outside the literature pipeline (`provenance_tier: community`). It is
held to the **same structural discipline** as a published skill, but is not required
to derive from a paper. See
[`governance/COMMUNITY_SKILLS.md`](../governance/COMMUNITY_SKILLS.md) for the full
curation model and [`governance/PROVENANCE_TIERS.md`](../governance/PROVENANCE_TIERS.md)
for the `community` tier. As with everything else, **a maintainer makes the final
merge decision** — you cannot self-merge.

There are two ways in:

### 1. Suggest via an issue (lightest)

Open a **Propose a skill (community tier)** issue using the
[`propose-skill`](ISSUE_TEMPLATE/propose-skill.md) template. Tell us what the skill
does, why it matters, and link it (or paste its `SKILL.md`). The issue template asks
you to confirm you license your skill prose under **CC-BY-4.0**.

### 2. Stage a proposal PR with the `propose-skill` command (recommended)

Run the `propose-skill` command
([`collections/metabolomics/v2/commands/propose-skill.md`](../collections/metabolomics/v2/commands/propose-skill.md))
on your local `SKILL.md`. It will:

- **normalize** the frontmatter to the CI gates (description prefix/length, no
  marketing terms, canonical EDAM IRIs, a valid `license_tier`);
- **match** it against the collection to suggest `related_skills` + `tools_used`,
  and **warn** if it looks like a near-duplicate (annotate/merge instead of adding a
  copy);
- best-effort **ground** it (Perspicacité, optional — community skills need no DOI);
- tier it `community` / `hold` and **stage** the files via
  `scripts/propose_skill.py`:
  - `collections/<slug>/v<N>/proposals/skills/<skill-slug>/SKILL.md`
  - `collections/<slug>/v<N>/proposals/wave-skills-<date>.yaml` (ledger,
    `asb-skill-proposals/1.0`).

The command **never opens the PR for you** — it prints the exact
`git`/`gh pr create` commands for you to review and run yourself. On the PR, the
**Proposals gate** (`scripts/check_proposals.py` in `validate.yml`) checks the staged
skill against the same discipline as a published one, and the
[pull-request template](PULL_REQUEST_TEMPLATE.md) asks you to confirm the CC-BY-4.0
grant on your skill prose. A maintainer then reviews fit and merges; accepted skills
are promoted out of `proposals/` into the shipped collection at a curation wave.

## Claim/contribute a skill for your tool (become a co-author)

If you are an **author of the tool (or method/paper)** a skill grounds on, you can
contribute that skill **and be credited as a verified co-author**. This is the
community-tier path above, plus an attribution layer: your identity is verified and
your credit surfaces in `contributors.jsonld`, the merge commit's `Co-authored-by:`
trailer, and (at release) `CITATION.cff`. See
[`governance/AUTHORSHIP.md`](../governance/AUTHORSHIP.md) for the full model.

1. **Open a "Claim / contribute a skill for your tool" issue** using the
   [`claim-skill`](ISSUE_TEMPLATE/claim-skill.md) template. Tell us the skill, the
   tool/method and its **paper DOI**, and **who you are** — name, ORCID, GitHub, and
   the email you want on the `Co-authored-by:` trailer.

2. **Verified authorship.** Your authorship is **identity-verified** before any
   credit, using the same checks as curator candidacy (`vet-curator`): **L1** (your
   GitHub URL is in your ORCID public profile) and **L2** (your ORCID is an author on
   the tool's paper DOI, via OpenAlex). If you are not yet in `contributors.jsonld`,
   complete **Step 0** above first — your authorship is credited once that lands.

3. **A maintainer runs the `claim-skill` command**
   ([`collections/metabolomics/v2/commands/claim-skill.md`](../collections/metabolomics/v2/commands/claim-skill.md)).
   It reuses the `propose-skill` flow (normalize → match → ground → stage), writes you
   into the staged skill's `contributors` as `role: author`, and prepares a PR with a
   `Co-authored-by: <you>` trailer, `Closes #<issue>`, and **you requested as a
   reviewer** of your own contribution.

4. **Conflict of interest is disclosed, not disqualifying.** Authoring a skill for
   your own tool and reviewing it yourself is a self-review — disclosed on the issue
   and PR (exactly like a co-authored paper review under
   [`governance/COI_POLICY.md`](../governance/COI_POLICY.md)). The independent gate is
   the **merging maintainer**, who must be a *different* person. **You cannot
   self-merge.**

5. **On merge, your credit is recorded** via the author-credit path of
   `scripts/tier_update.py` (`--credit-author` increments `asb:authored_skills` and
   re-evaluates your tier — it never downgrades an already-higher tier).

## Tier progression

| Tier | Requirement |
|---|---|
| Reviewer | 1+ reviews, L1 identity verified |
| Domain Contributor | 5-9 reviews OR >=10 domain pubs (verified L1+L2) |
| Curator | >=10 reviews + >=5 domain pubs (L1+L2) |
| Lead Curator | >=30 reviews (>=20 external) + >=10 domain pubs + h-index >=5 + maintainer approval |

Tiers are per-collection-release. Career totals are tracked in `leaderboard/career.jsonld`.

## Code of Conduct

We follow the Contributor Covenant v2.1. Scientific integrity and respectful review
are non-negotiable. Fabricated citations or identity fraud result in permanent banning.

## Questions

Open a GitHub Discussion or email the lead maintainer listed in `MAINTAINERS.md`.
