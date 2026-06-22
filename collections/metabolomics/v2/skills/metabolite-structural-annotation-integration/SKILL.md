---
name: metabolite-structural-annotation-integration
description: Use when after statistical analysis (e.g., MB-PLS with permutation testing) has identified a subset of significant LC-MS features (p < 0.05 or similar threshold) that require structural interpretation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3068
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - scikit-learn
  - matplotlib
  - MamsiStructSearch
  - peakPantheR
  - npc-open-lcms
  - scipy / numpy
  - networkx
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework
- import pandas as pd
- import numpy as np
- scipy
- 'Dependencies: scipy'
- from sklearn.model_selection import train_test_split
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

# Metabolite Structural Annotation Integration

## Summary

Integrate statistically significant LC-MS features into structural clusters by detecting isotopologue and adduct signatures, then cross-reference with retention time and m/z-based metabolite annotations to assign putative identities. This skill bridges the gap between multivariate statistical feature selection and structural/chemical interpretation of untargeted metabolomics.

## When to use

After statistical analysis (e.g., MB-PLS with permutation testing) has identified a subset of significant LC-MS features (p < 0.05 or similar threshold) that require structural interpretation. Specifically, when you have a feature table with columns in format (AssayName)_(RTsec)_(m/z)m/z and access to retention-time and m/z-based metabolite reference libraries (e.g., from National Phenome Centre LC-MS assays), and you need to disambiguate whether multiple feature peaks represent the same metabolite (as isotopologues, adducts, or cross-assay equivalents) or distinct structures.

## When NOT to use

- Input features already clustered or pre-annotated by targeted methods (e.g., MRM transitions); structural clustering is designed for untargeted data.
- No retention time or m/z resolution sufficient to distinguish isotopologues (Δm/z < 1.00335 Da detection requires mass accuracy better than ~1 ppm).
- Metabolite reference annotations unavailable and chemical interpretation is not the goal; structural clustering alone (without annotation) may not provide sufficient biological insight.

## Inputs

- Feature table (pandas DataFrame) with columns named (AssayName)_(RTsec)_(m/z)m/z (e.g., HPOS_120.5_250.1234)
- Statistically significant feature subset (e.g., mask or filtered DataFrame with p < 0.05)
- Retention time tolerance window parameter (seconds; default 5)
- Mass tolerance parameter (ppm; default 15)
- Metabolite annotation ROI files (optional, for automated annotation; format from peakPantheR or npc-open-lcms)

## Outputs

- Annotated feature table with structural cluster membership assignments
- Structural cluster definitions (grouped feature indices, inferred neutral masses, adduct/isotopologue relationships)
- Putative metabolite identities and chemical annotations (if ROI files provided)
- Feature network object (networkx graph) showing structural links (adducts, isotopologues, cross-assay edges)

## How to apply

Load statistically significant features into MamsiStructSearch by calling .load_lcms() to extract metadata (m/z, RT, assay name). Partition all features into retention time windows (default 5 seconds) and search within each window for isotopologue signatures by identifying mass differences of exactly 1.00335 Da between m/z values. Next, calculate hypothetical neutral masses for each feature by applying common electrospray ionisation adduct mass shifts ([M+H]+, [M-H]−, [M+Na]+, etc.) and match neutral masses within the specified mass tolerance (default 15 ppm). Group features with matching neutral masses into adduct clusters. Merge overlapping isotopologue and adduct clusters to form structural clusters via .get_structural_clusters(). Finally, cross-reference cluster neutral masses and retention times against curated metabolite annotation ROI files (from peakPantheR or npc-open-lcms) to assign putative metabolite identities and chemical annotations to each cluster.

## Related tools

- **MamsiStructSearch** (Core class for loading LC-MS feature metadata, detecting isotopologue/adduct signatures, merging clusters, and assigning structural relationships via .load_lcms(), .get_structural_clusters(), and .get_structural_network()) — https://github.com/kopeckylukas/py-mamsi
- **peakPantheR** (Provides retention-time and m/z-based metabolite annotations via ROI (region of interest) files used by MamsiStructSearch for automated feature annotation) — https://github.com/phenomecentre/peakPantheR
- **npc-open-lcms** (Repository of LC-MS metabolite annotations and chromatographic methods for National Phenome Centre assays (RPOS, RNEG, HPOS, LPOS, LNEG, BANEG); used to generate ROI reference files for structural annotation) — https://github.com/phenomecentre/npc-open-lcms
- **pandas** (Data manipulation and DataFrame operations for loading, filtering, and organizing feature tables with named columns)
- **scipy / numpy** (Numerical computation for mass difference calculations, adduct mass shift arithmetic, and hierarchical clustering support)
- **networkx** (Construction and export of feature relationship networks representing structural links (adducts, isotopologues, cross-assay); output can be visualized in Cytoscape)
- **scikit-learn** (Hierarchical clustering algorithm for optional correlation-based feature grouping via .get_correlation_clusters() with configurable linkage criteria and flattening methods)

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=15)
struct.load_lcms(selected_features)
struct.get_structural_clusters(annotate=True)
network = struct.get_structural_network(include_all=True, interactive=False, labels=True, return_nx_object=True)
```

## Evaluation signals

- Cluster assignments are reproducible: running .get_structural_clusters() twice on the same input with identical parameters yields identical cluster membership.
- All features in an adduct cluster share the same calculated neutral mass (within ppm tolerance) when back-calculated from their observed m/z and assigned adduct type.
- Isotopologue clusters contain exactly two or more features with mass differences of 1.00335 ± (1 ppm × m/z / 1e6) Da within the same RT window.
- Cross-assay cluster links are valid: features from different assay prefixes (e.g., HPOS vs. LPOS) assigned to the same cluster must share identical or near-identical neutral masses and RT values (within tolerance).
- Annotated features match metabolite reference library entries: putative identities returned should have RT and m/z within ±5 sec and ±15 ppm of the respective reference values.

## Limitations

- Detection of isotopologue signatures relies on m/z resolution and accuracy; features with lower mass accuracy (>1 ppm) may fail to resolve 1.00335 Da differences.
- Automated annotation (via ROI files) is currently supported only for assays processed by the National Phenome Centre; other LC-MS assays require manual curation or external annotation databases.
- Adduct detection assumes common electrospray ionisation adducts; unusual or non-standard adducts (e.g., metal-bound complexes, radical cations) will not be detected.
- Structural clustering does not distinguish isomeric metabolites; multiple isomers with identical m/z and similar RT will be grouped into a single cluster.
- No permutation-based validation of cluster stability is currently implemented; cluster membership may vary if input features are noisy or near retention-time/mass tolerance boundaries.

## Evidence

- [readme] each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 *Da* between mass-to-charge ratios (*m/z*) of the features: "each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 *Da* between mass-to-charge ratios (*m/z*) of the features"
- [readme] This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation.: "This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation."
- [readme] Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [readme] our structural search tool, that utilises region of interest [(ROI) files](https://github.com/phenomecentre/npc-open-lcms) from peakPantheR [[4](#references)], allows for automated annotation of  some features based on the *RT* for a given chromatography and *m/z*.: "our structural search tool, that utilises region of interest [(ROI) files] from peakPantheR, allows for automated annotation of  some features based on the *RT* for a given chromatography and *m/z*."
- [intro] MAMSI links statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters defined by structural properties based on m/z and RT: "MAMSI links statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters defined by structural properties based"
- [readme] struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected)
struct.get_structural_clusters(annotate=True): "struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected)
struct.get_structural_clusters(annotate=True)"
