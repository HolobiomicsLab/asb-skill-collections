---
name: lipid-class-annotation-and-parsing
description: Use when immediately after loading raw lipid identifiers from LipidSearch or LIQUID output, or when importing lipidomic data from the Metabolomics Workbench.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3407
  tools:
  - ADViSELipidomics
  - limma
  - edgeR
  - ComBat
  - LIPID MAPS
  - LipidSearch
  - LIQUID
derived_from:
- doi: 10.1093/bioinformatics/btac706
  title: ADViSELipidomics
evidence_spans:
- ADViSELipidomics can normalize the data matrix, providing absolute values of concentration per lipid and sample
- ADViSELipidomics is a novel Shiny app for the preprocessing, analysis, and visualization of lipidomics data.
- allows the identification of differentially abundant lipids in simple and complex experimental designs
- dealing with batch effect correction.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_adviselipidomics_cq
    doi: 10.1093/bioinformatics/btac706
    title: ADViSELipidomics
  dedup_kept_from: coll_adviselipidomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac706
  all_source_dois:
  - 10.1093/bioinformatics/btac706
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-class-annotation-and-parsing

## Summary

Extract and standardize lipid structural metadata (class, chain length, saturation) from raw lipid identifiers using LIPID MAPS classification. This skill enables downstream filtering, visualization, and interpretation of lipidomics results by enriching individual lipid hits with canonical structural annotations.

## When to use

Apply this skill immediately after loading raw lipid identifiers from LipidSearch or LIQUID output, or when importing lipidomic data from the Metabolomics Workbench. Use it before differential abundance testing or visualization if you need to group lipids by class, chain properties, or saturation state, or if your downstream analysis requires annotated lipid metadata columns in the results table.

## When NOT to use

- Lipid identifiers are already in a pre-annotated format with class and structural metadata present
- The analysis goal does not require class-level or structural grouping (e.g., single-lipid biomarker discovery)
- Lipid naming follows a non-standard convention that cannot be mapped to LIPID MAPS (check compatibility before proceeding)

## Inputs

- raw lipid identifier strings from LipidSearch or LIQUID output
- lipid abundance matrix with lipid IDs as row names
- Metabolomics Workbench lipidomic experiment data

## Outputs

- annotated lipid table with columns: lipid_id, lipid_class, chain_length, saturation, other_structural_features
- lipid abundance matrix with enriched metadata columns
- parsed lipid class summary (unique classes and their frequencies)

## How to apply

Parse each lipid identifier string using LIPID MAPS classification rules to extract canonical attributes: lipid class (e.g., PC, PE, TAG), chain length (e.g., C18), saturation (number of double bonds), and regioisomer information where available. Store these annotations as separate columns in the lipid abundance matrix or results table. The rationale is that LIPID MAPS provides a curated, standardized nomenclature that allows aggregation of lipid species across naming conventions and enables class-level statistical comparisons. Validation occurs by confirming that all lipid identifiers successfully map to at least one LIPID MAPS class and that no identifiers are left unparsed.

## Related tools

- **LIPID MAPS** (Provides standardized lipid classification nomenclature and parsing rules for extracting class, chain length, and saturation from lipid identifiers)
- **LipidSearch** (Source of raw lipid identifiers that are parsed and annotated using LIPID MAPS classification in ADViSELipidomics)
- **LIQUID** (Alternative source of raw lipid identifiers compatible with LIPID MAPS parsing in ADViSELipidomics)
- **ADViSELipidomics** (Implements lipid parsing and annotation workflow using LIPID MAPS classification; outputs annotated results with lipid class, chain length, saturation metadata) — https://github.com/ShinyFabio/ADViSELipidomics

## Evaluation signals

- All input lipid identifiers successfully map to a LIPID MAPS class; zero unparseable identifiers remain
- Extracted chain length and saturation values are numeric and fall within biologically plausible ranges (e.g., chain length ≥ 6 carbons, saturation ≤ chain length / 2)
- Lipid class annotations are consistent with the source (e.g., identifiers labeled as 'PC' all parse to phosphatidylcholine class)
- Output table contains expected columns: lipid_id, lipid_class, chain_length, saturation, and batch-corrected group means are retained from upstream steps
- Class-level summaries show expected lipid diversity (multiple classes present if input is from complex lipid extracts; no class dominates 100% of entries)

## Limitations

- Parsing depends on standardized LIPID MAPS nomenclature; identifiers from non-standard or proprietary naming schemes may not parse correctly
- Regioisomer and stereoisomer information may be lost or ambiguous during parsing if the input identifier does not explicitly encode position or stereochemistry
- Chain length and saturation extraction assumes standard shorthand (e.g., 'C18:2'); non-standard notations (e.g., chemical IUPAC names) require custom pre-processing
- The README does not specify whether ADViSELipidomics auto-detects lipid identifier format or requires user specification of the source tool (LipidSearch vs LIQUID); manual format selection may be needed

## Evidence

- [readme] ADViSELipidomics extracts information by parsing lipid species (using LIPID MAPS classification): "ADViSELipidomics extracts information by parsing lipid species (using LIPID MAPS classification)"
- [readme] It copes with the outputs from LipidSearch and LIQUID for lipid identification and quantification: "It copes with the outputs from LipidSearch and LIQUID for lipid identification and quantification"
- [other] Annotate results with lipid class, chain length, saturation, and batch-corrected mean abundances per group: "Annotate results with lipid class, chain length, saturation, and batch-corrected mean abundances per group"
- [intro] Parsing lipid species using LIPID MAPS classification is a workflow step in ADViSELipidomics: "Parsing lipid species using LIPID MAPS classification"
