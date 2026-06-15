---
name: scientific-task-formulation
description: 'Use when you have tandem MS/MS spectra from natural product samples annotated by multiple orthogonal tools (GNPS, ISDB-LOTUS, Sirius 6) and need a single, ranked decision output that reconciles conflicting or uncertain identifications. Specifically: when you hold a .mgf file, quantitative .'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3050
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3572
  tools:
  - GitHub
  - GNPS (Global Natural Products Social Molecular Networking)
  - ISDB-LOTUS
  - Sirius 6
  - MatchMS
  - MZmine
  - npanalyst
  - forward_train.py
  - forward_evaluate_pipeline.py
  - analysis_pipeline.py
  - Conda / Mamba
derived_from:
- doi: 10.1002/cmtd.202400088
  title: ms2decide
- doi: 10.1021/acscentsci.1c01108
  title: ''
- doi: 10.1021/acs.analchem.2c02093
  title: ''
- doi: 10.1021/acs.analchem.5c03730
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_13c_spacem
    doi: 10.1038/s42255-024-01118-4
    title: 13C-SpaceM
  - build: coll_bindiscover
    doi: 10.1186/s13321-023-00734-8
    title: bindiscover
  - build: coll_hexpmetdb
    doi: 10.1289/EHP7722
    title: HExpMetDB
  - build: coll_ms2decide
    doi: 10.1002/cmtd.202400088
    title: ms2decide
  - build: coll_np_analyst
    doi: 10.1021/acscentsci.1c01108
    title: NP Analyst
  - build: coll_rassp
    doi: 10.1021/acs.analchem.2c02093
    title: rassp
  - build: coll_rtmsecho
    doi: 10.1021/acs.analchem.5c03730
    title: rtmsecho
  dedup_kept_from: coll_ms2decide
schema_version: 0.2.0
---

# scientific_task_formulation

## Summary

Formulate and scope a reproducible scientific task by integrating multisource annotations (GNPS, ISDB-LOTUS, Sirius) and applying decision theory to rank natural product identifications from tandem mass spectrometry data. This skill bridges expert knowledge elicitation with computational annotation aggregation to prioritize compounds in discovery workflows.

## When to use

You have tandem MS/MS spectra from natural product samples annotated by multiple orthogonal tools (GNPS, ISDB-LOTUS, Sirius 6) and need a single, ranked decision output that reconciles conflicting or uncertain identifications. Specifically: when you hold a .mgf file, quantitative .csv table, and at least two completed annotation sets, and the annotations disagree or have low confidence individually.

## When NOT to use

- Input annotations come from a single tool only (K_estimation requires multi-tool agreement to compute meaningful similarity scores).
- Sirius 6 output file contains redundant feature mappings in 'mappingFeatureId' column (will raise 'DataFrame index must be unique' error; must be cleaned before use).
- No internet connectivity available (GNPS and ISDB-LOTUS access required).
- Mass spectrometry data is already feature-matched and ranked by another method; re-ranking may introduce inconsistency.

## Inputs

- quantitative data table (.csv format, e.g., MZmine FBMN export)
- tandem mass spectrometry data (.mgf file)
- Sirius 6 annotation file (structure_identifications.tsv)
- GNPS credentials (username, password, email)
- ionization mode selection (POS or NEG)
- mass tolerance parameter (<0.5 Da)

## Outputs

- filtered and ranked .tsv file (K_estimation output) with K-values and unified annotations
- optional: empty.tsv report (empty annotations from iterative GNPS analog search)

## How to apply

Invoke K_estimation() to aggregate annotations via decision theory: (1) provide GNPS credentials and specify strict or iterative weighted analog search (iterative can run 27 jobs over ~3 hours); (2) supply quantitative table (.csv) and MS/MS data (.mgf, preferably from MZmine >2.53 FBMN export); (3) select ionization mode (POS/NEG) and mass tolerance (<0.5 Da, default 0.02) for ISDB-LOTUS; (4) provide Sirius 6 structure_identifications.tsv and choose confidence score type (exact or approximate); (5) the function computes tanimoto-based similarity between tool pairs, applies default values (0.7 for missing GNPS–Sirius matches, 0.5 for failed Sirius annotations), and exports ranked .tsv output sorted by K-values. Zero ISDB-LOTUS matches are treated as meaningful novelty signals, not failures.

## Related tools

- **GNPS (Global Natural Products Social Molecular Networking)** (spectral library search and feature-based molecular networking; supports both strict (0.02 Da tolerance, 0.001 threshold) and iterative weighted analog search modes) — https://ccms-ucsd.github.io/GNPSDocumentation/librarysearch/
- **ISDB-LOTUS** (spectral matching and structure annotation via CFM-ID 4.0 using MatchMS library; applied with user-specified ionization mode and mass tolerance) — https://zenodo.org/records/8287341
- **Sirius 6** (de novo structure annotation with confidence scoring (exact or approximate modes); outputs structure_identifications.tsv for input to K_estimation) — https://v6.docs.sirius-ms.io/
- **MatchMS** (spectral library matching backend for ISDB-LOTUS comparisons)
- **MZmine** (feature extraction and quantification; FBMN module produces .csv and .mgf exports compatible with K_estimation (version >2.53 recommended))

