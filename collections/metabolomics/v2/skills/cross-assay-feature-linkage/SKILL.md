---
name: cross-assay-feature-linkage
description: Use when when you have structural clusters from multiple LC-MS assays (e.g., positive and negative ion modes, or reversed-phase and HILIC methods) and need to identify which features across assays represent the same underlying metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - networkx
  - pyvis
  - matplotlib
  - MamsiStructSearch
  - peakPantheR
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets.
- import pandas as pd
- import numpy as np
- 'Dependencies: scipy'
- 'Dependencies: networkx'
- 'Dependencies: pyvis'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi_cq
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01327
  all_source_dois:
  - 10.1021/acs.analchem.5c01327
  - 10.1371/journal.pcbi.1011814
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-assay-feature-linkage

## Summary

Link statistically significant LC-MS features across multiple assays (e.g., HPOS, LPOS, LNEG) by identifying features that represent the same metabolite in different ionization modes or chromatographic methods. This skill uses mass-to-charge ratio and retention time patterns to recognize common metabolites across assays and strengthen evidence for compound identification in multi-assay metabolomics studies.

## When to use

When you have structural clusters from multiple LC-MS assays (e.g., positive and negative ion modes, or reversed-phase and HILIC methods) and need to identify which features across assays represent the same underlying metabolite. Use this skill after performing retention-time windowing and intra-assay isotopologue/adduct clustering, and when you have reference patterns such as [M+H]+/[M-H]- pairs that can anchor cross-assay matches.

## When NOT to use

- Input contains only a single LC-MS assay (no cross-assay comparison needed; use intra-assay clustering instead)
- Retention times are not comparable across assays (e.g., different instruments, columns, or gradient methods not properly aligned)
- You have not yet performed intra-assay structural clustering (isotopologue and adduct detection); cross-assay linking requires pre-clustered features

## Inputs

- Structural clusters (DataFrame) from MamsiStructSearch with columns: Feature, Assay, Isotopologue_group, Isotopologue_pattern, Adduct_group, Adduct, Structural_cluster
- Multi-assay LC-MS feature tables (one per assay: HPOS, LPOS, LNEG, etc.) with m/z and retention time columns
- Reference adduct patterns (e.g., [M+H]+, [M-H]-) and their mass shifts
- Retention time window tolerance (typically 5 seconds)

## Outputs

- Annotated structural clusters table with added Cross-assay_link column indicating which features are linked across assays
- Feature-to-cluster assignments spanning multiple assays
- Cross-assay link metadata (source_assay, target_assay, reference_adduct_pair, mass_match_ppm, rt_difference)

## How to apply

After MamsiStructSearch has grouped features into structural clusters within each assay using 5-second retention time windows and isotopologue/adduct signatures, search for cross-assay links by using [M+H]+/[M-H]- as reference patterns to match features across assays. For each cluster, calculate hypothetical neutral masses from features in one assay (e.g., HPOS [M+H]+ adducts) and look for matching features in another assay (e.g., LNEG [M-H]- adducts) within the same retention time window and mass tolerance (typically 10 ppm). Features that match on both neutral mass and retention time proximity are marked as cross-assay links and merged into a unified structural cluster annotation. The rationale is that the same metabolite will elute at approximately the same retention time across methods and, when accounting for ionization differences, will have a consistent neutral mass.

## Related tools

- **MamsiStructSearch** (Performs structural clustering (isotopologue and adduct detection within each assay) and executes cross-assay linking using [M+H]+/[M-H]- reference patterns) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (DataFrame manipulation and merging of cross-assay cluster assignments)
- **numpy** (Mass and retention time tolerance calculations (ppm and time difference thresholds))
- **scipy** (Distance and similarity metrics for validating neutral mass matches)
- **peakPantheR** (Optional: provides ROI files with retention time reference ranges for given chromatography and m/z, enabling automated annotation and cross-assay validation) — https://github.com/phenomecentre/peakPantheR

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected)
struct.get_structural_clusters(annotate=True)
```

## Evaluation signals

- Cross-assay link assignments are consistent with known metabolite ionization patterns (e.g., [M+H]+ in positive mode matches [M-H]- in negative mode for the same neutral mass within ±10 ppm)
- Features flagged as cross-assay linked show retention time differences ≤ 5 seconds across assays
- Neutral mass calculations from different adduct forms converge to the same value within mass tolerance; verify by back-calculating m/z from assigned neutral mass and adduct formula
- Network visualization of linked features across assays shows plausible structural relationships (isotopologues, adducts, cross-assay anchors) with no contradictory mass assignments
- Count and percentage of features with at least one cross-assay link; validate against expected metabolite diversity and assay complementarity

## Limitations

- Cross-assay linking relies on consistent retention time alignment across assays; if chromatographic columns, gradients, or instrument conditions differ substantially, retention times may shift beyond the 5-second tolerance, leading to missed links or false negatives.
- Reference adduct patterns ([M+H]+, [M-H]-) are limited to common electrospray ionization adducts; unusual or tissue-specific adducts may not be detected.
- Mass accuracy and calibration must be maintained across all assays; systematic m/z drift or recalibration between assays can introduce false negatives in cross-assay matching.
- The method is most effective when assays are run on similar platforms and use standard chromatographic methods (e.g., RPOS, RNEG, HPOS as documented in National Phenome Centre protocols); cross-linking between fundamentally different LC-MS methods may be unreliable.
- Requires pre-existing structural clustering (isotopologue and adduct detection) within each assay; cannot operate on raw feature tables without prior filtering and grouping.

## Evidence

- [methods] Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references.: "we search cross-assay clusters using [M+H]+/[M-H]- as link references"
- [methods] all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da: "RT windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures"
- [methods] This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation.: "calculating hypothetical neutral masses based on common adducts in electrospray ionisation"
- [methods] Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters"
- [intro] the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters: "linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters"
- [readme] Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references. Additionally, our structural search tool, that utilises region of interest [(ROI) files] from peakPantheR, allows for automated annotation of some features based on the RT for a given chromatography and m/z.: "search cross-assay clusters using [M+H]+/[M-H]- as link references. Additionally, our structural search tool...allows for automated annotation of some features based on the RT for a given"
