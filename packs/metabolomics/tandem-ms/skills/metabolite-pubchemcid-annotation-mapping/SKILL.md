---
name: metabolite-pubchemcid-annotation-mapping
description: Use when after metabolite annotation has been completed (level-1 confidence via spectral library matching in margheRita or equivalent), and you need to perform pathway enrichment analysis on a subset of significant features (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  tools:
  - clusterProfiler
  - margheRita
  - R
  - ComplexHeatmap
  - PubChem
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

# metabolite-pubchemcid-annotation-mapping

## Summary

Map annotated metabolite features from LC-MS/MS data to PubChemCID identifiers to enable pathway enrichment queries against metabolic databases. This bridges spectral library-based metabolite identification (level-1) to chemical structure identifiers required by pathway analysis tools.

## When to use

After metabolite annotation has been completed (level-1 confidence via spectral library matching in margheRita or equivalent), and you need to perform pathway enrichment analysis on a subset of significant features (e.g., those meeting a q-value or p-value threshold from ANOVA or other statistical tests). The mapping is essential when your statistical result table contains metabolite names or m/z values but lacks PubChemCID entries needed by clusterProfiler or other pathway databases.

## When NOT to use

- Your metabolites are already assigned PubChemCIDs in your annotation table; proceed directly to pathway enrichment.
- Your pathway analysis tool accepts metabolite names or m/z values natively (some tools do; verify tool documentation first).
- The metabolite set is dominated by lipids or other non-standard metabolites not reliably represented in PubChem; consider lipid-specific databases (LipidMaps, HMDB) or hybrid mapping strategies.

## Inputs

- Annotated metabolite feature table with level-1 identifications (metabolite names or chemical synonyms)
- Statistical result table with significance metrics (q-values, p-values, fold-changes) per metabolite
- Complete set of detected metabolites (metabolic universe) for background definition

## Outputs

- Vector or list of PubChemCIDs corresponding to significant metabolites
- Metadata table linking PubChemCID to original metabolite name, m/z, and significance metrics
- Mapping success report (number and percentage of features successfully mapped to CIDs)

## How to apply

Extract the annotated metabolite names or chemical identifiers from your statistical result table (e.g., features with q-value < 1e-9 from ANOVA). Query each metabolite name against PubChem or use a local/cached PubChemCID mapping table provided by margheRita or a synonym resolver to retrieve the corresponding PubChemCID for each feature. Retain only metabolites with successful CID matches; unmappable features should be flagged and excluded from downstream pathway analysis. The resulting vector or list of PubChemCIDs becomes the input 'gene' list for clusterProfiler's ORA function. Document the mapping success rate (fraction of input metabolites that obtained a CID) as a quality metric.

## Related tools

- **margheRita** (Performs metabolite annotation (level-1) from MS-DIAL output and can export annotated features for downstream mapping; provides spectral library matching across multiple chromatographic column types.) — https://github.com/emosca-cnr/margheRita
- **clusterProfiler** (Consumes the PubChemCID list as the 'gene' argument for Over-Representation Analysis (ORA) against metabolic pathway databases (KEGG, Reactome).)
- **PubChem** (Primary chemical structure and CID reference database; queries resolve metabolite names and synonyms to unique PubChemCID integers.)

## Evaluation signals

- Mapping success rate: ≥80% of significant metabolites obtain a valid PubChemCID (track unmappable metabolites and document reasons).
- No duplicate CIDs in the output list (each metabolite name maps to at most one CID).
- All returned CIDs are positive integers matching PubChem's ID format and can be queried via PubChem API or local KEGG/Reactome databases without errors.
- The size of the PubChemCID list matches the size of the input significant metabolites after filtering for successful matches.
- ORA enrichment analysis downstream completes without errors and returns ≥1 significantly enriched pathways (adjusted p-value < 0.05), indicating the CID list is valid and biologically informative.

## Limitations

- Metabolites with multiple chemical names, isomers, or ambiguous annotations may map to incorrect or multiple CIDs; manual curation is recommended for high-stakes analyses.
- PubChem coverage is incomplete for emerging or naturally occurring metabolites; lipids, glycosides, and complex natural products may lack CIDs or have outdated synonymy.
- Mapping relies on exact or fuzzy string matching of metabolite names; typos, non-standard nomenclature, or proprietary compound codes in your feature table will cause mapping failures.
- Some metabolites detected by MS-DIAL may not achieve level-1 confidence (spectral library match); such features cannot be reliably mapped to CIDs and should be excluded before pathway analysis.

## Evidence

- [other] Extract PubChemCIDs corresponding to metabolite features meeting the most stringent ANOVA significance threshold from the Urine dataset: "Extract PubChemCIDs corresponding to metabolite features meeting the most stringent ANOVA significance threshold from the Urine dataset (both RP_NEG and RP_POS polarities)."
- [other] Define the metabolic universe as all metabolites detected across the full Urine dataset: "Define the metabolic universe as all metabolites detected across the full Urine dataset."
- [other] Execute over-representation analysis (ORA) using clusterProfiler with the significant PubChemCIDs queried against standard metabolic pathway databases: "Execute over-representation analysis (ORA) using clusterProfiler with the significant PubChemCIDs queried against standard metabolic pathway databases (e.g., KEGG, Reactome)."
- [readme] metabolite annotation up to level-1, based on in-house spectral libraries as well as freely available libraries: "metabolite annotation up to level-1, based on in-house spectral libraries as well as freely available libraries"
- [other] margheRita implements both Over Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA), based on clusterProfiler: "margheRita implements both Over Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA), based on clusterProfiler"
