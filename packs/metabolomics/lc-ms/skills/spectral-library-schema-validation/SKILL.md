---
name: spectral-library-schema-validation
description: Use when after harmonizing MS/MS spectra and metadata fields (compound identifiers, adduct annotations, collision energies, instrument types) to a common schema, and before exporting the spectral library to standardized formats (mzML, mzTab, or repository-native format).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - spectraverse-analysis repository
  - spectraverse-analysis
  - matchms
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c06256
  title: Spectraverse
evidence_spans:
- github.com/skinniderlab/spectraverse-analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectraverse_cq
    doi: 10.1021/acs.analchem.5c06256
    title: Spectraverse
  dedup_kept_from: coll_spectraverse_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c06256
  all_source_dois:
  - 10.1021/acs.analchem.5c06256
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-schema-validation

## Summary

Validate preprocessed and harmonized MS/MS spectra and their metadata against a defined schema to ensure consistency, completeness, and conformance before library compilation. This skill detects structural inconsistencies, missing required fields, and format violations that would compromise downstream spectral matching and annotation.

## When to use

Apply this skill after harmonizing MS/MS spectra and metadata fields (compound identifiers, adduct annotations, collision energies, instrument types) to a common schema, and before exporting the spectral library to standardized formats (mzML, mzTab, or repository-native format). Use it to catch schema violations, duplicates, and incomplete annotations before final library release.

## When NOT to use

- Input spectra have not yet been harmonized or standardized to a common metadata schema — apply harmonization first.
- Spectra are already in a pre-curated, vendor-supplied format with guaranteed schema compliance.
- The goal is exploratory analysis of raw, unstructured spectral data rather than production library compilation.

## Inputs

- Harmonized MS/MS spectra in MGF or CSV format with standardized metadata fields
- Metadata schema definition specifying required fields, data types, and valid value ranges
- Compound identifiers (SMILES, InChI, or canonical chemical identifiers)
- Adduct annotations (e.g., [M+H]+, [M-H]−)
- Collision energy values and instrument type labels

## Outputs

- Schema-validated spectral library (filtered MGF, mzML, or mzTab)
- Validation report detailing passed and failed records
- List of removed or flagged spectra with failure reasons
- Deduplicated spectral library ready for export

## How to apply

Execute schema validation as part of the harmonization workflow following metadata field standardization. Define required fields for each spectrum record (precursor m/z, fragment peaks, adduct type, collision energy, instrument identifier, SMILES or InChI identifier) and validate that all records conform to these requirements. Check for consistent data types (numeric vs. string), valid value ranges (e.g., m/z > 0, collision energy within instrument range), and presence of mandatory annotations. Remove or flag spectra that fail validation. This ensures downstream tools (cosine scoring, spectral matching) receive well-formed, complete inputs and prevents propagation of malformed data through subsequent harmonization and deduplication steps.

## Related tools

- **spectraverse-analysis** (Repository containing preprocessing and harmonization code that precedes schema validation; validation is integrated into the harmonization pipeline to remove duplicates and ensure metadata conformance) — https://github.com/skinniderlab/spectraverse-analysis
- **matchms** (Used for spectral preprocessing and metadata repair; schema validation is applied after matchms filtering to ensure coherent annotations) — https://github.com/matchms/matchms

## Examples

```
python run_steps.py --config config/config_step3.json  # Executes schema validation as part of step3, including step3-5_uniq-select.py which removes duplicates based on schema-validated cosine scores
```

## Evaluation signals

- All records in the validated library contain non-null values for mandatory fields (precursor m/z, fragment peaks, adduct type, instrument identifier).
- Numeric fields (m/z, collision energy, intensity values) fall within chemically plausible ranges and match field type expectations.
- Duplicate spectra are identified and removed based on matching compound identity, adduct type, and instrument parameters.
- Validation report shows 0% schema violations in final exported library; any removed spectra are logged with explicit failure reasons.
- Output file passes downstream tool ingestion (e.g., mzML/mzTab parsers accept all records without format errors).

## Limitations

- Schema validation does not detect scientific implausibility (e.g., fragment peaks with m/z > precursor m/z are caught only if the schema explicitly defines that constraint; see step2-7_highfragmass-check.py for this specialized check).
- Validation depends on prior harmonization quality; inconsistently mapped metadata fields (e.g., adduct notation variants not standardized) will pass validation if the schema permits multiple string representations.
- No changelog is available in the repository to track schema evolution or validation rule changes across library versions.
- Duplicate detection relies on cosine similarity scoring (threshold typically >0.7 in step3-4 and step3-5) rather than exact matching, so spectra with minor peak differences may not be flagged.

## Evidence

- [intro] Validate harmonized spectra and metadata against schema requirements and remove duplicates.: "Validate harmonized spectra and metadata against schema requirements and remove duplicates."
- [intro] code used to preprocess and harmonize MS/MS spectra and their associated metadata in the compilation of Spectraverse.: "code used to preprocess and harmonize MS/MS spectra and their associated metadata in the compilation of Spectraverse"
- [other] Harmonize metadata fields (compound identifiers, adduct annotations, collision energies, instrument types) to common schema using repository mapping functions.: "Harmonize metadata fields (compound identifiers, adduct annotations, collision energies, instrument types) to common schema"
- [readme] step3-5_uniq-select.py: Removal of duplicate spectra based on pairwise cosine scores: "step3-5_uniq-select.py: Removal of duplicate spectra based on pairwise cosine scores"
- [other] Export preprocessed and harmonized spectral library in standardized output format (mzML, mzTab, or repository-native format).: "Export preprocessed and harmonized spectral library in standardized output format (mzML, mzTab, or repository-native format)."
