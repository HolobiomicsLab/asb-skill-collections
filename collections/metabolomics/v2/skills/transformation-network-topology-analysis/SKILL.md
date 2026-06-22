---
name: transformation-network-topology-analysis
description: Use when when you have pre-processed FT-ICR MS peak lists with assigned molecular formulas and wish to move beyond univariate chemical composition analysis to understand metabolic transformation pathways and hub metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0659
  - http://edamontology.org/topic_3407
  tools:
  - MetaboDirect
  - Python (NumPy, pandas)
  - R (vegan package)
  - Cytoscape
  - FT-ICR MS
  - KEGG database
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- Molecular transformation networks for each sample (mass difference network-based approach) are generated in this step
- The MetaboDirect pipeline consists of 6 major steps/categories (Fig. 1)
- The MetaboDirect pipeline was developed in Python 3.8 and requires the Python dependencies NumPy, pandas
- developed in Python 3.8 [38] and R 4.0.2 [39]
- Networks are then constructed using Cytoscape and colored based on their molecular class
- Networks are then constructed using Cytoscape [79] and colored based on their molecular class.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect_cq
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect_cq
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

# transformation-network-topology-analysis

## Summary

Construct and analyze biochemical transformation networks from FT-ICR MS data by identifying mass differences between detected peaks, then compute topological metrics (degree distribution, component count, hub identification) to characterize metabolic connectivity and transformation pathways in complex organic mixtures.

## When to use

When you have pre-processed FT-ICR MS peak lists with assigned molecular formulas and wish to move beyond univariate chemical composition analysis to understand metabolic transformation pathways and hub metabolites. Use this skill when you need to identify which masses are connected by biologically or chemically plausible transformations, and when you want to rank metabolites by their centrality in the transformation network.

## When NOT to use

- Input peak list lacks reliable molecular formula assignments; mass differences will not map to interpretable biochemical transformations.
- Sample is a pure standard or synthetic mixture with known structure; transformation network topology is uninformative and univariate formula/class composition is sufficient.
- FT-ICR MS mass accuracy is degraded (>1 ppm systematic error); false-positive and false-negative transformation calls will corrupt the network.

## Inputs

- Peak m/z list (CSV format, one row per detected mass with intensity)
- Molecular formula assignments (one formula per m/z)
- Biochemical transformation reference key (KEGG-derived, keyed by mass difference and transformation name)
- Error tolerance threshold (ppm; recommended ≤1)

## Outputs

- Edge table (CSV: source_mz, target_mz, mass_difference, transformation_name, biotic|abiotic classification)
- Node table (CSV: all detected m/z values, molecular class assignments)
- Network statistics (degree distribution, connected component count, hub metabolite rankings)
- Cytoscape-compatible network files (.sif, .noa, .eda formats for import and visualization)

## How to apply

Load the peak m/z list and molecular formulas for each sample as CSV. Compute all pairwise mass differences between detected peaks using vectorized subtraction. Match each mass difference against a pre-defined biochemical transformation reference key (keyed to KEGG), retaining only matches with ≤1 ppm error tolerance to account for FT-ICR MS ultra-high mass accuracy. Classify retained transformations as biotic or abiotic according to the reference classification. Export edge and node tables in Cytoscape-compatible format, with edges encoding source m/z, target m/z, mass difference, transformation name, and classification. Compute topological statistics including degree distribution (count of incoming/outgoing transformations per node), connected component count, and hub ranking by node degree. The rationale is that mass-difference networks bypass the need for chromatographic separation and isomer disambiguation: two peaks connected by a known biochemical transformation mass difference imply a metabolic pathway, even if their structures are not individually resolved.

## Related tools

