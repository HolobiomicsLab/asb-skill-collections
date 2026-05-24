---
name: Propose curator candidacy
about: Apply to become a verified curator (Reviewer tier and above)
title: "[CANDIDACY] <your-github-handle>"
labels: ["curator-candidacy", "needs-vet"]
assignees: "lfnothias"
---

## Curator candidacy

> **Next step after this issue:** Open a PR adding `candidates/<your-github-handle>.yaml`.
> This issue is for discussion; the PR is what triggers automated vetting.

**GitHub handle:** @your-handle
**ORCID:** 0000-0000-0000-0000
**Intended collections:** <!-- which collection(s) you want to review -->

## Proof publications (2-3 of your own papers)

The automated vetter (`vet-curator.yml`) will check that your ORCID appears
in the author list of these papers via OpenAlex.

- DOI: 10.xxxx/your-paper-1
- DOI: 10.xxxx/your-paper-2
- DOI: 10.xxxx/your-paper-3 (optional)

## Identity check prerequisite

Before your candidacy PR is merged, please:

- [ ] Add your GitHub profile URL (`https://github.com/<your-handle>`) to your
      public ORCID record under "Websites & Social Links"
      (https://orcid.org/my-orcid?conversationId=2)
      This is the L1 identity check -- CI will verify this automatically.

## Target tier

- [ ] Reviewer (1+ reviews, L1 only)
- [ ] Domain Contributor (5-9 reviews or >=10 domain pubs, L1+L2)
- [ ] Curator (>=10 reviews + >=5 domain pubs, L1+L2)
- [ ] Lead Curator (>=30 reviews + >=20 external + >=10 pubs + h>=5 + maintainer approval, L1+L2+L3)

## Declaration

- [ ] I have read CONTRIBUTING.md and COI_POLICY.md
- [ ] I understand my ORCID will be public in contributors.jsonld
- [ ] I understand self-review requires a co-reviewer (see COI_POLICY.md)
