# Maintainers

## Lead Maintainer

**Louis-Felix Nothias**
- GitHub: [@lfnothias](https://github.com/lfnothias)
- ORCID: [0000-0001-6711-6719](https://orcid.org/0000-0001-6711-6719) (the ORCID in `scripts/release_creators.yaml` and `CITATION.cff`)
- Affiliation: Holobiomics Lab, Institut de Chimie de Nice (ICN), CNRS UMR 7272 / Universite Cote d'Azur
- Email: louisfelix.nothias@gmail.com

### Responsibilities
- Merge all PRs (no self-merge by contributors). In this repository `.github/CODEOWNERS`
  names the lead maintainer as the default owner. At v0 the lead maintainer may
  self-merge PRs they authored (`CONTENT_POLICY.md` §9, gate 13 waiver).
- Act as Lead Curator of the released collections: `scripts/release_creators.yaml`
  lists the lead maintainer as the only lead curator, and candidate assembly writes
  that list into each collection.
- Veto power on release-blocking changes (license, version, deprecation)
- Override authority for soft gates; hard gates are never overridable
  (`CONTENT_POLICY.md` §8).
- Annual release cycle stewardship
- The owner's steps of a release. A release is driven with `scripts/release_domain.py`
  (`docs/RELEASE_DEPOSIT.md`). The steps that tool never performs are the lead
  maintainer's, or are done on the lead maintainer's word: merging the domain and registry pull requests, publishing the Zenodo
  draft, creating and pushing the release tag, and changing repository visibility
  (`CONTENT_POLICY.md` §7.3).

## Mentors for first-time contributors

New contributors should be paired with a mentor for their first review.
Contact the lead maintainer to be assigned one.

## Adding yourself as maintainer

Maintainers are added by the lead maintainer. There is currently no formal process;
contact louisfelix.nothias@gmail.com if you are interested in co-maintaining a domain.
