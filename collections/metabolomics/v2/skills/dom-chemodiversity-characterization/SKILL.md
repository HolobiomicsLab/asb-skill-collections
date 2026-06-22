---
name: dom-chemodiversity-characterization
description: Use when you have a formula-assigned FT-ICR MS dataset (molecular formulas already assigned to individual mass features) and seek to understand the chemodiversity landscape and transformation relationships within DOM.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0621
  tools:
  - MoleTrans
  techniques:
  - NMR
derived_from:
- doi: 10.1021/acs.estlett.5c00284
  title: MoleTrans
evidence_spans:
- MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_moletrans_cq
    doi: 10.1021/acs.estlett.5c00284
    title: MoleTrans
  dedup_kept_from: coll_moletrans_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.estlett.5c00284
  all_source_dois:
  - 10.1021/acs.estlett.5c00284
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dom-chemodiversity-characterization

## Summary

Characterize molecular diversity and transformation networks in dissolved organic matter (DOM) by computing pairwise mass differences from formula-assigned FT-ICR MS datasets, clustering them into transformation groups, and filtering by occurrence thresholds to derive a transformation network. This skill bridges high-resolution mass spectrometry analysis with reactomics-based interpretation of molecular transformations in complex environmental organic mixtures.

## When to use

Apply this skill when you have a formula-assigned FT-ICR MS dataset (molecular formulas already assigned to individual mass features) and seek to understand the chemodiversity landscape and transformation relationships within DOM. Use it specifically when the research question targets how common functional group gains/losses or metabolic modifications relate across the sample, or when you need to filter spurious mass differences from the full pairwise transformation space to focus on biologically or chemically plausible transformations.

## When NOT to use

- Input is already a feature table without assigned molecular formulas — this skill requires formula-level data, not just m/z and intensity.
- The research goal is compound-level annotation or structural elucidation of individual masses — use targeted fragmentation, NMR, or chromatographic methods instead.
- The DOM dataset lacks sufficient formula assignments or mass measurement accuracy — formula assignment errors will propagate directly into spurious transformation pairs.

## Inputs

- Formula-assigned FT-ICR MS dataset (one row per mass feature with assigned molecular formula and intensity or abundance)
- Known mass-shift reference library (optional but recommended; gains/losses for common functional groups)
- Minimum occurrence threshold parameter (positive integer; default or user-specified)

## Outputs

- Transformation network table (rows: transformation pairs; columns: mass difference, associated formulas, transformation type, frequency count)
- Clustered transformation groups (keyed by mass-shift value or functional group category)
- Chemodiversity metrics or summary statistics (e.g., unique transformations, transformation frequency distribution)

## How to apply

Load the formula-assigned DOM dataset from FT-ICR MS analysis into MoleTrans or equivalent calculation framework. Compute all pairwise mass differences between assigned molecular formulas across the dataset. Identify and cluster these mass differences into transformation groups by matching them to known mass-shift patterns (e.g., gains or losses of common functional groups or metabolic modifications such as oxidation, methylation, or sulfation). Count the frequency and co-occurrence of each transformation pair within the sample. Apply a minimum occurrence threshold (specifics depend on sample size and noise profile) to remove spurious mass differences and retain only transformation pairs that exceed the threshold. Export the final transformation network as a table containing mass differences, associated formulas, transformation types, and frequency counts for visualization and downstream analysis.

## Related tools

- **MoleTrans** (Browser-based webtool for post-analysis and data mining on formula-assigned FT-ICR MS datasets; provides source code for main calculation functions and algorithms for transformation network derivation, clustering, and frequency-based filtering) — https://github.com/JibaoLiu/MoleTrans

## Evaluation signals

- Transformation pair frequency distribution is non-zero only for mass differences that match known metabolic or chemical modifications; no singleton or near-zero-frequency pairs remain after filtering.
- Co-occurrence counts sum correctly across transformation groups and aggregate to total pairwise comparisons expected from the input dataset size.
- Exported transformation network table is consistent with input formula set: all formulas cited in transformation pairs are present in the original dataset; no formulas are duplicated or out of order.
- Minimum occurrence threshold is applied uniformly; all rows in the final table meet or exceed the threshold; no spurious low-frequency pairs are retained.
- Transformation types are semantically meaningful and map to known functional group gains/losses (e.g., +CH₂, +O, –H₂O); no unintelligible or anomalous mass shifts appear.

## Limitations

- Formula assignment errors in the input FT-ICR MS dataset propagate directly into the transformation network; false positives and negatives depend critically on initial mass calibration and formula assignment accuracy.
- The skill requires a priori knowledge of expected mass-shift patterns; omitted or misspecified functional group modifications will be missed or misclassified.
- Minimum occurrence threshold is user-defined; no automatic method is provided in the article to select an optimal threshold; underestimation retains noise, overestimation discards rare but meaningful transformations.
- MoleTrans can only partially support combined analysis on compound-annotated results from mass spectrometry approaches other than FT-ICR MS; integration with other MS platforms may be incomplete.
- The skill is optimized for FT-ICR MS; applicability to lower-resolution MS data (e.g., orbitrap, Q-TOF) depends on formula assignment quality and may degrade.

## Evidence

- [other] Load the formula-assigned DOM dataset (e.g., from FT-ICR MS analysis with molecular formulas assigned to each mass feature). 2. Compute all pairwise mass differences between assigned formulas across the dataset. 3. Identify and cluster mass differences into transformation groups based on known mass-shift patterns (e.g., gains/losses of common functional groups or metabolic modifications). 4. Count frequency and co-occurrence of each transformation pair within the sample. 5. Filter transformation pairs by minimum occurrence threshold to remove spurious mass differences. 6. Export the final transformation network as a table with mass differences, associated formulas, transformation types, and frequency counts.: "Compute all pairwise mass differences between assigned formulas across the dataset. 3. Identify and cluster mass differences into transformation groups based on known mass-shift patterns (e.g.,"
- [other] MoleTrans provides source code for main calculation functions and algorithms that enable post-analysis and data mining on formula-assigned datasets from FT-ICR MS, which supports reactomics-based analysis of molecular transformations in complex organic mixtures.: "MoleTrans provides source code for main calculation functions and algorithms that enable post-analysis and data mining on formula-assigned datasets from FT-ICR MS, which supports reactomics-based"
- [readme] MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS. Alternatively, it can partialy support the combined analysis on the compound annotated results based on other mass spectrometry.: "MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS. Alternatively, it can partialy support the combined analysis on the compound annotated"