## Examples

```
from ms2decide.K_estimation import K_estimation
K_estimation()
```

## Evaluation signals

- Output .tsv file is successfully generated and contains a 'K' column with numeric values ranked by certainty.
- All three annotation sources (GNPS, ISDB-LOTUS, Sirius) appear as columns in the output; missing annotations have been filled with documented default values (0.7 or 0.5).
- Tanimoto similarity scores between tool pairs are computed and fall within [0, 1] range; check that at least one inter-tool similarity is present (not all defaults).
- Feature count in output matches input feature count unless user-specified filtering was applied; verify no rows were dropped unexpectedly.
- When iterative GNPS search is used, optional empty.tsv report can be inspected to confirm empty annotation signals are preserved separately.

## Limitations

- When GNPS or Sirius fails to annotate, default tanimoto values (0.7 for GNPS–Sirius missing pairs; 0.5 for failed Sirius confidence) are assigned, reducing signal specificity for those features.
- Strict ISDB-LOTUS library search (0.02 Da) may miss isobars and isomers; zero matches are treated as novelty rather than failure, which may conflate unknown compounds with truly novel ones.
- Iterative weighted GNPS analog search launches 27 jobs and can require up to 3 hours; strict mode (single job) is faster but less sensitive.
- Redundant feature IDs in Sirius structure_identifications.tsv cause DataFrame uniqueness errors; manual inspection and cleaning of the input file is required before processing.
- No changelog is available in the repository, limiting reproducibility tracking across versions.

## Evidence

- [readme] The K_estimation function: - Integrates annotation data from multiple sources: GNPS, ISDB-LOTUS, and Sirius.: "Integrates annotation data from multiple sources: GNPS, ISDB-LOTUS, and Sirius."
- [readme] MS2DECIDE is a Python library that leverages decision theory to assist chemists in natural products multiannotation and prioritization.: "MS2DECIDE is a Python library that leverages decision theory to assist chemists in natural products multiannotation and prioritization."
- [readme] By gathering insights from domain experts and modeling their intuition, the library offers a structured, data-driven approach to interpreting multiannotated tandem mass spectrometry data.: "By gathering insights from domain experts and modeling their intuition, the library offers a structured, data-driven approach to interpreting multiannotated tandem mass spectrometry data."
- [readme] Ensure that your input files follow the required format (.csv for quantitative data, .mgf for mass spectrometry data). If you use the export file module of MZmine (>2.53) for FBMN, the format will be accepted.: "Ensure that your input files follow the required format (.csv for quantitative data, .mgf for mass spectrometry data). If you use the export file module of MZmine (>2.53) for FBMN, the format will be"
- [readme] Choose the type of GNPS library search: strict: Uses a typical mass difference tolerance of 0.02 Da and threshold value of 0.001. iterative: for iterative weighted analog search (can take up to three hours).: "Choose the type of GNPS library search: strict: Uses a typical mass difference tolerance of 0.02 Da and threshold value of 0.001. iterative: for iterative weighted analog search (can take up to three"
- [readme] ISDB-LOTUS annotation is performed using the function isdb_res = get_cfm_annotation(mgf, ISDBtol). During the process, the user will be prompted to choose: Ionization mode: Specify the ionization mode for annotation (POS for positive, NEG for negative). Mass tolerance: Provide a mass tolerance value less than 0.5 (default: 0.02).: "During the process, the user will be prompted to choose: Ionization mode: Specify the ionization mode for annotation (POS for positive, NEG for negative). Mass tolerance: Provide a mass tolerance"
- [readme] In scenarios where there is no match with GNPS or no match with Sirius, the tanimoto between GNPS and Sirius cannot be calculated. Hence, a default value of 0.7 was assigned to T_gs and T_gi in these instances.: "In scenarios where there is no match with GNPS or no match with Sirius, the tanimoto between GNPS and Sirius cannot be calculated. Hence, a default value of 0.7 was assigned to T_gs and T_gi in these"
- [readme] Sirius annotations were performed in batch mode by using Sirius 6. we utilized the Confidence Approximate score. Unfortunately, in some cases, Sirius was not able to propose an annotation. To remedy, we associated a value of 0.5 to Sirius matching score.: "Unfortunately, in some cases, Sirius was not able to propose an annotation. To remedy, we associated a value of 0.5 to Sirius matching score."
- [readme] For ISDB-LOTUS, since a strict library search was applied (0.02 Da), we considered a zero answer as an important information regarding our definition of novelty.: "For ISDB-LOTUS, since a strict library search was applied (0.02 Da), we considered a zero answer as an important information regarding our definition of novelty."
