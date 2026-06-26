---
name: Claim / contribute a skill for your tool (become a co-author)
about: A tool's author contributes (or claims) a skill grounded on their tool/paper and is credited as a verified co-author. Keep it short — a maintainer runs the claim-skill command and stages the PR.
title: "Claim skill: <tool / skill name>"
labels: ["claim", "community-skill", "co-authorship", "needs-triage"]
---

<!--
Use this when YOU are the author of the tool (or method/paper) a skill grounds
on, and you want to contribute that skill AND be credited as a co-author. Keep
it short: tell us the tool/paper, what the skill does, and who you are. A
maintainer runs the `claim-skill` command, which normalizes/matches/grounds the
skill (the propose-skill flow), writes you into the staged skill's `contributors`
as `role: author`, and stages a reviewable PR with `Co-authored-by:` you. A
maintainer makes the final merge decision — you cannot self-merge.

Authorship is **identity-verified**: your ORCID/GitHub are checked the same way
candidate curators are (L1 GitHub-in-ORCID, L2 ORCID-on-the-tool's-paper via
OpenAlex, run by `vet-curator`) BEFORE you are credited. See
governance/AUTHORSHIP.md and governance/COMMUNITY_SKILLS.md.
-->

**What does the skill do?** <!-- one line, e.g. "Use when aligning RT across batches with <tool>" -->

**Your tool / method (and its paper, if any):**
<!-- tool name + repo/homepage, and the DOI of the paper that describes it -->

**Link to the skill:** <!-- a gist, repo path, or the SKILL.md pasted below — whatever you have -->

**Target collection:** <!-- metabolomics (default), or another collection slug -->

## You (for verified authorship credit — required)

<!--
We verify these before crediting you (governance/AUTHORSHIP.md). Make sure your
ORCID public profile lists your GitHub URL (the L1 check) and that your ORCID
is an author on the tool's paper above (the L2 check, via OpenAlex).
-->

- **Name (as it should appear in credit):**
- **ORCID:** <!-- 0000-0000-0000-0000 -->
- **GitHub:** <!-- @handle -->
- **Email for `Co-authored-by:`** <!-- the address you want on the merge commit's trailer -->

---
<!-- Optional, all skippable — a maintainer/the command resolves these: -->
- **Related existing skills?** <!-- slugs it overlaps or composes, if you know them -->
- **Conflict of interest?** <!-- you authoring a skill for your own tool is disclosed, not disqualifying — the maintainer is the independent gate; see governance/AUTHORSHIP.md -->

## Licensing

- [ ] I am an author of the tool/method this skill grounds on, and the identity I
      give above is mine.
- [ ] I license my contributed skill prose (description + body) under **CC-BY-4.0**.

<!--
The CC-BY-4.0 grant covers the text you wrote. It is separate from the skill's
`license_tier`, which describes the tool the skill grounds on (open / noncommercial
/ restricted) — see governance/LICENSE_TIERS.md.
-->
