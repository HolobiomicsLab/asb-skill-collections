---
name: molecular-similarity-calculation
description: Use when you have two or more molecular structures (represented as SMILES or spectral data) and need to rank transformation product candidates by structural plausibility, filter isomeric or duplicate TP predictions, or group features into components based on chemical relatedness.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3640
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  tools:
  - patRoon
  - BioTransformer
  - CTS
  - PubChem
  - PubChemLite
  - MetFrag
  - SIRIUS
  techniques:
  - CE-MS
  - tandem-MS
derived_from:
- doi: 10.1186/s13321-020-00477-w
  title: patRoon
evidence_spans:
- The `generateTPs` function is used to obtain TPs for a particular set of parents.
- componTP <- generateComponents(algorithm = "tp",
- '`generateTPs(algorithm = "biotransformer", ...)` | Parents | TPs structural information'
- '`generateTPs(algorithm = "cts", ...)` | Parents | TPs with structural information'
- Library ([PubChem][PubChemLiteTR] or custom)
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

# molecular-similarity-calculation

## Summary

Quantifies structural similarity between pairs of molecules (parent compounds and transformation products, or features within components) using fingerprint-based metrics to rank candidates, filter near-duplicates, and support MS/MS-based componentization in non-target screening workflows.

## When to use

Use this skill when you have two or more molecular structures (represented as SMILES or spectral data) and need to rank transformation product candidates by structural plausibility, filter isomeric or duplicate TP predictions, or group features into components based on chemical relatedness. Typical triggers: (1) filtering TP library results to remove chemically implausible candidates; (2) removing near-duplicate isomers after in-silico TP prediction; (3) ranking annotation candidates from BioTransformer or CTS by structural similarity to the parent; (4) grouping features in componentization workflows using spectral similarity as a proxy for chemical relationship.

## When NOT to use

- Input lacks structural information (no SMILES or spectra); use formula-based filtering (formula fragment matches, neutral loss matching) instead.
- Workflow goal is exhaustive TP prediction, not filtering; applying strict similarity thresholds may remove genuine but structurally divergent TPs from deep metabolic pathways.
- Feature data are already curated and pre-filtered by the analyst; re-applying similarity filters may discard valid biological signals.

## Inputs

- parent compound SMILES or molecular structure
- TP candidate SMILES or structures (from BioTransformer, CTS, library, or annotation algorithms)
- parent MS/MS spectrum (m/z, intensity pairs)
- TP MS/MS spectra or feature spectra
- optional: log P values for structural descriptors

## Outputs

- TP object with ranked candidates (filtered and sorted by similarity score)
- filtered component object (features grouped by MS/MS spectral similarity)
- list of retained TPs passing minSimilarity threshold
- removed duplicates and isomers (audit trail)

## How to apply

Calculate pairwise structural similarity scores using fingerprint-based metrics (e.g., Tanimoto coefficient on molecular fingerprints) between parent and TP candidates, or between MS/MS spectra of features. Set a minimum similarity threshold (e.g., minSimilarity = 0.5 in patRoon) to retain only structurally plausible transformations; apply threshold filters to remove TPs whose similarity to the parent falls below this cutoff, or to eliminate isomers and near-duplicates. For spectrum-based similarity, use minimum spectral similarity thresholds (minSpecSim) and fragment match counts (minFragMatches, minNLMatches) to prioritize high-confidence MS/MS matches. The rationale is that true transformation products should retain substantial structural or spectral similarity to the parent, whereas random chemical predictions or database noise will score below the threshold. Use topMost ranking (e.g., topMost = 25) to further focus on the highest-scoring candidates when library size is large.

## Related tools

- **patRoon** (R interface for applying similarity filtering via filter() and minSimilarity parameter on TP and component objects; provides native similarity calculation and ranking functions) — github.com/rickhelmus/patRoon
- **BioTransformer** (generates TP candidates that are then ranked and filtered by molecular similarity)
- **CTS** (generates in-silico TP predictions subject to similarity filtering)
- **PubChemLite** (library of known TPs retrieved and ranked by similarity to parent)
- **MetFrag** (MS/MS fragment matching and spectral similarity calculation used to rank compound annotation candidates)
- **SIRIUS** (generates molecular formula and compound candidates ranked by similarity metrics)

## Examples

```
TPsF <- filter(TPs, minSimilarity = 0.5, removeParentIsomers = TRUE, removeTPIsomers = TRUE, topMost = 25)
```

## Evaluation signals

- Similarity scores are in the range [0, 1], with retained TPs above minSimilarity threshold (e.g., ≥ 0.5) and rejected TPs below; audit removal counts.
- TP count decreases monotonically with increasing minSimilarity threshold; no retained TPs should violate the cutoff.
- Spectrum similarity (minSpecSim) and fragment match counts (minFragMatches, minNLMatches) are consistently applied across all parent–TP pairs; no inconsistent filtering.
- Removed isomers and duplicates are logged; verify that structural isomers (identical formula, different connectivity) are correctly identified and removed when removeTPIsomers = TRUE or removeParentIsomers = TRUE.
- Ranked candidate list is sorted in descending order of similarity; top candidate(s) should be manually inspectable and chemically plausible (e.g., known metabolite or minor structural variant of parent).

## Limitations

- Similarity metrics based on fingerprints (e.g., Tanimoto on Morgan/ECFP) are biased toward large molecular changes; structurally similar but small modifications may score lower than expected. Performance varies with fingerprint type and radius.
- Spectral similarity (minSpecSim) depends on MS/MS quality, ionization mode, and collision energy; poorly fragmented spectra or different instrumental conditions may yield artificially low similarity scores between true related compounds.
- Isomer detection (removeParentIsomers, removeTPIsomers) relies on exact molecular formula matching; does not distinguish stereoisomers or regioisomers without explicit 3D structural comparison.
- Library-based TP screening (PubChemLite) only filters known or experimentally confirmed TPs; similarity filtering does not help predict novel or pathway-specific TPs not in the library.
- Multi-step transformations (generations > 1) may produce TPs with low similarity to the original parent despite being biologically plausible; high minSimilarity thresholds may inadvertently exclude multi-generation metabolites.

## Evidence

- [other] minSimilarity parameter and threshold application: "TPsF <- filter(TPs, minSimilarity = 0.5)"
- [other] isomer removal in TP filtering workflow: "TPsF <- filter(TPs, removeParentIsomers = TRUE, removeTPIsomers = TRUE)"
- [other] spectral similarity and fragment matching for TP filtering: "Filter | minSpecSim, minSpecPrec, minSpecSimBoth | The minimum spectrum similarity between the parent and TP."
- [other] ranking by TP Score incorporating structural similarity: "For ann_comp and ann_form, rank candidates by TP Score incorporating structural similarity and suspect matching."
- [other] topMost ranking for limiting candidate output: "TPsAnnCompF <- filter(TPsAnnComp, minTPScore = 0.5, topMost = 25)"
- [readme] native C++ implementation of MS similarity: "Code for loading MS and EIC data, MS similarity calculations and others were implemented in `C++` to reduce computational times."
