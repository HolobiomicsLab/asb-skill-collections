---
name: mass-spectral-query-submission
description: Use when you have one or more individual MS/MS spectra (in mzML, mzXML, or JSON format) and need to identify the compound(s) and their biological source by searching against a domain-specific spectral library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3407
  tools:
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - metadataMASST
  - GNPS_MASST
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
---

# mass-spectral-query-submission

## Summary

Submit a single mass spectrum query to a domain-specific MASST (Spectral Similarity Search Tool) web application and retrieve ranked spectral matches with similarity scores and taxonomic metadata. This skill enables rapid metabolite identification and microbial/plant/tissue/food source attribution by querying curated databases indexed by organism domain.

## When to use

You have one or more individual MS/MS spectra (in mzML, mzXML, or JSON format) and need to identify the compound(s) and their biological source by searching against a domain-specific spectral library. This is the appropriate choice when you want rapid, web-based interactive lookup rather than batch processing, or when your research question targets a specific biological domain (microbe, plant, tissue, microbiome, or food).

## When NOT to use

- Input is a batch of hundreds or thousands of spectra—use the batch search workflow via jobs.py and the Fast Search API instead.
- You require searches across ALL indexed databases regardless of biological domain—use the general GNPS/MassIVE MASST or the batch Fast Search API which queries GNPS, Metabolomics Workbench, MetaboLights, and NORMAN simultaneously.
- Your spectrum is already annotated at Level 3 or higher (structure confirmed by NMR or reference standard)—this skill provides Level 2 annotation by spectral library matching.

## Inputs

- Single mass spectrum in mzML, mzXML, or JSON format with m/z and intensity pairs
- Precursor m/z value
- Ionization mode (positive/negative)
- Collision energy (optional but recommended)

## Outputs

- Ranked list of matched spectra with cosine similarity scores
- Library spectrum metadata (compound name, InChI, SMILES if available)
- Organism lineage information (kingdom, phylum, class, order, family, genus, species, strain)
- Dataset and sample provenance for each match
- CSV or JSON formatted results table
- Optional: interactive visualization or tree structure of results

## How to apply

Load or receive a single query mass spectrum with m/z and intensity pairs in a supported format (mzML, mzXML, or JSON). Normalize spectrum intensities and format metadata including precursor m/z, ionization mode, and collision energy if available. Submit the prepared spectrum to the domain-specific MASST web interface (e.g., https://masst.gnps2.org/microbemasst/) via the application endpoint. The tool will return a ranked list of matching spectra from the curated domain database, scored by cosine similarity. Parse the structured output to extract match scores (typically cosine similarity threshold ≥0.6), library spectrum metadata, organism lineage information (kingdom, phylum, class, order, family, genus, species, strain), and associated dataset provenance. Export results as CSV or JSON containing ranked matches, similarity scores, and full taxonomic annotations for downstream analysis or visualization (e.g., via metadataMASST).

## Related tools

- **microbeMASST** (Standalone web application for single-spectrum query submission against microbial spectral library (8 kingdoms, 20 phyla, 561 genera, 1379 species)) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Standalone web application for single-spectrum query submission against plant spectral library (1 kingdom, 1 phylum, 1796 genera, 3712 species)) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Standalone web application for single-spectrum query submission against tissue/animal spectral library) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Standalone web application for single-spectrum query submission against microbiome/environment spectral library) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Standalone web application for single-spectrum query submission against food-derived spectral library) — https://masst.gnps2.org/foodmasst2/
- **metadataMASST** (Tool for aggregating and visualizing search results from multiple domain-specific MASST queries) — https://masst.gnps2.org/metadatamasst/
- **GNPS_MASST** (Core codebase implementing standalone web application API and spectrum submission logic for all domain-specific MASSTs) — https://github.com/mwang87/GNPS_MASST

## Evaluation signals

- Returned match list is non-empty and ranked by cosine similarity score in descending order.
- Top match(es) have cosine similarity ≥ 0.6 and associated organism lineage information is complete (at minimum genus and species).
- Output CSV/JSON parses without error and contains all required fields: match rank, similarity score, library spectrum ID, compound name, organism, dataset provenance.
- Results are specific to the queried domain (e.g., microbeMASST results contain only microbial taxa; plantMASST results contain plant taxa).
- Precursor m/z of query spectrum and top-ranked library matches are within expected m/z tolerance (typically ±0.1 Da for high-resolution MS).

## Limitations

- Single-spectrum submission is slow for batch queries; for >10 spectra, use jobs.py with the Fast Search API instead.
- Curated domain-specific libraries are smaller than the full GNPS/MassIVE database; queries may fail to find matches if the compound is rare or unrepresented in the curated subset.
- Some entries fail in initial Fast Search API calls and require re-running jobs.py multiple times (skip_existing=True) to catch all possible matches; interactive single-spectrum queries do not have this issue.
- Results are annotated at Level 2 (spectral library match) per Metabolomics Standards Initiative; identity is presumed but not confirmed by reference standard or NMR.
- Spectrum quality (signal-to-noise, fragment intensity patterns) directly affects match reliability; noisy or atypical spectra may return low similarity scores or false negatives.

## Evidence

- [other] Load or receive a single query mass spectrum (m/z and intensity pairs) in a standard format (mzML, mzXML, or JSON). Prepare the spectrum for submission to the microbeMASST API or web interface by normalizing intensities and formatting metadata (precursor m/z, ionization mode, collision energy if available). Submit the query spectrum to the microbeMASST web application endpoint and retrieve the ranked list of matching spectra from the microbeMASST database.: "Load or receive a single query mass spectrum (m/z and intensity pairs) in a standard format (mzML, mzXML, or JSON). Prepare the spectrum for submission to the microbeMASST API or web interface by"
- [other] microbeMASST is a standalone web application accessible at https://masst.gnps2.org/microbemasst/ that enables users to search one spectrum at a time and retrieve matched results.: "microbeMASST is a standalone web application accessible at https://masst.gnps2.org/microbemasst/ that enables users to search one spectrum at a time and retrieve matched results."
- [readme] The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST: "The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST"
- [other] Parse and structure the search results (match scores, library spectrum metadata, organism/taxonomy information) into a machine-readable output table. Format and save the results as a CSV or JSON file containing ranked matches with similarity scores and associated metadata.: "Parse and structure the search results (match scores, library spectrum metadata, organism/taxonomy information) into a machine-readable output table. Format and save the results as a CSV or JSON file"
- [readme] microbeMASST and plantMASST. These tools currently cover | microbeMASST | 8 | 20 | 48 | 124 | 278 | 561 | 1379 | 542 | | plantMASST | 1 | 1 | 11 | 81 | 319 | 1796 | 3712 | NA |: "microbeMASST and plantMASST. These tools currently cover taxonomy IDs with coverage of 8 kingdoms, 20 phyla, 561 genera, and 1379 species for microbeMASST"
- [readme] Aggregated search outputs can be generated and visualized using metadataMASST: "Aggregated search outputs can be generated and visualized using metadataMASST"
