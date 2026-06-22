---
name: cross-assay-feature-linkage-analysis
description: Use when after identifying statistically significant features within individual LC-MS assays (e.g., via MB-VIP and permutation testing), use this skill when you have multiple parallel assays acquired in complementary ionization modes (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - pandas
  - numpy
  - matplotlib
  - MAMSI (MamsiStructSearch)
  - Cytoscape
  techniques:
  - LC-MS
  - GC-MS
  - NMR
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework
- import pandas as pd
- import numpy as np
- from matplotlib import pyplot as plt
- A class for performing structural search on multi-modal MS data using
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi
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

# cross-assay-feature-linkage-analysis

## Summary

Link statistically significant LC-MS features across multiple assays (e.g., HPOS, LPOS, LNEG) by matching their ionization states ([M+H]+/[M-H]− pairs) to identify the same metabolite detected in different chromatographic or ionization modes. This enables unified structural clustering and interpretation of multi-assay metabolomics datasets.

## When to use

After identifying statistically significant features within individual LC-MS assays (e.g., via MB-VIP and permutation testing), use this skill when you have multiple parallel assays acquired in complementary ionization modes (e.g., positive and negative ESI) or chromatographic separation methods (e.g., RPOS, HILIC, lipidomic RP) and need to recognize which features represent the same underlying metabolite across assays to avoid redundant annotation and improve structural interpretation.

## When NOT to use

- Input contains only a single LC-MS assay; cross-assay linking requires multiple parallel assays.
- Features are already annotated or curated manually; this skill is for automated discovery of cross-assay identity, not for validating known annotations.
- Data are targeted (e.g., MRM-scheduled) rather than untargeted profiling; untargeted discovery of adduct signatures is the intended use case.

## Inputs

- Statistically significant LC-MS feature table (selected features from multiple assays, with column names following AssayName_(RTsec)_(m/z)m/z convention)
- Feature metadata: retention time (RT, in seconds), mass-to-charge ratio (m/z), assay origin

## Outputs

- Cross-assay structural clusters (sets of features from different assays linked by [M+H]+/[M-H]− ionization state matching)
- Cluster metadata table (cluster ID, member assays, constituent features, neutral mass, RT window)
- Network representation (nodes = features, edges = cross-assay links with link type annotation)

## How to apply

Within a retention time (RT) window (typically 5-second intervals), search for cross-assay links by matching hypothetical neutral masses calculated from features in different assays using [M+H]+/[M-H]− as canonical reference ionization states. For each feature in one assay, calculate its neutral mass by de-adducting using known ESI adduct mass shifts; compare neutral masses across assays within a predefined mass tolerance (typically 15 ppm, adjustable). When two or more features from different assays yield matching neutral masses, group them as a cross-assay structural cluster. This process is performed after (and merged with) isotopologue and single-assay adduct clustering. The resulting cross-assay links are represented as edges in a network visualization and stored in the structural cluster metadata with link type (e.g., 'cross-assay [M+H]+/[M-H]−').

## Related tools

- **MAMSI (MamsiStructSearch)** (Python class that loads LC-MS feature data, performs cross-assay structural clustering via get_structural_clusters() method with adduct parameterization, and returns cross-assay link assignments) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Data manipulation and column filtering to concatenate selected features from multiple assays and extract cross-assay cluster results)
- **Cytoscape** (Optional downstream visualization and exploration of the cross-assay feature network saved as a NetworkX object to inspect structural relationships) — https://cytoscape.org

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=15)
struct.load_lcms(selected)
struct.get_structural_clusters()
cross_assay_clusters = struct.structural_clusters
```

## Evaluation signals

- All cross-assay links should pair features with matching or near-matching neutral masses (within the specified ppm tolerance, typically 15 ppm) when de-adducted using standard ESI adduct shifts (+1.00783 Da for [M+H]+, −1.00783 Da for [M-H]−)
- Cross-assay clusters should only form between features in different assays; features from the same assay should not be cross-linked (they should be grouped in single-assay adduct or isotopologue clusters)
- RT overlap between linked features should be small (within the RT window size, typically ≤5 seconds), validating chromatographic co-elution
- Network degree distribution and cluster size should be reasonable: no single feature should link to >5 assay partners, and most cross-assay clusters should contain 2–4 features (representing different ionization modes of the same metabolite)
- Feature coverage metric (% of features assigned to ≥1 cross-assay link) should be lower than single-assay cluster coverage, reflecting that cross-assay linkage is a subset of all structural relationships

## Limitations

- Cross-assay linking assumes that the ionization states [M+H]+ and [M-H]− are present and detectable in complementary assays; metabolites ionizing as only [M+Na]+ or [M+K]+ or forming only proton adducts in one mode may not be linked even if chemically identical.
- Mass tolerance (ppm) must be appropriate for instrument resolution and calibration; mismatched ppm setting (e.g., 15 ppm on a low-resolution or poorly calibrated instrument) can create false links or miss true cross-assay pairs.
- RT alignment between assays is assumed to be sufficiently accurate (RT window size must accommodate inter-assay RT drift); severe RT drift or systematic shift between instruments can prevent linking of the same metabolite across assays.
- The approach is limited to LC-MS data; it is not applicable to other omics modalities (e.g., GC-MS, NMR, or protein assays) unless the ionization and adduct model are analogous.
- No changelog is available for the MAMSI package, so version-specific behavior or parameter defaults (e.g., default ppm tolerance or adduct list) must be verified in documentation or source code.

## Evidence

- [methods] Further, we search cross-assay clusters using [M+H]<sup>+</sup>/[M-H]<sup>−</sup> as link references.: "Further, we search cross-assay clusters using [M+H]+/[M-H]− as link references."
- [methods] This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation. If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 *ppm*) then these features are grouped together.: "calculating hypothetical neutral masses based on common adducts in electrospray ionisation. If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 ppm)"
- [methods] Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [intro] MAMSI links statistically significant features of untargeted multi-assay LC-MS metabolomics datasets into clusters defined by structural properties based on m/z and RT: "MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters"
- [readme] struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected)
struct.get_structural_clusters(annotate=True): "struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected)
struct.get_structural_clusters(annotate=True)"
