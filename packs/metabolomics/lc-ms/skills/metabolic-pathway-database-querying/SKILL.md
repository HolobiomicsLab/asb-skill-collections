---
name: metabolic-pathway-database-querying
description: Use when you have a ranked list of metabolite identifiers (PubChemCIDs, KEGG IDs, or chemical names) from differential abundance or ANOVA testing and need to determine which metabolic pathways are overrepresented or enriched among the most significant features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0188
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0092
  tools:
  - clusterProfiler
  - margheRita
  - R
  - ComplexHeatmap
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- margheRita implements both Over Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA), based on clusterProfiler
- The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
- The R package margheRita addresses the complete workflow
- The R package margheRita
- The function `h_map()` provides heatmaps based on package ComplexHeatmap
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  dedup_kept_from: coll_margherita_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.06.20.599545v1
  all_source_dois:
  - 10.1101/2024.06.20.599545v1
  - 10.1101/2024.06.20.599545
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolic-pathway-database-querying

## Summary

Query metabolic pathway databases (KEGG, Reactome) with a set of metabolite identifiers (PubChemCIDs or chemical names) to identify which biochemical pathways are represented, annotated, and statistically enriched within your detected feature set. This skill bridges mass spectrometry-derived metabolite lists to curated biological pathway knowledge.

## When to use

You have a ranked list of metabolite identifiers (PubChemCIDs, KEGG IDs, or chemical names) from differential abundance or ANOVA testing and need to determine which metabolic pathways are overrepresented or enriched among the most significant features. Typical trigger: you have extracted the top N metabolites by q-value or p-value and want to move from feature-level to pathway-level biological interpretation.

## When NOT to use

- Your metabolite identifiers are not reliably mapped to a standard database (PubChemCID, KEGG ID, or chemical name); ORA requires precise, unambiguous identifiers.
- Your feature set is very small (< 5 significant metabolites) or nearly all detected metabolites are significant; ORA power and interpretation degrade when the query set is not substantially smaller than the universe.
- You have no access to curated metabolic pathway databases or margheRita's spectral library; the skill requires a pre-built mapping of metabolites to pathways.

## Inputs

- PubChemCID list from significant metabolites (e.g., q-value < 1e-9)
- Complete metabolite PubChemCID universe (all detected features)
- Metabolite-to-pathway annotation database (KEGG, Reactome, or margheRita internal library)
- Statistical significance thresholds (q-value or p-value cutoff)

## Outputs

- Enriched pathway table with pathway names, descriptions, adjusted p-values, and effect sizes
- Barplot visualization ranked by −log10(adjusted p-value)
- Filtered pathway set meeting p-value and size thresholds

## How to apply

Define your metabolite universe (all detected metabolites in the experiment) and your query set (e.g., features with q-value < 1e-9 from ANOVA). Map each metabolite to its PubChemCID or KEGG ortholog identifiers. Use over-representation analysis (ORA) via clusterProfiler to test whether the query set is significantly enriched in specific pathways relative to the universe, accounting for pathway size and multiple testing. Filter enriched pathways by adjusted p-value threshold (commonly p.adjust < 0.05) and minimum pathway size (e.g., ≥2 metabolites detected) to focus on robust, biologically interpretable enrichments. Visualize results as a ranked barplot of pathway names by −log10(adjusted p-value) to communicate effect size and significance.

## Related tools

- **clusterProfiler** (Executes over-representation analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA) to test for significant pathway enrichment; provides statistical testing, p-value adjustment, and filtering.)
- **margheRita** (R package wrapper that implements ORA/MSEA on top of clusterProfiler; provides metabolite spectral library, PubChemCID mapping, and pathway database integration tailored to LC-MS/MS workflows.) — https://github.com/emosca-cnr/margheRita
- **ComplexHeatmap** (Optional visualization of pathway enrichment results as heatmaps showing metabolite–pathway membership and abundance patterns.)
- **R** (Scripting and statistical environment for orchestrating ORA workflow, filtering, and visualization.)

## Evaluation signals

- Enriched pathways have adjusted p-value ≤ 0.05 and contain ≥2 detected metabolites; no spurious single-metabolite or high-p-value pathways appear in final results.
- Pathway counts and metabolite overlap are internally consistent: sum of metabolites across top pathways should be ≤ |query set| × average pathway size.
- Barplot visualization shows monotonically decreasing −log10(adjusted p-value) left to right; effect sizes are biologically plausible (e.g., amino acid metabolism, urea cycle, or lipid pathways for urine data).
- Metadata and filtering parameters (significance threshold, pathway size min, p-adjust method) are documented and reproducible; re-running with identical inputs yields identical results.
- Query set and universe cardinalities are reported; ORA assumptions verified (e.g., query ⊂ universe, no duplicates).

## Limitations

- ORA power depends on accurate PubChemCID or chemical name mapping; misidentified or unmapped metabolites will be silently excluded, biasing results if missing features cluster in specific pathways.
- Pathway enrichment is sensitive to pathway size and annotation completeness; large, well-curated pathways (e.g., central carbon metabolism) may dominate, while small or recently discovered pathways may be underrepresented.
- Multiple testing corrections (e.g., Benjamini–Hochberg) are necessary to control false discovery, especially when testing against large pathway databases; p-value thresholds should be pre-registered or clearly justified.
- ORA does not account for pathway crosstalk, metabolite connectivity, or quantitative effect sizes (e.g., fold-change); it reports only representation counts and Fisher's exact test p-values.
- Database-dependent: KEGG, Reactome, and margheRita's internal libraries may differ in pathway definitions, metabolite coverage, and curation; results may not be directly comparable across databases or tool versions.

## Evidence

- [other] Extract PubChemCIDs corresponding to metabolite features meeting the most stringent ANOVA significance threshold from the Urine dataset (both RP_NEG and RP_POS polarities). Define the metabolic universe as all metabolites detected across the full Urine dataset. Execute over-representation analysis (ORA) using clusterProfiler with the significant PubChemCIDs queried against standard metabolic pathway databases (e.g., KEGG, Reactome).: "Execute over-representation analysis (ORA) using clusterProfiler with the significant PubChemCIDs queried against standard metabolic pathway databases (e.g., KEGG, Reactome)."
- [other] Filter enriched pathways by adjusted p-value and pathway size thresholds to identify robust enrichments. Generate a barplot visualization of top enriched pathways ranked by -log10(adjusted p-value) and export the results table.: "Filter enriched pathways by adjusted p-value and pathway size thresholds to identify robust enrichments."
- [intro] margheRita implements both Over Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA), based on clusterProfiler: "margheRita implements both Over Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA), based on clusterProfiler"
- [intro] pathway analysis based on ORA and MSEA over various databases: "pathway analysis based on ORA and MSEA over various databases"
- [other] Over Representation Analysis (ORA) of the most significant ANOVA features (q-value < 1e-9) from the Urine dataset identified enriched pathways represented in a table with pathway descriptions and visualization as a barplot.: "Over Representation Analysis (ORA) of the most significant ANOVA features (q-value < 1e-9) from the Urine dataset identified enriched pathways"
