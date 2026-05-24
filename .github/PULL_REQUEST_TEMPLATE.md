## PR summary

<!-- One sentence: what does this PR add or change? -->

## Type of change

- [ ] New collection (`staged-collections/<slug>/v<N>/`)
- [ ] Review attestation (`collections/<slug>/v<N>/reviews/<doi>.yaml`)
- [ ] Curator candidacy (`candidates/<handle>.yaml`)
- [ ] Leaderboard result (`benchmark/leaderboard.jsonld`)
- [ ] Governance / docs update
- [ ] CI / tooling update

## Checklist

### For all PRs
- [ ] CI is passing (or I have documented why a failure is expected / acceptable)
- [ ] I have read CONTRIBUTING.md

### For review attestations
- [ ] `attestation.yaml` validates against the template schema
- [ ] `is_coauthor` is declared and matches CI auto-detection
- [ ] If `is_coauthor: true`: `co_reviewer` block is present and co-reviewer has posted a sign-off comment

### For new collections
- [ ] `collection.yaml` validates against LinkML schema
- [ ] `curator-criteria.yaml` is filled in for the domain
- [ ] `CITATION.cff` includes all contributors
- [ ] RO-Crate metadata is valid (Workflow Run Profile 0.5)
- [ ] At least 1 skill has `evidence_spans` linking to a verifiable paper quote
- [ ] Description discipline passes CI lint (50-300 chars, "Use when..." lead)

### For curator candidacy PRs
- [ ] `candidates/<handle>.yaml` includes `proof_publications` (2-3 DOIs)
- [ ] GitHub URL is added to ORCID public profile (L1 check)
- [ ] `vet-curator.yml` CI action has run and posted a result comment

## Related issues

<!-- Link to any related issues: Closes #N, Relates to #N -->
