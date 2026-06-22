---
name: mzml-format-validation
description: Use when after downloading an mzML file from a remote repository (e.g., MetaboLights, MassIVE, GNPS) via USI resolution, before attempting to parse it into a spectrum container or visualization dashboard.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0336
  edam_topics:
  - http://edamontology.org/topic_0943
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - pymzML
  - mzML indexer
  - GNPS LCMS Visualization Dashboard
  - MSConvert
  - MS-DIAL
derived_from:
- doi: 10.1038/s41592-021-01339-5
  title: GNPS Dashboard
- doi: 10.1021/acs.analchem.4c00786
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnps_dashboard_cq
    doi: 10.1038/s41592-021-01339-5
    title: GNPS Dashboard
  - build: coll_rapid_qc_ms_cq
    doi: 10.1021/acs.analchem.4c00786
    title: Rapid QC-MS
  dedup_kept_from: coll_gnps_dashboard_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-021-01339-5
  all_source_dois:
  - 10.1038/s41592-021-01339-5
  - 10.1021/acs.analchem.4c00786
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzml-format-validation

## Summary

Validate downloaded mzML files against the mzML XML schema to confirm structural integrity, presence of spectrum list, and indexed offset consistency before loading into analysis pipelines. This ensures data quality and compatibility with downstream spectrum access and metadata retrieval tools.

## When to use

After downloading an mzML file from a remote repository (e.g., MetaboLights, MassIVE, GNPS) via USI resolution, before attempting to parse it into a spectrum container or visualization dashboard. Validation is essential when the source file integrity cannot be assumed or when the file will be used in production analysis workflows.

## When NOT to use

- Input file is already loaded in memory as a spectrum object; re-validation of a parsed object is unnecessary.
- Input file comes from a trusted, validated local cache with documented provenance; skip validation if reproducibility does not depend on fresh verification.
- File format is not mzML (e.g., mzXML, NetCDF, Bruker .d); use format-specific validators instead.

## Inputs

- mzML file (downloaded or local path)
- mzML schema definition (implicit in validator)

## Outputs

- Validation result (pass/fail boolean or report)
- Error log or message (if validation fails)
- Validated mzML file ready for parsing (if validation passes)

## How to apply

Parse the downloaded mzML file using a dedicated mzML validator tool (such as mzML indexer or pymzML parser) to check XML well-formedness, verify the presence and structure of the spectrum list element, and confirm that indexed offset records match the actual byte positions of spectrum entries in the file. If validation fails (malformed XML, missing spectrum list, corrupted offsets), reject the file and re-download. Pass only validated files to downstream spectrum container constructors. The validation step is grounded in the USI resolution workflow where file integrity directly impacts spectrum loading reliability.

## Related tools

- **pymzML** (Parse and validate mzML XML structure; confirm spectrum list presence and indexed offset integrity)
- **mzML indexer** (Validate mzML schema compliance and index offset correctness)
- **GNPS LCMS Visualization Dashboard** (Consume validated mzML files for spectrum visualization and XIC extraction) — https://github.com/Wang-Bioinformatics-Lab/GNPS_LCMSDashboard

## Examples

```
from pymzml.run import Reader; run = Reader('QC07.mzML'); spectra = [s for s in run]; assert len(spectra) > 0, 'No spectra found'
```

## Evaluation signals

- Validator returns no XML parsing errors; file structure conforms to mzML schema.
- Spectrum list element is present and contains at least one spectrum entry with valid index references.
- Indexed byte offsets in the mzML index match actual file positions of spectrum elements when spot-checked.
- File can be successfully loaded into a pymzML container without exceptions; spectrum metadata and scan numbers are accessible.
- Validated file produces consistent chromatogram and spectrum data when visualized in the GNPS LCMS Dashboard or equivalent viewer.

## Limitations

- Validation only confirms syntactic and structural correctness; does not verify semantic correctness (e.g., whether m/z values are physically plausible or whether retention times are monotonic).
- Some validators may not detect all edge cases of corrupt index offsets in very large mzML files; manual spot-checking of index entries is recommended for critical workflows.
- Validation performance may degrade on very large files (>1 GB); consider streaming or sampling-based validation for production pipelines with strict latency requirements.

## Evidence

- [other] Validate the downloaded file against mzML schema using an mzML validator (e.g., mzML indexer or pymzML parser) to confirm XML structure, presence of spectrum list, and indexed offset integrity.: "Validate the downloaded file against mzML schema using an mzML validator (e.g., mzML indexer or pymzML parser) to confirm XML structure, presence of spectrum list, and indexed offset integrity."
- [other] Load the validated mzML file into an mzML spectrum container (e.g., pymzML object or equivalent data structure) to enable downstream spectrum access and metadata retrieval.: "Load the validated mzML file into an mzML spectrum container (e.g., pymzML object or equivalent data structure) to enable downstream spectrum access and metadata retrieval."
