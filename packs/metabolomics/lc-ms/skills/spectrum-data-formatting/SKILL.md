---
name: spectrum-data-formatting
description: Use when you have acquired raw or semi-processed mass spectra and need to search them against curated domain-specific databases (microbeMASST, plantMASST, etc.) using standalone web applications or batch APIs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - microbeMASST
  - GNPS_MASST
  - Fast Search API
  - MZmine
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41564-023-01575-9
  title: microbemasst
evidence_spans:
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_microbemasst_cq
    doi: 10.1038/s41564-023-01575-9
    title: microbemasst
  dedup_kept_from: coll_microbemasst_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41564-023-01575-9
  all_source_dois:
  - 10.1038/s41564-023-01575-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-data-formatting

## Summary

Normalize and format mass spectrometry spectra (m/z and intensity pairs) into standardized input formats (mzML, mzXML, or JSON) with consistent metadata fields before submission to domain-specific MASST search tools. This ensures compatibility with downstream spectral matching APIs and enables accurate retrieval of matched library spectra.

## When to use

You have acquired raw or semi-processed mass spectra and need to search them against curated domain-specific databases (microbeMASST, plantMASST, etc.) using standalone web applications or batch APIs. The trigger is: spectra are in heterogeneous formats, intensity values are not normalized to 0–100 scale, or metadata fields (precursor m/z, ionization mode, collision energy) are missing or inconsistent.

## When NOT to use

- Spectra are already in a curated GNPS library or MSP format and will be used only for visual inspection or local reference — formatting overhead is unnecessary.
- Your analysis goal is to perform de novo fragmentation prediction or in silico spectrum generation, not spectral library matching — formatting for MASST is not applicable.
- Input is already a pre-computed similarity matrix or feature table (e.g., presence/absence of known metabolites) — the spectrum objects themselves are not being searched.

## Inputs

- raw mass spectrum (m/z and intensity pairs in any format)
- metadata fields: precursor m/z, ionization mode, collision energy (optional)
- input file formats: .mgf, .mzML, .mzXML, .ms2, or CSV/TSV with m/z and intensity columns

## Outputs

- formatted spectrum file (mzML, mzXML, or JSON)
- normalized intensity vector (0–100 scale)
- structured metadata object with precursor m/z, ionization mode, collision energy

## How to apply

Load the raw mass spectrum as m/z and intensity pairs in any supported format. Normalize intensity values to a 0–100 scale (or library-standard range) and verify the precursor m/z, ionization mode (positive/negative), and collision energy (if available) are present and correctly encoded. Reformat the spectrum into the target structure (mzML, mzXML, or JSON with proper metadata headers). This step is essential because the microbeMASST API and Fast Search API require normalized intensities and standardized metadata to compute cosine similarity scores accurately and to enable filtering by ionization mode and collision energy during batch searches.

## Related tools

- **microbeMASST** (Target spectral search engine; accepts formatted spectra and returns ranked matches from microbial metabolome database) — https://masst.gnps2.org/microbemasst/
- **GNPS_MASST** (Codebase for standalone web applications; defines spectrum input schema and normalization requirements) — https://github.com/mwang87/GNPS_MASST
- **Fast Search API** (Batch search backend; requires normalized spectra and metadata for efficient querying across indexed repositories)
- **MZmine** (Upstream tool for generating .mgf files with properly normalized intensities and spectrum metadata) — https://github.com/mzmine/mzmine

## Evaluation signals

- Intensity values are all in the range [0, 100] after normalization, with the base peak set to 100.
- Precursor m/z, ionization mode, and collision energy (if applicable) are present and non-null in the output metadata object.
- Output file passes schema validation for the target format (mzML XSD, mzXML XSD, or JSON schema) without errors.
- Spectrum can be successfully submitted to microbeMASST API endpoint and returns a non-empty result set with match scores (cosine similarity) and ranked library matches.
- Batch job using jobs.py completes without entry failures related to spectrum format or metadata incompleteness (allowing for transient API timeouts).

## Limitations

- Collision energy metadata is optional and may not be available for all instruments; its absence does not prevent search but may reduce match precision.
- Intensity normalization to 0–100 scale assumes linear response; spectra from instruments with non-linear detectors or heavy noise may lose information during normalization.
- Some spectra from older datasets or non-standard acquisition may lack ionization mode or precursor m/z annotations; these must be inferred or manually curated before formatting.
- The Fast Search API may fail on first submission for some entries; re-running jobs.py with skip_existing=True is recommended until no new output is generated.

## Evidence

- [other] Normalization of intensities and formatting of metadata: "Prepare the spectrum for submission to the microbeMASST API or web interface by normalizing intensities and formatting metadata (precursor m/z, ionization mode, collision energy if available)."
- [other] Standard input formats accepted by microbeMASST: "Load or receive a single query mass spectrum (m/z and intensity pairs) in a standard format (mzML, mzXML, or JSON)."
- [readme] Batch search input flexibility via jobs.py: "You can run either a single .mgf file generated via MZmine, from the molecular networking in GNPS workflow, or a list of USIs provided either via a .csv or .tsv file."
- [readme] API search parameter tuning during batch runs: "Check and adjust the different parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks based on your research question."
