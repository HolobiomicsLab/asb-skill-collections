---
name: spectral-similarity-scoring-parent-tp
description: Use when after generating TP candidates (via in-silico prediction or library lookup) and extracting MS/MS peak lists for both parent features and TP feature candidates, use spectral similarity scoring to quantify fragmentation pattern overlap.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3370
  tools:
  - patRoon
  - XCMS / OpenMS
  techniques:
  - LC-MS
  - ion-mobility-MS
  - tandem-MS
  - NMR
derived_from:
- doi: 10.1186/s13321-020-00477-w
  title: patRoon
evidence_spans:
- The `generateTPs` function is used to obtain TPs for a particular set of parents.
- componTP <- generateComponents(algorithm = "tp",
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_patroon_cq
    doi: 10.1186/s13321-020-00477-w
    title: patRoon
  dedup_kept_from: coll_patroon_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-020-00477-w
  all_source_dois:
  - 10.1186/s13321-020-00477-w
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Similarity Scoring for Parent-TP Pairing

## Summary

Calculate spectrum similarity metrics between parent chemical MS/MS spectra and transformation product (TP) candidate spectra to rank and filter parent-TP associations based on shared fragmentation patterns. This scoring is a core filtering step in TP componentization workflows to prioritize chemically plausible TP candidates.

## When to use

After generating TP candidates (via in-silico prediction or library lookup) and extracting MS/MS peak lists for both parent features and TP feature candidates, use spectral similarity scoring to quantify fragmentation pattern overlap. Apply this when you have feature groups from before and after transformation (e.g., treatment vs. control samples), suspect-screened TP features, and need to rank candidate TPs by MS/MS coherence with their parents before final componentization validation.

## When NOT to use

- Parent or TP features lack MS/MS spectra (MS1-only data): spectral similarity scoring requires fragment ion information.
- TP candidates are already validated by orthogonal methods (e.g., reference standards, NMR): additional spectral scoring may be redundant.
- Input feature groups contain unfiltered or poorly aligned EIC extractions: noisy or shifted peak lists will produce unreliable similarity estimates.

## Inputs

- fGroups: feature group object with parent feature MS/MS spectra
- fGroupsTPs: feature group object with TP candidate MS/MS spectra
- MSPeakLists: extracted peak lists (m/z, intensity) for parent and TP features
- TPs object: TP library or in-silico predictions (with optional structural annotation)
- formulas: optional formula annotations for fragment/neutral loss matching

## Outputs

- componentsTPs object: ranked parent-TP associations with spectrum similarity scores
- Filtered componentsTPs: subset of associations meeting minSpecSim, minFragMatches, and retDirMatch thresholds
- Candidate ranking matrix: per-parent list of TP candidates sorted by decreasing similarity

## How to apply

Within the generateComponents(algorithm='tp', ...) workflow, supply parent feature group objects (fGroups) and TP feature group objects (fGroupsTPs) along with optional MSPeakLists annotation. The function automatically calculates spectrum similarity between parent and candidate TP MS/MS spectra using a cosine-like or Jaccard metric on m/z-intensity pairs. Post-componentization, apply the minSpecSim (or minSpecSimBoth for bidirectional matching) filter to retain only parent-TP pairs exceeding a user-defined threshold (e.g., 0.5–0.7 cosine similarity). Combine this filter with minFragMatches or minNLMatches (shared fragment or neutral loss counts from formula annotation) and retDirMatch (retention time direction consistency with expected biotransformation) to further refine candidate rankings and reduce false positives.

## Related tools

- **patRoon** (Platform providing generateComponents(algorithm='tp') function and filter methods (minSpecSim, minFragMatches, retDirMatch) for spectral similarity scoring and parent-TP ranking.) — https://github.com/rickhelmus/patRoon
- **XCMS / OpenMS** (Upstream MS feature extraction and MS/MS peak list generation for input to spectral similarity calculations.)

## Examples

```
componTP <- generateComponents(algorithm = "tp", fGroups = fGroups[ni = treatment == "before"], fGroupsTPs = fGroups[ni = treatment == "after"]); componTPFilt <- filter(componTP, retDirMatch = TRUE, minSpecSim = 0.5, minFragMatches = 2)
```

## Evaluation signals

- Verify that componentsTPs object contains non-null spectrum similarity scores (numeric) for each parent-TP pair ranked in decreasing order.
- Check that filtered componentsTPs retains only associations with minSpecSim ≥ threshold (e.g., ≥ 0.5); inspect score distribution to confirm filtering is not over-aggressive.
- Confirm that parent-TP pairs with high spectrum similarity also exhibit low m/z difference and plausible neutral loss patterns consistent with known biotransformation rules (if formulas are available).
- Cross-validate retained associations against experimental or literature-known TPs; false negatives (known TPs filtered out) and false positives (spurious pairs retained) should be minimal.
- Inspect retention time direction consistency: if biotransformation is expected to shift RT (e.g., hydroxylation increasing polarity), verify retDirMatch filter correlates with biological plausibility, not just spectral similarity.

## Limitations

- Spectrum similarity metrics are sensitive to MS instrument type, ionization method, and collision energy; thresholds and scoring parameters may require reoptimization across different instrument platforms or LC-MS conditions.
- Isomeric TPs and their parents often yield very similar MS/MS spectra despite distinct chemical structures; spectral similarity alone cannot distinguish isomers—supplementary data (e.g., CCS from ion mobility, RT, or formula constraints) are needed.
- Low-abundance parent or TP features may produce noisy or incomplete MS/MS spectra, degrading similarity estimates; filtering by minimum peak abundance or SNR before scoring can mitigate this.
- TP candidates predicted in-silico may not reflect the actual structural diversity and MS/MS patterns observed in real samples; library-based TP screening tends to yield more coherent spectral similarities.
- The choice of minSpecSim threshold (e.g., 0.5 vs. 0.7) is empirical and dataset-dependent; aggressive thresholds risk losing true TPs with atypical fragmentation, while lenient thresholds admit false positives.

## Evidence

- [other] Call generateComponents with algorithm='tp', passing fGroups, fGroupsTPs, TPs object, and optional annotation data (MSPeakLists, formulas, compounds) to calculate spectrum similarity and fragment/neutral loss matches between parents and TP candidates.: "Call generateComponents with algorithm='tp', passing fGroups, fGroupsTPs, TPs object, and optional annotation data (MSPeakLists, formulas, compounds) to calculate spectrum similarity and"
- [other] Apply post-componentization filters such as retDirMatch (expected retention direction), minSpecSim or minSpecSimBoth (spectrum similarity threshold), and minFragMatches or minNLMatches (shared fragment/neutral loss counts) to prioritize candidates.: "Apply post-componentization filters such as retDirMatch (expected retention direction), minSpecSim or minSpecSimBoth (spectrum similarity threshold), and minFragMatches or minNLMatches (shared"
- [other] The minimum spectrum similarity between the parent and TP.: "Filter | minSpecSim, minSpecPrec, minSpecSimBoth | The minimum spectrum similarity between the parent and TP"
- [other] Screening for TPs, i.e. chemicals that are formed from a parent chemical by e.g. chemical or biological processes, has broad applications.: "Screening for TPs, i.e. chemicals that are formed from a parent chemical by e.g. chemical or biological processes, has broad applications"
- [readme] MS similarity calculations and others were implemented in C++ to reduce computational times.: "MS similarity calculations and others were implemented in C++ to reduce computational times"
