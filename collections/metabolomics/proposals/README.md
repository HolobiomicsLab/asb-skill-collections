# Proposal queue (`proposals/`)

Staging area for community **proposals** that have been triaged but not yet
shipped. Each `wave-*.yaml` is a batch collected from GitHub "Propose" issues and
normalized by a curator pass (identity / DOI / open-access resolved, category
suggested, decision recorded).

These files use the `asb-corpus/1.0` schema with every entry at `status: hold`, so
accepted entries paste directly into a release `corpus.yaml`. They are **not** part
of any release: `verify-paper.yml` only gates `status: included`.

## Lifecycle

1. A contributor opens a **Propose** issue (light template — what + link + one-line why).
2. A curator (or an automated curation pass) resolves the metadata and appends a
   normalized entry to the current `wave-*.yaml` here, with a `triage` block.
3. At the next curation wave, a maintainer reviews each entry against
   [`governance/SOURCES.md`](../../../governance/SOURCES.md) and, on accept, moves it
   into `collections/metabolomics/v2/corpus.yaml` with `status: included`.
4. The entry is removed from (or marked resolved in) the wave file.

`resource_type` distinguishes method papers from software / data-infrastructure /
tutorial proposals — the latter may be routed to a skill pack instead of the paper
corpus (a maintainer decides).
