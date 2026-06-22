---
name: chemical-coverage-optimization
description: Use when your LC-MS feature table is incomplete or has low chemical coverage because traditional peak extraction algorithms (e.g., standard XCMS workflows) systematically miss features at m/z and retention time positions corresponding to known suspect compounds in your database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R Shiny
  - R Shiny (EISA-EXPOSOME interface)
  - T3DB (compiled database file)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c02697
  title: EISA-EXPOSOME
evidence_spans:
- We provide a Rshiny program for EISA-EXPOSOME
- We provide a Rshiny program for EISA-EXPOSOME, which runs with the interface shown below
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eisa_exposome_cq
    doi: 10.1021/acs.analchem.3c02697
    title: EISA-EXPOSOME
  dedup_kept_from: coll_eisa_exposome_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c02697
  all_source_dois:
  - 10.1021/acs.analchem.3c02697
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct the targeted peak extraction strategy for rescuing missed features

## Summary

This skill applies a targeted peak extraction strategy to LC-MS feature tables in order to rescue chemical features that traditional peak extraction algorithms fail to detect, thereby expanding the chemical substance annotation coverage without reliance on additional chemical standards.

## When to use

Your LC-MS feature table is incomplete or has low chemical coverage because traditional peak extraction algorithms (e.g., standard XCMS workflows) systematically miss features at m/z and retention time positions corresponding to known suspect compounds in your database. Use this skill when you have a suspect compound database (e.g., T3DB) and want to augment an existing feature table by deliberately extracting peaks at database-specified m/z–RT coordinates that were not recovered in the initial peak picking pass.

## When NOT to use

- Your input is already a high-coverage annotated feature table from a tool specifically designed for suspect screening (e.g., already processed through EISA); targeted extraction adds noise rather than coverage.
- You lack a validated suspect compound database or cannot justify the m/z and RT coordinates for your compounds of interest.
- Your LC-MS data has poor peak quality, high chemical noise, or insufficient mass accuracy (>10 ppm) to reliably distinguish targeted peaks from background.

## Inputs

- LC-MS raw data or preprocessed feature table (mzML, netCDF, or vendor format)
- Suspect compound database in .xlsx or .csv format with columns: NAME, PrecursorMZ, ProductMZ, Intensity, RT (optional), ID
- Existing feature table from traditional peak extraction (e.g., XCMS output)

## Outputs

- Augmented feature table with targeted-extraction-recovered features flagged and integrated
- Metadata table linking rescued features to suspect compound identities and database entries
- Visualization and filtering results from Shiny interface (optional)

## How to apply

Load your LC-MS raw data (or preprocessed feature table) and a structured suspect compound database (columns: NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID) into the EISA-EXPOSOME R Shiny environment. For each suspect compound in the database, use its known m/z and retention time as targeted extraction coordinates to search the raw LC-MS data for peaks that traditional algorithms missed. Integrate successfully recovered peaks back into your original feature table, labeling them as targeted-extraction rescues. Apply optional filtering and visualization through the Shiny interface to validate extracted features and remove false positives based on peak intensity and spectral coherence.

## Related tools

- **R Shiny (EISA-EXPOSOME interface)** (Interactive platform for applying targeted peak extraction, visualizing recovered features, and filtering results by intensity and retention time) — https://github.com/Lab-XUE/EISA-EXPOSOME
- **T3DB (compiled database file)** (Pre-formatted suspect compound database (.xlsx) providing m/z, RT, and product ion information for targeted extraction queries) — https://github.com/Lab-XUE/EISA-EXPOSOME

## Evaluation signals

- Number of features rescued by targeted extraction exceeds zero and is consistent with the number of suspect compounds in the database with valid m/z–RT coordinates.
- Rescued features appear in the augmented feature table with correct m/z ± mass accuracy tolerance (typically <5 ppm for high-resolution MS) and RT within expected retention window (±0.5 min).
- Intensity values of rescued peaks are above instrument noise floor and display reasonable product ion fragmentation patterns consistent with database records.
- Downstream chemical annotation coverage increases (e.g., more compounds identified in your sample) after targeted extraction compared to traditional peak extraction alone.
- Visualization in Shiny interface confirms that rescued features do not represent systematic artifacts or repeated extractions of the same underlying peak.

## Limitations

- The skill relies on the accuracy and completeness of the suspect compound database; missing or incorrect m/z or RT values will prevent recovery of true features or lead to false extractions.
- Targeted extraction may recover spurious peaks if the LC-MS data has high background noise, co-eluting contaminants, or poor mass calibration; manual validation or stricter intensity thresholds may be necessary.
- RT values in the database may shift between instruments or chromatographic methods; the workflow assumes RT data are either provided or can be reliably predicted or empirically validated.
- The strategy is designed for targeted screening of known suspect compounds; it does not discover novel or unanticipated chemical features not in the database.

## Evidence

- [intro] Targeted peak extraction strategy rescues features that cannot be extracted by traditional peak extraction algorithms: "used a targeted peak extraction strategy to rescue features that cannot be extracted by traditional peak extraction algorithms, improving the coverage of chemica substance annotation"
- [other] Workflow input and output specifications: "Load LC-MS feature/peak data and the suspect database (e.g., T3DB in .xlsx format) into memory. Apply the targeted peak extraction strategy to identify and extract peaks at m/z and retention time"
- [readme] Database format requirements: "your file (.xlsx /.csv) must contain the following columns:|NAME|PrecursorMZ|ProductMZ|Intensity|RT|ID|, **RT** is not essential."
- [readme] Platform and tool delivery: "We provide a Rshiny program for EISA-EXPOSOME, which runs with the interface shown below, and you can filter the results according to the visualisation interface"
- [intro] Benefit and coverage improvement: "can help reduce the dependence on chemical standards in traditional chemical analysis and significantly enhance the chemical coverage"
