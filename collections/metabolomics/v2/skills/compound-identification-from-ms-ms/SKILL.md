---
name: compound-identification-from-ms-ms
description: Use when you have LC-MS/MS data in mgf format and a custom spectral database prepared with CFM-id (or an in-built database), and you need to identify unknown compounds by comparing their experimental fragmentation patterns against predicted or reference spectra with quantified match scores.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  tools:
  - MS2Compound
  - CFM-id
  - MS2Compound v1.0.2
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1089/omi.2021.0051
  title: MS2Compound
evidence_spans:
- MS2Compound (v1.0.2) is a user friendly Graphical User Interface (GUI) for the identification of the compounds from LC-MS and MS/MS metabolomics data
- compatible with the customized database prepared using CFM-id, the fragment prediction tool
- The current version of MS2Compound is compatible with the customized database prepared using CFM-id, the fragment prediction tool.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2compound_cq
    doi: 10.1089/omi.2021.0051
    title: MS2Compound
  dedup_kept_from: coll_ms2compound_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1089/omi.2021.0051
  all_source_dois:
  - 10.1089/omi.2021.0051
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-identification-from-ms-ms

## Summary

Spectral matching workflow that searches LC-MS/MS query spectra (in Mascot Generic Format) against CFM-id-derived custom compound databases to identify compounds with similarity scores. This skill bridges fragmentation prediction and database-driven metabolite annotation.

## When to use

You have LC-MS/MS data in mgf format and a custom spectral database prepared with CFM-id (or an in-built database), and you need to identify unknown compounds by comparing their experimental fragmentation patterns against predicted or reference spectra with quantified match scores.

## When NOT to use

- Your LC-MS/MS data are in an unsupported format (not mgf); convert first using appropriate format conversion tools.
- You lack a relevant custom database for your compound class; CFM-id predictions may not be available or accurate for novel/highly unusual structures.
- You need real-time or streaming spectral identification; MS2Compound is batch-oriented with a GUI, not API-driven or command-line automated.

## Inputs

- Mascot Generic Format (mgf) file containing LC-MS/MS spectra with precursor m/z, charge, and fragment ion intensities
- Custom compound database prepared using CFM-id or in-built MS2Compound database
- Compound structure database with associated fragment predictions (CFM-id output)

## Outputs

- Identified compounds list with match scores and rankings
- Compound metadata (molecular formula, mass, structure)
- Fragment ion match annotations between query and database spectra
- Results file exportable in tabular or structured format

## How to apply

Load the custom compound database (prepared using CFM-id fragment predictions) into MS2Compound v1.0.2. Import the mgf query file containing your LC-MS/MS spectra. Execute the matching algorithm to compare each query spectrum against all database entries, computing similarity scores for each candidate. Export identified compounds ranked by match score along with metadata (retention time, precursor m/z, fragment ions). Evaluate results by inspecting the magnitude of the top match score relative to decoys, the rank of the top hit, and manual inspection of fragment ion matches against known fragmentation rules for the proposed structure.

## Related tools

- **CFM-id** (Fragment prediction tool used to prepare custom spectral databases compatible with MS2Compound)
- **MS2Compound v1.0.2** (GUI platform that executes spectral matching and compound identification against custom or in-built databases) — https://sourceforge.net/projects/ms2compound/

## Evaluation signals

- Match score magnitude: Top match(es) should have similarity scores substantially higher than background/decoy matches; inspect score distribution to detect false positives.
- Fragment ion coverage: Verify that matched database fragments align with observed query fragment m/z values (within instrument mass accuracy tolerance) and that major peaks are explained.
- Database consistency: Confirm that the custom database was successfully imported without errors and that database statistics (number of entries, mass range) match expectations.
- Rank stability: Rerun on technical replicates or pooled QC samples; expect consistent top-hit rankings for the same compounds across runs.
- Manual spectral inspection: For high-confidence identifications, visually compare query spectrum profile (peak heights, isotope patterns) against top-ranked match in MS2Compound viewer.

## Limitations

- Windows-only GUI (Windows 7, 8, 10); no Linux/macOS native support; requires minimum 2 GB RAM and Intel i3 64-bit CPU.
- Dependent on quality and completeness of the custom database; CFM-id predictions may be inaccurate for unusual or novel chemical structures not well-represented in training data.
- No changelog or version history provided in README; no discussion of algorithm updates or bug fixes between versions.
- Installation path must avoid spaces to prevent execution errors; directory path restrictions add friction to deployment.
- Limited automation: requires manual file import and export steps via GUI; not suitable for high-throughput automated pipelines without external scripting.

## Evidence

- [readme] MS2Compound (v1.0.2) is a user friendly Graphical User Interface (GUI) for the identification of the compounds from LC-MS and MS/MS metabolomics data.: "MS2Compound (v1.0.2) is a user friendly Graphical User Interface (GUI) for the identification of the compounds from LC-MS and MS/MS metabolomics data."
- [readme] The current version of MS2Compound is compatible with the customized database prepared using CFM-id, the fragment prediction tool. Mascot Generic Format (mgf) files can be used as query input file: "The current version of MS2Compound is compatible with the customized database prepared using CFM-id, the fragment prediction tool. Mascot Generic Format (mgf) files can be used as query input file"
- [other] Execute the matching algorithm to compare query spectra against database entries and compute similarity scores.: "Execute the matching algorithm to compare query spectra against database entries and compute similarity scores."
- [readme] The tool allows use of custom database for the identification of compounds.: "The tool allows use of custom database for the identification of compounds."
- [readme] Windows 7, 8, and 10: "Windows 7, 8, and 10"