- **MetaboDirect** (Automated pipeline that encapsulates all six steps of transformation network analysis: data pre-processing, diagnostics, exploration, chemodiversity, statistical analysis, and transformation network generation with Cytoscape export.) — https://github.com/Coayala/MetaboDirect
- **FT-ICR MS** (Ultra-high mass accuracy instrument (enabling ≤1 ppm error tolerance) that produces the peak m/z list and enables reliable mass difference matching to biochemical transformations.)
- **Cytoscape** (Network visualization and topology analysis tool; MetaboDirect exports edge/node tables in Cytoscape-compatible format (.sif, .noa) for interactive exploration of transformation networks.)
- **Python (NumPy, pandas)** (Vectorized computation of pairwise mass differences and matching against transformation key; core data manipulation for edge/node table generation.)
- **R (vegan package)** (Computation of network topology metrics and diversity indices; supports chemodiversity analysis and statistical assessment of transformation network structure.)
- **KEGG database** (Source of reference biochemical transformation definitions and mass differences; MetaboDirect queries KEGG to populate the transformation key.)

## Examples

```
metabodirect -i sample_peaks.csv -f sample_formulas.csv -t kegg_transformations.csv --ppm_tol 1.0 --output network_output/
```

## Evaluation signals

- Edge table has no null values in source_mz, target_mz, or mass_difference columns; all mass differences fall within ±1 ppm of a reference transformation.
- Node table includes all peaks from the input m/z list and assigns each a molecular class; no missing or duplicate entries.
- Degree distribution is non-degenerate (at least two nodes with degree > 0); isolated nodes (degree = 0) are present only if they failed to match any reference transformation.
- Connected component count is ≤ (number of nodes / 2); large networks should show sub-networks linked by hub metabolites.
- Network statistics (e.g., hub rankings) are reproducible; re-running with identical inputs and ≤1 ppm threshold yields identical edge/node tables.

## Limitations

- FT-ICR MS cannot separate chemical isomers; two different structures with the same m/z and molecular formula will be conflated into a single node, obscuring distinct biochemical pathways.
- Transformation network is deterministic given the reference key; if a genuine biochemical transformation is missing from KEGG or the transformation reference, the corresponding edge will not be generated.
- Mass-difference matching does not account for cofactor stoichiometry, enzymatic specificity, or thermodynamic feasibility; a mass difference matching a reference transformation does not guarantee the reaction occurred in the sample.
- Ion suppression and signal enhancement in direct injection MS can cause peak detection bias, leading to incomplete or skewed transformation networks if low-abundance intermediates are missed.
- Network topology is sample-specific; transformation networks from different samples or different extraction conditions may differ substantially, limiting cross-sample comparative claims.

## Evidence

- [other] nodes represent masses and edges represent the mass differences corresponding to specific biochemical transformations: "nodes represent masses and edges represent the mass differences corresponding to specific biochemical transformations"
- [other] Compute all pairwise mass differences between peaks using vectorized subtraction. 3. Match each mass difference against the pre-defined biochemical transformation key, retaining matches with ≤1 ppm error tolerance.: "Compute all pairwise mass differences between peaks using vectorized subtraction. 3. Match each mass difference against the pre-defined biochemical transformation key, retaining matches with ≤1 ppm"
- [abstract] MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences: "MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences"
- [other] Export edge and node tables formatted for import into Cytoscape; compute and export network statistics (e.g., degree distribution, component count).: "Export edge and node tables formatted for import into Cytoscape; compute and export network statistics (e.g., degree distribution, component count)."
- [intro] FT-ICR MS has evolved during the past two decades into a powerful tool to study the molecular composition of small-molecule organic complex mixtures: "FT-ICR MS has evolved during the past two decades into a powerful tool to study the molecular composition of small-molecule organic complex mixtures"
- [intro] Even though DI-MS has ample coverage and can detect a wide range of compounds (e.g., lipids, sugars, amino acids, or lignin), some drawbacks are its inability to separate chemical isomers: "Even though DI-MS has ample coverage and can detect a wide range of compounds (e.g., lipids, sugars, amino acids, or lignin), some drawbacks are its inability to separate chemical isomers"
