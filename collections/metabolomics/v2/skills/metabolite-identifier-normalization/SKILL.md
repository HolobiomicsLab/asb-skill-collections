---
name: metabolite-identifier-normalization
description: Use when your metabolomics dataset contains compound identifiers in mixed
  formats (chemical names, InChI strings, InChIKey hashes, or SMILES notation) and
  you need a single canonical identifier to enable meta-analysis across multiple studies
  or to avoid counting the same metabolite twice under.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0599
  tools:
  - R
  - webchem
  - amanida
  - PubChem
  - KEGG
  - enrichmet
  - readr
  - readxl
  - dplyr
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
- doi: 10.1101/2025.08.28.672951v2
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted
  meta-analysis in R
- the package will retrieve the PubChem ID from the ID using `webchem`
- This vignette illustrates `Amanida` R package, which contains a collection of functions
  for computing a weighted meta-analysis
- simplifies pathway enrichment analysis by allowing the complete workflow to be executed
  through a single R function call
- curated KEGG data for enrichment using Fisher's Exact Test
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_amanida_cq
    doi: 10.1093/bioinformatics/btab591
    title: Amanida
  - build: coll_enrichmet_cq
    doi: 10.1101/2025.08.28.672951v2
    title: EnrichMET
  dedup_kept_from: coll_amanida_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab591
  all_source_dois:
  - 10.1093/bioinformatics/btab591
  - 10.3390/metabo13121167
  - 10.1101/2025.08.28.672951v2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-identifier-normalization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert multiple chemical identifier formats (chemical name, InChI, InChIKey, SMILES) into a canonical standardized nomenclature using PubChem as the reference database, and detect and remove duplicate entries. This skill enables harmonization across metabolomics studies that report compounds using heterogeneous identifier schemes.

## When to use

Apply this skill when your metabolomics dataset contains compound identifiers in mixed formats (chemical names, InChI strings, InChIKey hashes, or SMILES notation) and you need a single canonical identifier to enable meta-analysis across multiple studies or to avoid counting the same metabolite twice under different names.

## When NOT to use

- Input identifiers are already standardized to a single format (e.g., all PubChem IDs or all SMILES) and no duplicate detection is needed.
- Metabolites in your study are not present in PubChem (e.g., novel synthetic compounds, plant metabolites with limited database coverage).
- Your analysis workflow does not require a canonical identifier across multiple studies (single-study analysis with internally consistent naming).

## Inputs

- R data frame with compound identifier column (supported formats: chemical name, InChI, InChIKey, SMILES)
- amanida data frame object (output from amanida_read)

## Outputs

- harmonized identifier table with PubChem ID as canonical identifier
- duplicate detection report (compounds flagged as redundant entries)
- enriched metadata table (if comp.inf = TRUE): PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank

## How to apply

Load your metabolite identifiers using the amanida_read function in R, specifying the column containing compound identifiers (chemical name, InChI, InChIKey, or SMILES). Call check_names on the resulting data frame to query PubChem via the webchem R package, which converts each heterogeneous identifier to its corresponding PubChem ID. The function automatically compares retrieved PubChem IDs across the full dataset to identify duplicates (same compound reported under different names) and retains only unique PubChem IDs, preserving one record per metabolite. Optionally set comp.inf = TRUE to retrieve additional compound descriptors (Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank) from PubChem for enrichment.

## Related tools

- **amanida** (R package providing check_names function for identifier harmonization via PubChem integration) — https://github.com/mariallr/amanida
- **webchem** (R package that queries PubChem API to retrieve PubChem IDs and compound metadata from multiple identifier formats)
- **PubChem** (Reference chemical database providing canonical PubChem IDs and compound descriptors)

## Examples

```
datafile <- amanida_read('metabolites.csv', mode = 'quan', c('Compound Name', 'P-value', 'Fold-change', 'N total', 'References'), separator=';'); datafile_harmonized <- check_names(datafile, comp.inf = TRUE)
```

## Evaluation signals

- All compounds in the harmonized output have a valid PubChem ID assigned; no missing identifiers for compounds present in PubChem.
- Row count of harmonized table ≤ input row count (at minimum no increase; duplicates removed or merged).
- Duplicate detection report identifies instances where different input identifiers map to the same PubChem ID (e.g., 'aspirin' and 'acetylsalicylic acid' both resolve to PubChem ID 2244).
- Enriched metadata columns (Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank) are populated where available in PubChem; missing values indicate compounds not fully indexed in PubChem.
- Consistency check: re-querying the same input identifiers produces identical PubChem ID assignments.

## Limitations

- Metabolites not indexed in PubChem (novel compounds, rare natural products, study-specific synthetic molecules) cannot be harmonized and will fail to retrieve a PubChem ID.
- Identifier harmonization depends on PubChem's structure matching algorithms; similar but chemically distinct compounds or stereoisomers may be mismatched if PubChem's matching is imperfect.
- Webchem queries are internet-dependent; network failures or PubChem API downtime will halt the harmonization process.
- Chemical name strings are ambiguous and may match multiple compounds; harmonization accuracy is highest for unambiguous identifiers like InChIKey or SMILES.
- Deprecated or removed entries in PubChem may cause retrieval failures for identifiers that were historically valid.

## Evidence

- [intro] identifier_format_conversion: "The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common nomenclature, PubChem ID"
- [intro] duplicate_detection_workflow: "The identifier harmonization is implemented via the check_names function, which searches chemical identifiers in PubChem format (chemical name, InChI, InChIKey, SMILES) using the webchem package to"
- [intro] metadata_enrichment_output: "Results will return the following information: PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank"
- [methods] canonical_identifier_retention: "Retain unique PubChem IDs and remove redundant entries, preserving one record per unique metabolite"
- [readme] readme_check_names_invocation: "The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common nomenclature using `webchem` package"
- [readme] readme_comp_inf_parameter: "Selecting the option `comp.inf = T` the package need the previous use of `check_names`. Then using PubChem ID duplicates are checked"
