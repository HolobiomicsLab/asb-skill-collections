---
name: chemical-descriptor-retrieval
description: Use when after harmonizing compound identifiers to PubChem IDs (e.g.,
  via check_names function).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2815
  - http://edamontology.org/topic_3172
  tools:
  - R
  - webchem
  - amanida
  - PubChem
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted
  meta-analysis in R
- the package will retrieve the PubChem ID from the ID using `webchem`
- This vignette illustrates `Amanida` R package, which contains a collection of functions
  for computing a weighted meta-analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_amanida_cq
    doi: 10.1093/bioinformatics/btab591
    title: Amanida
  dedup_kept_from: coll_amanida_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab591
  all_source_dois:
  - 10.1093/bioinformatics/btab591
  - 10.3390/metabo13121167
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Chemical Descriptor Retrieval

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Retrieve standardized chemical descriptors (molecular formula, molecular weight, SMILES, InChIKey, and cross-database identifiers) for metabolites from public chemical databases using canonical identifiers. This enriches harmonized compound records with physicochemical and structural properties needed for comparative metabolomics meta-analysis.

## When to use

Apply this skill after harmonizing compound identifiers to PubChem IDs (e.g., via check_names function). Use when your metabolomics dataset requires enrichment with standardized chemical properties for cross-study comparison, or when you need to retrieve external database mappings (KEGG, ChEBI, HMDB, DrugBank) for compounds already converted to PubChem nomenclature.

## When NOT to use

- Input metabolites have not yet been harmonized to a canonical identifier system (run check_names first)
- Your study focuses only on relative fold-change and p-value combination and does not require chemical property metadata
- PubChem does not have records for your compounds (e.g., novel synthetic intermediates or non-standard metabolites with no public database coverage)

## Inputs

- Harmonized metabolite table with PubChem IDs as canonical identifiers
- Vector of PubChem IDs (numeric or character)
- Amanida data object after check_names harmonization

## Outputs

- Enriched metabolite table with columns: PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, DrugBank
- S4 amanida result object with descriptor data accessible via @stat slot

## How to apply

After successful identifier harmonization to PubChem IDs, invoke the amanida package's comp.inf parameter (set to TRUE) during meta-analysis computation. The webchem R package queries PubChem for each PubChem ID and retrieves a fixed set of descriptors: Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG ID, ChEBI ID, HMDB ID, and DrugBank ID. Results are appended as new columns to the harmonized metabolite table. This step is optional but recommended when integrating results across multiple metabolomics studies that use different identifier systems, as it enables standardization and cross-database traceability.

## Related tools

- **webchem** (Queries PubChem database via HTTP API to retrieve chemical descriptors for each PubChem ID)
- **amanida** (R package that wraps webchem queries and integrates chemical descriptors into meta-analysis workflow via comp.inf parameter) — https://github.com/mariallr/amanida
- **PubChem** (Public chemical database queried by webchem to fetch standardized descriptors and cross-database identifiers) — https://pubchem.ncbi.nlm.nih.gov/

## Examples

```
amanida_result <- compute_amanida(datafile, comp.inf = TRUE)
```

## Evaluation signals

- Output table has exactly 9 columns: PubChem ID + 8 descriptor columns (Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, DrugBank)
- No rows are dropped during descriptor retrieval (row count equals input PubChem ID count)
- All retrieved SMILES and InChIKey values conform to standard chemical notation (InChIKey is 27 alphanumeric characters; SMILES contains only valid atom/bond symbols)
- Cross-database IDs (KEGG, ChEBI, HMDB, DrugBank) are non-empty strings or NA for compounds without external links; no malformed values
- Molecular Weight values are positive numeric floats; Molecular Formula strings match standard Hill system notation

## Limitations

- Descriptor retrieval depends on PubChem coverage: compounds not in PubChem will have missing (NA) values for all descriptors
- The webchem package queries PubChem HTTP API sequentially, which can be slow for large compound sets (thousands of metabolites); no batch retrieval optimization described in the article
- Cross-database IDs (KEGG, ChEBI, HMDB, DrugBank) are only as complete as PubChem's internal mappings; gaps or outdated mappings may occur
- Retrieval is performed only at the time of analysis; descriptors are static snapshots and do not auto-update if PubChem records change

## Evidence

- [intro] Results will return the following information: PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank: "Results will return the following information: PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank"
- [readme] Selecting the option `comp.inf = T` the package need the previous use of `check_names`. Then using PubChem ID duplicates are checked. Results are returned including the following information: PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank.: "Selecting the option `comp.inf = T` the package need the previous use of `check_names`. Then using PubChem ID duplicates are checked. Results are returned including the following information: PubChem"
- [intro] If you select the option `comp.inf = T` the package will retrieve the PubChem ID from the ID using `webchem`.: "If you select the option `comp.inf = T` the package will retrieve the PubChem ID from the ID using `webchem`"
- [other] The process optionally retrieves additional compound descriptors (Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank) from public databases.: "The process optionally retrieves additional compound descriptors (Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank) from public databases."
