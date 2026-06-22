---
name: transformation-classification-biotic-abiotic
description: Use when after mass-difference network generation has matched pairwise peak mass differences to a reference biochemical transformation key with mass error ≤1 ppm, and you need to distinguish metabolic transformations driven by microbial activity from those arising from non-biological chemical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3766
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MetaboDirect
  - Cytoscape
  - KEGG database
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# transformation-classification-biotic-abiotic

## Summary

Classify matched mass-difference transformations detected in FT-ICR MS data as either biotic (microbial metabolic) or abiotic (chemical/environmental) based on prior categorization in a reference biochemical transformation key. This step anchors the interpretation of molecular transformation networks to biological process origin.

## When to use

After mass-difference network generation has matched pairwise peak mass differences to a reference biochemical transformation key with mass error ≤1 ppm, and you need to distinguish metabolic transformations driven by microbial activity from those arising from non-biological chemical reactions or environmental processes. Use this skill when your research question separates microbial metabolism from abiotic chemical weathering or degradation pathways.

## When NOT to use

- Input transformations have not yet been matched to a reference key or mass-matching step was not performed with ≤1 ppm error tolerance.
- Reference biochemical transformation key is unavailable or does not contain biotic/abiotic labels for the detected transformation types.
- Analysis goal is purely structural network analysis (e.g., centrality, modularity) without interpretation of metabolic origin — classification adds no value.

## Inputs

- matched transformations table (source peak m/z, target peak m/z, transformation type, mass error in ppm)
- reference biochemical transformation key (transformation type → reference mass difference and biotic/abiotic label)

## Outputs

- edge CSV file with transformation metadata including biotic/abiotic classification for each edge
- transformation frequency statistics stratified by biotic vs. abiotic class
- summary counts of biotic and abiotic transformations per sample

## How to apply

For each matched transformation (source peak m/z → target peak m/z with assigned transformation type), consult the reference biochemical transformation key to retrieve the prior biotic/abiotic classification assigned to that transformation type. Retain this classification in the edge CSV output alongside transformation metadata (source m/z, target m/z, mass error). The classification is deterministic: each reference transformation entry carries a fixed biotic or abiotic label. No statistical threshold or re-inference is applied; the classification propagates from the reference key. Rationale: biotic transformations (e.g., methylation, acetylation, hydroxylation) are signatures of enzymatic pathways in active microbial communities, while abiotic transformations reflect non-enzymatic reactions. This distinction enables hub-metabolite analysis and network topology interpretation specific to metabolic state.

## Related tools

- **MetaboDirect** (End-to-end pipeline that integrates transformation network generation, biotic/abiotic classification, and Cytoscape export) — https://github.com/Coayala/MetaboDirect
- **Cytoscape** (Network visualization and analysis tool that imports node and edge CSV files with classification attributes for downstream topology and hub analysis)
- **KEGG database** (Reference source for biochemical transformations and reaction classifications that can populate the reference transformation key)

## Evaluation signals

- Edge CSV output contains no null or unassigned biotic/abiotic labels for any matched transformation.
- All matched transformations present in the edge CSV have a corresponding entry in the reference transformation key; no transformation type is orphaned.
- Biotic + abiotic transformation counts per sample sum to the total number of matched transformations in that sample.
- Cytoscape-imported network nodes and edges display biotic/abiotic labels as visual attributes (e.g., edge color or style) without import errors.
- Sample-level transformation statistics (total biotic, total abiotic, ratio) align with manual spot-check of edge CSV rows stratified by classification.

## Limitations

- Classification accuracy depends entirely on the completeness and correctness of the reference biochemical transformation key; unknown or misclassified transformations in the key propagate into results.
- Ambiguous transformations that could arise from either biotic or abiotic pathways are assigned a single fixed label; no confidence score or probabilistic assignment is supported.
- Reference key must be curated and maintained externally; MetaboDirect does not validate or update transformation classifications based on novel literature or experimental evidence.
- Mass-difference matching is sensitive to unassigned peaks and formula assignment errors upstream; mismatches due to poor peak quality or formula error will produce false or missing transformations before classification is applied.

## Evidence

- [other] Classify matched transformations as biotic or abiotic based on prior categorization.: "Classify matched transformations as biotic or abiotic based on prior categorization."
- [abstract] MetaboDirect is uniquely able to automatically generate biochemical transformation networks based on mass differences.: "MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences (mass difference network‑based approach)"
- [other] The networks are designed to quantify differences in microbial metabolic pathways and identify hub metabolites involved in many reactions.: "the networks designed to quantify differences in microbial metabolic pathways and identify hub metabolites involved in many reactions"
- [other] Match each mass difference to the reference biochemical transformation key, retaining transformations with mass error ≤1 ppm against reference values.: "Match each mass difference to the reference biochemical transformation key, retaining transformations with mass error ≤1 ppm against reference values."
- [other] Edge CSV files containing putative transformations for each sample.: "Generate edge CSV files containing putative transformations (source peak m/z, target peak m/z, transformation type, error) for each sample."
