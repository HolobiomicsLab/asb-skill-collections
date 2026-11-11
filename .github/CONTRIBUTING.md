# Contributing to ASB-Skill-Collections

We welcome community contributions of curated, evidence-grounded scientific skills,
tools, and benchmarks. All contributions are reviewed for scientific quality,
evidence provenance, and FAIR metadata completeness.

## Four routes

Whoever meets a skill, a person or an agent, has the same four routes. Each is an
issue on the tracker of this public repository,
<https://github.com/HolobiomicsLab/asb-skill-collections/issues>.

| Route | Where | What happens next |
|---|---|---|
| 1. This skill is wrong or could be better | [skill feedback](https://github.com/HolobiomicsLab/asb-skill-collections/issues/new?template=1-skill-feedback.md), the [contribute page](https://holobiomicslab.github.io/asb-skill-collections/contribute.html), or `asbb report skill` | A maintainer triages it, fixes the skill in the domain repository and the revision ships in a later release |
| 2. A skill is missing: request it, or propose yours | [request a skill](https://github.com/HolobiomicsLab/asb-skill-collections/issues/new?template=2-request-skill.md), or [propose your skill](https://github.com/HolobiomicsLab/asb-skill-collections/issues/new?template=propose-skill.md) | A curator looks for a method paper or a workflow, or stages your skill for review |
| 3. A paper is not referenced: propose it | [propose a paper](https://github.com/HolobiomicsLab/asb-skill-collections/issues/new?template=3-propose-paper.md) or the [paper form](https://holobiomicslab.github.io/asb-skill-collections/propose.html) | A curator checks fit and access and stages it for the next curation wave |
| 4. Something technical failed: report it | [technical fault](https://github.com/HolobiomicsLab/asb-skill-collections/issues/new?template=4-technical-fault.md) (install, plugin, search, CLI, MCP server, site, gates) | A maintainer reproduces and fixes it in the tooling |

Agents draft these reports with the router of a collection, `asbb report` or
`scripts/skill_feedback.py`: they show you the exact text and post only on your
explicit yes. Nothing is sent otherwise.

Released collections live in private domain repositories `asb-skills-<domain>`
(registry: `collections.yaml`). A member of the public cannot open an issue or a
pull request there, so every contribution goes through an issue on this public
repository, and a maintainer carries it into the domain repository. This
repository holds the tooling, governance and registry. Every `collections/…` and
`staged-collections/…` path below is a path in the domain checkout.

## How to contribute a review

1. **Prerequisites:** You must be listed in `contributors.jsonld` with at least
   Reviewer tier. If you are not yet listed, complete Step 0 below first.

2. **Open a review request issue** with the
   [`request-paper-review`](ISSUE_TEMPLATE/request-paper-review.md) template and
   paste your review attestation in it, written from
   `templates/attestation.yaml.template`. A maintainer commits it to
   `<domain checkout>/collections/<slug>/v<N>/reviews/<paper-doi-slug>.yaml` in
   the domain repository.

3. **Checks:** a maintainer runs the COI check (`scripts/check_coi.py`) and the
   domain repository's content gates (`domain-gates.yml`, called from its
   `gates.yml`). If `is_coauthor: true`, you must also add a `co_reviewer` block
   (see `governance/COI_POLICY.md`).

4. **A maintainer records** your attestation. You cannot record your own.

5. **Tier update:** a maintainer runs `scripts/tier_update.py` after the merge.

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
3. After maintainer go-ahead, a maintainer adds `<domain checkout>/staged-collections/<domain>/v1/` in the domain repository.

## Propose or annotate a paper

ASB-Skills are distilled from peer-reviewed **method papers**. Before proposing,
skim the inclusion criteria in [`governance/SOURCES.md`](../governance/SOURCES.md)
so your suggestion self-screens. Anyone may suggest or annotate a paper; **a
maintainer always makes the final merge decision** (you cannot self-merge), and
COI/tier rules are unchanged.

There are three ways to contribute a paper, all through this public repository:

### 1. Suggest via an issue (lightest)

Open a **Propose a paper, tool, or resource** issue using the
[`propose-paper`](ISSUE_TEMPLATE/3-propose-paper.md) template, or the
[paper form](https://holobiomicslab.github.io/asb-skill-collections/propose.html)
of the site, which writes the same fields. Keep it short — just
what it is, a link (DOI, repo, or homepage), and a one-line rationale. A curator (or
the automated curation pass) then resolves the rest: DOI on Crossref, access via
Unpaywall, dedup against the collection's `corpus.yaml`, retraction check, category,
and thematic fit. Triaged proposals are staged in
`<domain checkout>/collections/<slug>/proposals/wave-*.yaml` (`status: hold`); at the next wave a
maintainer moves accepted entries into `<domain checkout>/collections/<slug>/v<N>/corpus.yaml` with
`status: included`.

### 2. Suggest a ready corpus entry

Have the full entry? Paste it into the `propose-paper` issue, in the
`asb-corpus/1.0` schema of `<domain checkout>/collections/<slug>/v<N>/corpus.yaml`,
with `status: hold` (pending curator review):

```yaml
- name: ToolOrMethodName
  doi: 10.xxxx/xxxxx
  title: Full paper title
  category: <category from the review-series taxonomy>
  repo_url: owner/repo            # or full URL to code/data
  status: hold                    # maintainer flips to "included" after review
  wave: <curation batch — maintainer-assigned>
  access:
    type: gold-oa                 # a maintainer verifies this
    is_oa: true
```

A maintainer adds it to the domain repository, where its content gates check the
schema; the maintainer checks access and scientific fit against
[`governance/SOURCES.md`](../governance/SOURCES.md) and flips `status` to
`included`.

### 3. Annotate an existing or proposed paper

Improve a paper already in (or proposed to) the corpus with a structured comment
on its open `propose-paper` issue, or a new `propose-paper` issue that names the
paper and the change. A maintainer edits the `corpus.yaml` entry in the domain
repository.

**Annotatable fields:** `category` (refine to the review-series taxonomy),
`repo_url`, and free-text rationale/fit/tags. **Not annotatable** (maintainer/CI-
owned): `doi`, the `access` block, and `status` — these are set by verification
and curation, not by annotation.

## Propose a super-skill (composite workflow)

A **super-skill** is an end-to-end *composite workflow* — an ordered DAG of
**existing leaf skills** (e.g. `mzML → annotation`). It reuses leaves; it does not
add new ones (to add a new tool/paper, use the paper paths above). It is generated
from a short **skeleton** by the ASB factory, not hand-written.

1. Open a **Propose a super-skill** issue using the
   [`propose-superskill`](ISSUE_TEMPLATE/propose-superskill.md) template: name,
   end-to-end goal, target collection, and the **stages** (each stage's goal plus
   the preferred leaf skill slugs from `skills_index.json`).
2. A curator runs the checklist (every leaf slug resolves; stages form a valid
   DAG; no leaf in two stages; scientific ordering sound; not a duplicate).
3. On go-ahead, the skeleton lands in the **framework** repo
   (`HolobiomicsLab/AgenticScienceBuilder`) at
   `scripts/skeletons/<collection>/<slug>.yaml`. A maintainer generates the workflow
   there with `scripts/compose_workflows.py` — maintainer-only, because the semantic
   binding needs an `OPENAI_API_KEY` and the prebuilt embedding cache — and it must
   pass `validate_workflows.py` in *this* repo before promotion into the collection's
   `workflows/`. The 20 workflows of the metabolomics v3 collection were
   produced this way.

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

Open an issue with the `question` label, or email the lead maintainer listed in
`governance/MAINTAINERS.md`. Discussions are not enabled on this repository.
