---
name: Propose a paper
about: Propose a paper for inclusion in an ASB-Skill collection's corpus
title: "Propose: <DOI or short title>"
labels: ["propose-paper", "needs-triage"]
---

> 📚 **Before filing:** check the inclusion criteria in
> [`governance/SOURCES.md`](../../governance/SOURCES.md) so your proposal
> self-screens. Both the scientific gate (SOURCES) and the legal/OA gate
> (CONTENT_POLICY) apply.

## Paper

- **DOI:** <!-- e.g. 10.1186/s13321-024-00878-1 -->
- **Title:** <!-- full title from the publication -->
- **Authors (first author + et al.):** <!-- e.g. "Bittremieux et al." -->
- **Venue + year:** <!-- e.g. "Journal of Cheminformatics, 2024" -->

## Target collection

- **Collection:** <!-- e.g. metabolomics -->
- **Version target:** <!-- e.g. metabolomics/v1, or "next" -->

## Access tier (self-reported, CI will verify)

- [ ] **Open-access** — explicit CC / open license
- [ ] **Hybrid** — paywalled with quotation rights (default for most journals)
- [ ] **Closed** — paywalled, no open abstract
- [ ] Don't know — let CI determine

## Rationale

<!--
Why this paper? Aim for 3-6 sentences covering:
- What domain method or tool it introduces
- Why it should be referenced for retrieval (foundational? widely-used? rare expertise?)
- What kind of agent task / benchmark it enables
- How it relates to other papers already in the corpus
-->

## Proposer

- **GitHub:** <!-- @your-handle -->
- **ORCID (optional but recommended):** <!-- 0000-0000-0000-0000 -->
- **Affiliation (optional):** <!-- e.g. "Holobiomics Lab" -->

## Conflicts of interest

- [ ] I am an author of this paper
- [ ] I am at the same institution as the lead author
- [ ] I have direct funding ties to the work
- [ ] None of the above

<!-- COI doesn't disqualify a proposal — it just gets disclosed for transparency. -->

## Checklist for the curator reviewing this proposal

(For maintainers; leave unchecked when filing.)

- [ ] DOI resolves on Crossref
- [ ] Title/authors match the DOI's Crossref record
- [ ] Access tier verified via Unpaywall
- [ ] Paper isn't already in the target collection's `corpus.yaml`
- [ ] Paper isn't retracted (Crossref retraction-watch)
- [ ] Rationale is concrete (not "would be nice to have")
- [ ] Thematic fit with the target collection
- [ ] Decision: accept / reject / defer-pending-info
