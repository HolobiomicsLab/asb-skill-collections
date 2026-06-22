---
name: Request review for paper [DOI]
about: Nominate a paper in a collection for expert review. Opens the public review-request triage loop (§9.7).
title: "[REVIEW-REQUEST] <Paper Title or DOI>"
labels: ["review-requested", "needs-triage"]
---

## Paper information

**Paper DOI:** 
<!-- e.g., 10.1038/s41592-020-00891-6 -->

**Paper title:**
<!-- The full title of the paper -->

**Link to paper (optional):**
<!-- e.g., https://doi.org/10.xxxx/... -->

## Paper classification

**Which omics domain does this paper address?**
- [ ] Metabolomics
- [ ] Epigenomics
- [ ] Transcriptomics
- [ ] Other (please specify):

**Open-access status (required):**
- [ ] Fully open access (CC-BY, CC-0, or equivalent permissive license)
- [ ] Open access (PubMed Central, author-deposited preprint, etc.)
- [ ] Paywalled / restricted access
- [ ] Unknown (I've flagged this for triage)

> **Note:** v0 ASB-Skills collections admit **open-access sources only** (per §4 / POLICY-content.md). If you're nominating a paywalled paper, the maintainer may defer it to a post-v0 closed-access review gate.

## Proposed skills / claims from this paper

**What skills, workflows, or verifiable claims could be extracted from this paper?** (free text, 2-4 examples)

<!-- e.g., "Feature detection using GNPS library matching (section 2.1)", "Molecular networking for spectral similarity clustering (section 3)", "Statistical power calculation for untargeted metabolomics (supplementary)" -->

---

## Review demand signal

**Is there an active collection that would benefit from reviewing this paper?** (optional)

- [ ] Metabolomics (if chosen above)
- [ ] Epigenomics (if chosen above)
- [ ] Transcriptomics (if chosen above)
- [ ] I'm uncertain which collection this belongs to

**If you are a potential reviewer, declare your interest here:**

- [ ] I am willing to review this paper
- [ ] I am not a reviewer but nominating this for someone else

### Reviewer self-nomination (optional)

If you'd like to claim this review yourself, provide:

**Your GitHub username:**

**Your ORCID:**
<!-- Enter your real ORCID. The literal 0000-0000-0000-0000 here is a PLACEHOLDER
     (templates in this repo use 0000-0000-0000-0000 as the placeholder ORCID) —
     replace it with your real ORCID. Required to write a review in this repo.
     See CONTRIBUTING.md Step 0 if not yet verified. -->

**Are you a co-author of this paper?**
- [ ] Yes
- [ ] No
- [ ] Uncertain

> If yes, an independent co-reviewer (non-coauthor) is the **v1** target for COI handling (see COI_POLICY.md Safeguard 3). **This does NOT gate v0 release/tagging:** community review is not a tagging prerequisite, and for v0 the Lead Maintainer may self-merge (governance gates 13 & 14 are formally waived for v0; ≥20 external reviews is the v1 target). Opening this request does not block any release.

**Conflict of interest (COI) declaration:**

<!-- Free text. Disclose any financial, professional, or personal relationships that might bias your review. 
See COI_POLICY.md for examples. -->

---

## Agentic pre-review note

When a reviewer opens an attestation PR (see CONTRIBUTING.md), the following automated gates run:

1. **Evidence-span fidelity** — We verify that verbatim quotes from claims actually appear in the paper.
2. **Fabrication-risk flagging** — We check for inconsistent claims, unresolved DOIs, and duplicate reviews.
3. **COI detection** — We cross-check your ORCID against the paper's author list (via OpenAlex).

All three are **advisory** — the human reviewer and maintainer still make the binding decision. [See SPEC §9.7.3(C) for technical details.]

---

## Checklist

- [ ] I have checked that this paper is **open access or permissive license** (required for v0)
- [ ] I have read [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] I have read [COI_POLICY.md](../../governance/COI_POLICY.md)
- [ ] I understand the reviewer's responsibilities and tier progression
- [ ] (If self-nominating as reviewer) I am listed in `contributors.jsonld` OR willing to complete the onboarding in CONTRIBUTING.md Step 0

---

## Reference

- **Review workflow:** SPEC §9.7 "Community / Public Expert Review"
- **COI policy:** [COI_POLICY.md](../../governance/COI_POLICY.md)
- **Reviewer onboarding:** [CONTRIBUTING.md](../CONTRIBUTING.md) Step 0–1
- **Attestation template:** `templates/attestation.yaml.template`
- **Collections guide:** [README.md](../README.md#collections)
